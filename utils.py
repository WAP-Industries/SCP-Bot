import nextcord
from nextcord.ext import commands

class Utils:
    Blank = chr(173)
    Function = type(abs)

class __Message__:
    def __init__(self, message: nextcord.Message):
        self.Reference = message
        self.Embed = None
        self.View = nextcord.ui.View()

    async def Update(self):
        await self.Reference.edit(content=Utils.Blank, embed=self.Embed, view=self.View)
    
    async def AddButton(self, text: str, emoji: str, callback: Utils.Function):
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.primary, label=text, emoji=emoji)
        button.callback = callback
        self.View.add_item(button)
        await self.Update()

    async def ClearButtons(self):
        self.View.clear_items()
        await self.Update()

Utils.Message = __Message__