from game import *

class BRBot:
  CommandPrefix = "?"
  Bot = commands.Bot(command_prefix=CommandPrefix, intents=nextcord.Intents.all())
  Games = []

  @staticmethod
  def CreateEmbed(title: str):
        return nextcord.Embed(title=title, color=nextcord.Color(0x2c2c34))

  @Bot.event
  async def on_ready():
    print("im running nigger")

  @Bot.command(help="Closes the bot")
  async def exit(ctx: commands.Context):
    await ctx.send("bye nigger")
    await BRBot.Bot.close()

  @Bot.command()
  async def play(ctx: commands.Context, user: nextcord.Member):
    game = Game(ctx.author, user, await ctx.send(Game.DebugMessage(Settings.Messages.NewGame)))
    await game.UpdateDisplay()
    await game.UpdateDialogue(f"{game.Info.Gun.count(1)} lives. {game.Info.Gun.count(0)} blanks.")
    sleep(Settings.DialogueInterval)
    await game.Message.AddButton("Play", "⏯", game.Buttons.Play)
    # game.Info.Turn = random.choice(game.Players)
    game.Info.Turn = game.Player1
    await game.UpdateDialogue(f"{game.Info.Turn.Name} starts!")
    BRBot.Games.append(game)


BRBot.Bot.remove_command("help")
@BRBot.Bot.command(help="Shows this message")
async def help(ctx: commands.Context):
  menu = BRBot.CreateEmbed("Commands")
  menu.add_field(name="", value="\n\n".join([f"**{BRBot.CommandPrefix}{i.name}**\n{i.help}" for i in BRBot.Bot.commands]))
  await ctx.send(embed=menu)