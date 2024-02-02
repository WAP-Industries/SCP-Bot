from utils import *

class Item:
    def __init__(self, name: str=None, repr: str=None, callback: Utils.Function=None):
        self.Name = name
        self.Repr = repr or "⍰"
        self.Callback = callback

    class Callbacks:
        @staticmethod
        async def Beer(player, game, interaction):
            await game.UpdateDialogue(f'A {["blank", "live"][game.Info.Gun.Chamber.pop()]} round pops out of the shotgun.')

        @staticmethod
        async def Saw(player, game, interaction):
            game.Info.Gun.Damage*=2
            game.Info.Gun.Multi+=1
            await game.UpdateDialogue("Shotgun damage doubled!")

        @staticmethod
        async def Cigarette(player, game, interaction):
            player.Health+=1
            await game.UpdateDialogue(f"{player.Name} regains 1 Health!")

        @staticmethod
        async def MagnifyingGlass(player, game, interaction):
            from bot import BRBot
            embed = BRBot.CreateEmbed("")
            embed.add_field(
                name="", 
                value=f'🔫\n{"".join("❓" for _ in range(len(game.Info.Gun.Chamber)-1))+"🔵🔴"[game.Info.Gun.Chamber[-1]]}'
            )
            await game.UpdateDialogue(f"{player.Name} inspects the chamber...")
            await interaction.response.defer()
            await interaction.followup.send(Utils.Blank, embed=embed, ephemeral=True)

        @staticmethod
        async def Handcuffs(player, game, interaction):
            target = game.Players[not game.Players.index(player)]
            target.Handcuffed = True
            await game.UpdateDialogue(f"{player.Name} handcuffs {target.Name} to the table!")


Items = [
    Item("Beer", "🍺", Item.Callbacks.Beer),
    Item("Hand Saw", "🪚", Item.Callbacks.Saw),
    Item("Cigarette", "🚬", Item.Callbacks.Cigarette),
    Item("Magnifying Glass", "🔍", Item.Callbacks.MagnifyingGlass),
    Item("Handcuffs", "🔗", Item.Callbacks.Handcuffs)
]