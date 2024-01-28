import random

from settings import *
from utils import *


class Player:
    def __init__(self, user: nextcord.Member, health: int=5):
        self.User = user
        self.Name = user.name
        self.Health = health

class GameInfo:
    def __init__(self):
        self.Round = 1
        self.Turn = None
        self.Gun = random.shuffle(Settings.RoundConfig[self.Round])

class Game:
    def __init__(self, player1: nextcord.Member, player2: nextcord.Member, message: nextcord.Message):
        self.Player1, self.Player2 = Player(player1), Player(player2)
        self.Players = [self.Player1, self.Player2]
        self.Info = GameInfo()
        self.Message = Utils.Message(message)

    @staticmethod
    def DebugMessage(text):
        return f"`{text}...`"

    async def UpdateDialogue(self):
        pass

    async def UpdateDisplay(self):
        from bot import BRBot

        display = BRBot.CreateEmbed("")
        display.add_field(name=f"**{self.Player1.Name} vs {self.Player2.Name}**", value="")
        display.add_field(name="", value="", inline=False)
        display.add_field( 
            name="",
            value = "\n\n".join(['**{}**:\n{}'.format(i.Name, "".join("\u258D" for _ in range(i.Health))) for i in self.Players]),
            inline=False
        )

        self.Message.Embed = display
        await self.Message.Reference.edit(content="", embed=display)

    async def Play(self, interaction: nextcord.Interaction):
        message = Utils.Message(await interaction.response.send_message(content=Game.DebugMessage(Settings.Messages.LoadOptions), ephemeral=True))
        await message.AddButton("Shoot", "🔫", self.Shoot)

    async def Shoot(self, interaction: nextcord.Interaction):
        message = Utils.Message(await interaction.response.send_message(content=Game.DebugMessage(Settings.Messages.LoadOptions), ephemeral=True))
        await message.AddButton("Yourself", "🤓", lambda _:0)
        await message.AddButton([i for i in self.Players if i.User!=interaction.user][0].User.name, "😈", lambda _:0)