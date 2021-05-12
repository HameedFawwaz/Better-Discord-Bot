import discord
from discord.ext import commands
import traceback
from utils.baka import Mitai
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "=", intents=intents, help_command=None)

initial_extensions = [
    "cogs.bakamitai",
    "cogs.spellingbee",
    "cogs.vc",
    "cogs.help"
]



if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")
            traceback.print_exc()

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    print(f"Running on version {discord.__version__}")

@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    embed = discord.Embed(title = f"Current Ping: {ping}ms")
    await ctx.send(embed=embed)

@bot.command()
async def patreon(ctx):
    await ctx.send("Here is the link for the patreon: https://www.patreon.com/user?u=50267291")

@bot.command()
async def vote(ctx):
    await ctx.send("Vote for Kiryu here: https://top.gg/bot/747927452138864761/vote")

async def hourly_reset():
    await bot.wait_until_ready()

    while not bot.is_closed():
        guild = bot.get_guild(751101561169772674)
        for member in guild.members:
            for x in member.roles:
                if x.id == 810330999145758730:
                    mitai = Mitai()
                    mitai.update_value(user=member.id, column='pat', value='1')

                else:
                    mitai = Mitai()
                    mitai.update_value(user=member.id, column='pat', value='0')

        else:
            await asyncio.sleep(30)

bot.loop.create_task(hourly_reset())
bot.run("NjExMjQ1Njg0ODg4MTc0NTky.XVRA5w.5Ew8X2mOJZn9z3pAk8qq87_tjGc")