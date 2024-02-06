import random
from asyncio import sleep

from settings import *
from items import *

class Player:
    def __init__(self, user: nextcord.Member):
        self.User = user
        self.Name = user.name
        self.Health = Settings.PlayerHealth
        self.Items = [Item()]*Settings.MaxItems
        self.Handcuffed = False

class Game:
    def __init__(self, player1: nextcord.Member, player2: nextcord.Member, message: nextcord.Message):
        self.Player1, self.Player2 = Player(player1), Player(player2)
        self.Players = [self.Player1, self.Player2]
        self.Message = Utils.Message(message)
        
        class I:
            Round = 0
            Turn = None
            class Gun:
                Chamber = []
                Damage = 1
                Multi = 0
        self.Info = I
        
        class B:
            Play = self.ButtonPlay
            Shoot = self.ButtonShoot
            Item = self.ButtonItem
        self.Buttons = B

    @staticmethod
    def DebugMessage(text) -> str:
        return f"`{text}...`"
    
    @staticmethod
    async def ClearInteraction(interaction: nextcord.Interaction, empty: bool=False) -> None:
        try:
            await interaction.response.defer()
        except:
            pass
        await interaction.edit_original_message(content=Utils.Blank if empty else Game.DebugMessage(Settings.Messages.LoadOptions), view=None)

    async def StartRound(self) -> None:
        async def LoadGun() -> None:
            self.Info.Gun.Chamber = [*Settings.RoundConfig[self.Info.Round if self.Info.Round<len(Settings.RoundConfig) else -1]]
            random.shuffle(self.Info.Gun.Chamber)
            await self.UpdateDisplay()
        
        self.Info.Round+=1
        self.Info.Turn = random.choice(self.Players)

        await self.UpdateDisplay()
        for i in [
            [f"Round {self.Info.Round}", None],
            [
                lambda: f"{Settings.DrawConfig[self.Info.Round]} items drawn",
                lambda: self.DrawItems(Settings.DrawConfig[self.Info.Round if self.Info.Round<len(Settings.DrawConfig) else -1])
            ],
            [lambda: f"{self.Info.Gun.Chamber.count(1)} lives. {self.Info.Gun.Chamber.count(0)} blanks.", LoadGun],
            [f"{self.Info.Turn.Name} starts!", None]
        ]:
            if i[1]:
                await i[1]()
            await self.UpdateDialogue(i[0]() if type(i[0])==Utils.Function else i[0])
            await sleep(Settings.DialogueInterval)
            
        await self.Message.AddButton("Play", "⏯", self.Buttons.Play)

    async def EndGame(self, winner: Player, loser: Player) -> None:
        from bot import BRBot
        BRBot.UpdateStats(str(winner.User.id), True)
        BRBot.UpdateStats(str(loser.User.id), False)
        await self.UpdateDialogue(f"{winner.Name} wins!")
        BRBot.Games.remove(self)

    async def UpdateDialogue(self, text: str) -> None:
        self.Message.Embed.set_footer(text=text)
        await self.Message.Reference.edit(content="", embed=self.Message.Embed)

    async def UpdateDisplay(self) -> None:
        from bot import BRBot
        AddBlank = lambda d: d.add_field(name="", value="", inline=False) 

        display = BRBot.CreateEmbed("")
        display.add_field(name=f"**{self.Player1.Name} vs {self.Player2.Name}**", value="")
        AddBlank(display)
        display.add_field(
            name="", 
            value='🔫{}\n{}'.format("\u3000"+"".join(["☠" for _ in range(self.Info.Gun.Multi)]), "".join("❓" for _ in self.Info.Gun.Chamber) or Utils.Blank), 
            inline=False
        )
        AddBlank(display)
        display.add_field( 
            name="",
            value = "\n\n\n".join([
                '**{}**\n{}\n\n{}'.format(
                    i.Name+f"🔗"*i.Handcuffed, 
                    "".join(i.Items[j].Repr+"\n"*(j==len(i.Items)/2-1) for j in range(len(i.Items))), 
                    "".join("\u258D" for _ in range(i.Health)) or Utils.Blank
                ) for i in self.Players
            ]),
            inline=False
        )
        display.set_footer(text=(self.Message.Embed.footer.text or Utils.Blank) if self.Message.Embed else Utils.Blank)
        AddBlank(display)
        self.Message.Embed = display
        await self.Message.Reference.edit(content="", embed=display)

    async def Shoot(self, target: Player) -> None:
        bullet = self.Info.Gun.Chamber.pop()
        target.Health-=self.Info.Gun.Damage*bullet
        await self.UpdateDisplay()
        await self.UpdateDialogue(f'{self.Info.Turn.Name} shot {"themself" if self.Info.Turn==target else target.Name} with a {["blank", "live"][bullet]} round!')
        if bullet and self.Info.Gun.Damage>1:
            await sleep(Settings.DialogueInterval)
            await self.UpdateDialogue(f"Sawed-off shotgun deals {self.Info.Gun.Damage} damage!")
            self.Info.Gun.Damage = 1
            self.Info.Gun.Multi = 0
        await sleep(Settings.DialogueInterval)

        if target.Health<=0:
            return await self.EndGame(self.Players[not self.Players.index(target)], target)
        if not len(self.Info.Gun.Chamber):
            return await self.StartRound()

        other = self.Players[not self.Players.index(self.Info.Turn)]
        if not (not bullet and target==self.Info.Turn):
            if not other.Handcuffed:
                self.Info.Turn = other
            else:
                await sleep(Settings.DialogueInterval)
                await self.UpdateDialogue(f"Handcuffs skip {other.Name}'s turn!")
                other.Handcuffed = False
                await self.UpdateDisplay()
                await sleep(Settings.DialogueInterval)
        await self.UpdateDialogue(f"{self.Info.Turn.Name}'s turn!")
        await self.Message.AddButton("Play", "⏯", self.Buttons.Play)

    async def AddItem(self, player: Player, item: Item) -> None:
        states = [*map(lambda x: not x.Name, player.Items)]
        player.Items[len(states)-states[::-1].index(False) if states.count(False) else 0] = item
        await self.UpdateDisplay()

    async def DrawItems(self, count: int) -> None:
        for i in self.Players:
            curr = len([*filter(lambda x: x.Name, i.Items)])
            for _ in range(count if curr+count<=Settings.MaxItems else Settings.MaxItems-curr):
                await self.AddItem(i, random.choice(Items))
    
    async def UseItem(self, interaction: nextcord.Interaction, item: Item, player: Player) -> None:
        await self.UpdateDialogue(f"{player.Name} uses {item.Name}!")
        await sleep(Settings.DialogueInterval)
        await item.Callback(player, self, interaction)
        for i in reversed(range(len(player.Items))):
            if player.Items[i].Name==item.Name:
                player.Items[i] = Item()
                break
        await self.UpdateDisplay()

    async def ButtonPlay(self, interaction: nextcord.Interaction) -> None:
        if self.Message.Response:
            try:
                await self.Message.Response.delete()
            except:
                pass

        if interaction.user!=self.Info.Turn.User:
            return await interaction.response.send_message(content=Settings.Messages.NotTurn, ephemeral=True)
        message = Utils.Message(await interaction.response.send_message(content=Game.DebugMessage(Settings.Messages.LoadOptions), ephemeral=True))

        self.Message.Response = message.Reference
        await message.AddButton("Shoot", "🔫", self.Buttons.Shoot)
        await message.AddButton("Item", "🔧", self.Buttons.Item)

    async def ButtonShoot(self, interaction: nextcord.Interaction) -> None:
        await Game.ClearInteraction(interaction)
        message = Utils.Message(await interaction.original_message())

        current = self.Player1 if self.Player1.User==interaction.user else self.Player2
        enemy = self.Player2 if current==self.Player1 else self.Player2

        async def ClearButton():
            self.Message.View.clear_items()
            await self.Message.Update()

        async def c(_) -> None:
            await ClearButton()
            await Game.ClearInteraction(interaction, True)
            await self.Shoot(current)
        async def e(_) -> None:
            await ClearButton()
            await Game.ClearInteraction(interaction, True)
            await self.Shoot(enemy)

        await message.AddButton("Yourself", "🤓", c)
        await message.AddButton(enemy.User.name, "😈", e)
        await message.AddButton("Back", "↩", self.Buttons.Play)

    async def ButtonItem(self, interaction: nextcord.Interaction) -> None:
        await Game.ClearInteraction(interaction)
        message = Utils.Message(await interaction.original_message())

        async def InvokeItem(interaction: nextcord.Interaction, item: Item, player: Player) -> None:
            await self.UseItem(interaction, item, player)
            await self.ButtonItem(interaction)
            if not len(self.Info.Gun.Chamber):
                await Game.ClearInteraction(interaction, True)
                await sleep(Settings.DialogueInterval)
                await self.StartRound()

        player = self.Player1 if interaction.user==self.Player1.User else self.Player2
        for item in [i for i in Items if i.Name and [*filter(lambda x: x.Name==i.Name, player.Items)]]:
            await message.AddButton(item.Name, item.Repr, lambda i: InvokeItem(i, item, player))
        await message.AddButton("Back", "↩", self.Buttons.Play)