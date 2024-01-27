import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import random

from settings import *


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
        self.Display = message
        self.Info = GameInfo()

    async def UpdateDisplay(self):
        from bot import BRBot

        display = BRBot.CreateEmbed("")
        display.add_field(name=f"**{self.Player1.Name} vs {self.Player2.Name}**\n\n", value="")
        display.add_field(name=chr(173), value=chr(173))
        display.add_field( 
            name="",
            value = "\n\n".join(['**{}**:\n{}'.format(i.Name, "".join("\u258D" for _ in range(i.Health))) for i in [self.Player1, self.Player2]]),
            inline=False
        )
        await self.Display.edit(content="", embed=display)