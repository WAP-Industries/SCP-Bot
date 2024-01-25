import nextcord
from nextcord.ext import commands

class SCPBot:
    CommandPrefix = "?"
    Bot = commands.Bot(command_prefix=CommandPrefix, intents=nextcord.Intents.all())

    @Bot.event
    async def on_ready():
        print("im running nigger")

    @Bot.command(help="Closes the bot")
    async def exit(ctx):
        await ctx.send("bye nigger")
        await SCPBot.Bot.close()
        
        
SCPBot.Bot.remove_command('help')
@SCPBot.Bot.command(help="Shows this message")
async def help(ctx):
    menu = nextcord.Embed(title="Commands", color=nextcord.Color.blue())
    menu.add_field(name="", value="\n\n".join([f"**{SCPBot.CommandPrefix}{i.name}**\n{i.help}" for i in SCPBot.Bot.commands]))
    menu.set_footer(text=ctx.guild.name)
    await ctx.send(embed=menu)