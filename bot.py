from game import *
import json
import os

class BRBot:
    CommandPrefix = "?"
    Bot = commands.Bot(command_prefix=CommandPrefix, intents=nextcord.Intents.all())
    Games = []
    Stats, StatsFile = {}, "stats.json"

    @staticmethod
    def PlayerInGame(player: nextcord.Member) -> bool:
        return bool(len([*filter(lambda x: player in map(lambda y: y.User, x.Players), BRBot.Games)]))

    @staticmethod
    def CheckUser(func) -> Utils.Function:
        async def wrapper(ctx: commands.Context, user: str) -> None:
            try:
                return await func(ctx, await commands.MemberConverter().convert(ctx, user))
            except:
                await ctx.reply(Settings.Messages.NoUser(user))
        return wrapper

    @staticmethod
    def CreateEmbed(title: str) -> nextcord.Embed:
        return nextcord.Embed(title=title, color=nextcord.Color(0x2c2c34))
    
    @staticmethod
    def LoadStats() -> None:
        if not os.path.exists(BRBot.StatsFile):
            with open(BRBot.StatsFile, "w") as f:
                f.write(json.dumps({}))
        with open(BRBot.StatsFile) as f:
            BRBot.Stats = json.loads(f.read())

    @staticmethod
    def UpdateStats(pid: str, win: bool) -> None:
        if pid not in BRBot.Stats:
            BRBot.Stats[pid] = {
                 "Win": 0,
                 "Lose": 0,
            }
        BRBot.Stats[pid][["Lose", "Win"][win]]+=1
        with open(BRBot.StatsFile, "w") as f:
            f.write(json.dumps(BRBot.Stats, indent=4))

    @Bot.event
    async def on_ready() -> None:
        print("im running nigger")

    # remember to remove this when bot is finished
    @Bot.command()
    async def clearstats(ctx) -> None:
        if not ctx.author.guild_permissions.administrator:
            return await ctx.reply("You dont have permissions for this command nigger")
        BRBot.Stats = {}
        with open(BRBot.StatsFile, "w") as f:
            f.write(json.dumps({}))
        await ctx.reply("Player stats deleted")

    @Bot.command(help="Closes the bot")
    async def exit(ctx: commands.Context) -> None:
        await ctx.send("bye nigger")
        await BRBot.Bot.close()

    @Bot.command(name="play", help="Starts a game of Buckshot Roulette")
    @CheckUser
    async def play(ctx: commands.Context, user: nextcord.Member) -> None:
        if user==ctx.author:
            return await ctx.reply(Settings.Messages.SelfChallenge)
        
        if BRBot.PlayerInGame(ctx.author):
            return await ctx.reply(Settings.Messages.AlreadyInGame("You're"))
        
        if BRBot.PlayerInGame(user):
            return await ctx.reply(Settings.Messages.AlreadyInGame(f"{user.name} is"))

        game = Game(ctx.author, user, await ctx.send(Game.DebugMessage(Settings.Messages.NewGame)))
        BRBot.Games.append(game)
        await game.StartRound()

    @Bot.command(name="stats", help="Display player statistics")
    @CheckUser
    async def stats(ctx: commands.Context, user: nextcord.Member) -> None:
        menu = BRBot.CreateEmbed(f"{user.name}'s Stats")
        win, lose = [0]*2 if str(user.id) not in BRBot.Stats else BRBot.Stats[str(user.id)].values()
        ratio = win/lose if lose else win

        menu.add_field(name=f"Wins: {win}", value="", inline=False)
        menu.add_field(name=f"Losses: {lose}", value="", inline=False)
        menu.add_field(name=f"KDR: {int(ratio) if int(ratio)==ratio else round(ratio, 2)}", value="")
        await ctx.send(embed=menu)


BRBot.Bot.remove_command("help")
@BRBot.Bot.command(help="Shows this message")
async def help(ctx: commands.Context) -> None:
    menu = BRBot.CreateEmbed("Commands")
    menu.add_field(name="", value="\n\n".join([f"**{BRBot.CommandPrefix}{i.name}**\n{i.help}" for i in BRBot.Bot.commands]))
    await ctx.send(embed=menu)