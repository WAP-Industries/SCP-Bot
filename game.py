import random
from time import sleep

from settings import *
from utils import *


class Player:
    def __init__(self, user: nextcord.Member, health: int=5):
        self.User = user
        self.Name = user.name
        self.Health = health

class GameInfo:
    def __init__(self):
        self.Round = 0
        self.Turn = None
        self.Gun = []

class Game:
    def __init__(self, player1: nextcord.Member, player2: nextcord.Member, message: nextcord.Message):
        self.Player1, self.Player2 = Player(player1), Player(player2)
        self.Players = [self.Player1, self.Player2]
        self.Info = GameInfo()
        self.Message = Utils.Message(message)
        self.Dialogue = ""
        
        class B:
            Play = self.ButtonPlay
            Shoot = self.ButtonShoot
        self.Buttons = B

    @staticmethod
    def DebugMessage(text):
        return f"`{text}...`"

    async def StartRound(self):
        self.Info.Round+=1
        self.Info.Gun = Settings.RoundConfig[self.Info.Round]
        random.shuffle(self.Info.Gun)
        self.Info.Turn = self.Player1

        await self.UpdateDisplay()
        for i in [
            f"Round {self.Info.Round}",
            f"{self.Info.Gun.count(1)} lives. {self.Info.Gun.count(0)} blanks.",
            f"{self.Info.Turn.Name} starts!"
        ]:
            await self.UpdateDialogue(i)
            sleep(Settings.DialogueInterval)
        await self.Message.AddButton("Play", "⏯", self.Buttons.Play)

    async def UpdateDialogue(self, text):
        self.Dialogue = text
        self.Message.Embed.set_footer(text=text)
        await self.Message.Reference.edit(content="", embed=self.Message.Embed)

    async def UpdateDisplay(self):
        from bot import BRBot
        AddBlank = lambda d: d.add_field(name="", value="", inline=False) 

        display = BRBot.CreateEmbed("")
        display.add_field(name=f"**{self.Player1.Name} vs {self.Player2.Name}**", value="")
        AddBlank(display)
        display.add_field(name="", value=f'🔫\n{"".join("❓" for _ in self.Info.Gun) or Utils.Blank}', inline=False)
        AddBlank(display)
        display.add_field( 
            name="",
            value = "\n\n".join(['**{}**\n{}'.format(i.Name, "".join("\u258D" for _ in range(i.Health))) for i in self.Players]),
            inline=False
        )
        display.set_footer(text=self.Dialogue)
        AddBlank(display)
        self.Message.Embed = display
        await self.Message.Reference.edit(content="", embed=display)

    async def Shoot(self, target: Player):
        bullet = self.Info.Gun.pop()
        target.Health-=1*bullet
        await self.UpdateDisplay()
        await self.UpdateDialogue(f'{self.Info.Turn.Name} shot {"themself" if self.Info.Turn==target else target.Name} with a {["blank", "live"][bullet]} round!')
        sleep(Settings.DialogueInterval)
        self.Info.Turn = [i for i in self.Players if i!=self.Info.Turn][0]
        await self.UpdateDialogue(f"{self.Info.Turn.Name}'s turn!")

    async def ButtonPlay(self, interaction: nextcord.Interaction):
        if interaction.user!=self.Info.Turn.User:
            return await interaction.response.send_message(content=Settings.Messages.NotTurn, ephemeral=True)
        message = Utils.Message(await interaction.response.send_message(content=Game.DebugMessage(Settings.Messages.LoadOptions), ephemeral=True))
        await message.AddButton("Shoot", "🔫", self.Buttons.Shoot)

    async def ButtonShoot(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        message = Utils.Message(await interaction.original_message())
        await interaction.edit_original_message(content=Game.DebugMessage(Settings.Messages.LoadOptions), view=None)

        current = self.Player1 if self.Player1.User==interaction.user else self.Player2
        enemy = self.Player2 if current==self.Player1 else self.Player2

        async def c(_):
            await interaction.edit_original_message(content=Utils.Blank, view=None)
            await self.Shoot(current)
        async def e(_):
            await interaction.edit_original_message(content=Utils.Blank, view=None)
            await self.Shoot(enemy)

        await message.AddButton("Yourself", "🤓", c)
        await message.AddButton(enemy.User.name, "😈", e)