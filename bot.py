from game import *
import json
import os

class BRBot:
  CommandPrefix = "?"
  Bot = commands.Bot(command_prefix=CommandPrefix, intents=nextcord.Intents.all())
  Games = []
  Stats, StatsFile = {}, "stats.json"

  @staticmethod
  def CreateEmbed(title: str):
        return nextcord.Embed(title=title, color=nextcord.Color(0x2c2c34))
  
  @staticmethod
  def LoadStats():
      if not os.path.exists(BRBot.StatsFile):
        with open(BRBot.StatsFile, "w") as f:
          f.write({})
      with open(BRBot.StatsFile) as f:
         BRBot.Stats = json.loads(f.read())

  @staticmethod
  def UpdateStats(pid: str, win: bool):
    if pid not in BRBot.Stats:
      BRBot.Stats[pid] = {
         "Win": 0,
         "Lose": 0,
      }
    BRBot.Stats[pid][["Lose", "Win"][win]]+=1
    with open(BRBot.StatsFile, "w") as f:
      f.write(json.dumps(BRBot.Stats, indent=4))

  @Bot.event
  async def on_ready():
    print("im running nigger")

  @Bot.command(help="Closes the bot")
  async def exit(ctx: commands.Context):
    await ctx.send("bye nigger")
    await BRBot.Bot.close()

  @Bot.command(help="Starts a game of Buckshot Roulette")
  async def play(ctx: commands.Context, user: nextcord.Member):
    if user==ctx.author:
      return await ctx.reply(Settings.Messages.SelfChallenge)

    game = Game(ctx.author, user, await ctx.send(Game.DebugMessage(Settings.Messages.NewGame)))
    await game.StartRound()

  @Bot.command(help="Display player statistics")
  async def stats(ctx: commands.Context, user: nextcord.Member):
    menu = BRBot.CreateEmbed(f"{user.name}'s Stats")
    win, lose = [0]*2 if str(user.id) not in BRBot.Stats else BRBot.Stats[str(user.id)].values()
    ratio = win/lose if lose else win

    menu.add_field(name=f"Wins: {win}", value="", inline=False)
    menu.add_field(name=f"Losses: {lose}", value="", inline=False)
    menu.add_field(name=f"KDR: {int(ratio) if int(ratio)==ratio else round(ratio, 2)}", value="")
    await ctx.send(embed=menu)


BRBot.Bot.remove_command("help")
@BRBot.Bot.command(help="Shows this message")
async def help(ctx: commands.Context):
  menu = BRBot.CreateEmbed("Commands")
  menu.add_field(name="", value="\n\n".join([f"**{BRBot.CommandPrefix}{i.name}**\n{i.help}" for i in BRBot.Bot.commands]))
  await ctx.send(embed=menu)