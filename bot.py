import nextcord
from nextcord.ext import commands

class SCPBot:
    Bot = commands.Bot(command_prefix="?", intents=nextcord.Intents.all())

    @Bot.event
    async def on_ready():
        print("im running nigger")

    @Bot.command()
    async def exit(ctx):
        await ctx.send("bye nigger")
        await SCPBot.Bot.close()