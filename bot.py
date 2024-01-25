import nextcord
from nextcord.ext import commands

class SCPBot:
    Bot = commands.Bot(command_prefix="?", intents=nextcord.Intents.all())

    @Bot.event
    async def on_ready():
        print("im running nigger")

    @Bot.command(help="closes the bot")
    async def exit(ctx):
        await ctx.send("bye nigger")
        await SCPBot.Bot.close()


class CustomHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        command_list = [*mapping.values()][0]
        longest = max(map(lambda x:len(x.name), command_list))
        await self.get_destination().send("```{}```".format('\n'.join([f'{i.name:<{longest+5}}{i.short_doc}' for i in command_list])))
        
SCPBot.Bot.help_command = CustomHelp()