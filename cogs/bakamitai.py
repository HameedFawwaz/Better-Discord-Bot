import discord
from discord.ext import commands, tasks
import functools
from processes.process import dame
from utils.baka import Mitai

class Bakamitai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    def cog_check(self, ctx):
        return True


    @commands.command()
    async def bakamitai(self, ctx):
        mitai = Mitai()
        await ctx.send("Enter the image that you would like to make a meme out of")
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        original_picture = await self.bot.wait_for('message', check=check)

        if original_picture:

            pat, track = mitai._get_user_info(user_id = ctx.author.id)
            if track == 0:
                mitai.update_value(column = "track", value = 1, user=ctx.author.id)
                await ctx.send("Processing, this will take a bit, please consider donating to help support Kiryu, this will help decrease the processing time and make it better overall. To get the patreon link, use =patreon.\nNote: processing will take around 20 minutes")

                picture = original_picture.attachments

                for att in picture:

                    try:
                        async with ctx.typing():
                            actual_picture = await att.save(fp = f"saved/{ctx.message.id}.png")

                            dame_ = dame()

                            args = functools.partial(dame_.dane, ctx)

                            await self.bot.loop.run_in_executor(None, args)

                            await ctx.send(content = "Here is your baka mitai meme!", file = discord.File(f"./generated/{ctx.message.id}2.mp4"))
                    except:
                        await ctx.send("There was an error in processing, this is most likely due to an incorrect file entered or an unexpected error, try again.")

            elif pat == 1:
                await ctx.send("Processing, this will take a bit, because you have been supporting Kiryu, you can make as many memes as you want! Either way, it will still take around 20 minutes.")

                picture = original_picture.attachments

                for att in picture:

                    try:
                        async with ctx.typing():
                            actual_picture = await att.save(fp = f"saved/{ctx.message.id}.png")
                            dame_ = dame()

                            args = functools.partial(dame_.dane, ctx)

                            await self.bot.loop.run_in_executor(None, args)

                            await ctx.send(content = "Here is your baka mitai meme!", file = discord.File(f"./generated/{ctx.message.id}2.mp4"))
                    except:
                        await ctx.send("There was an error in processing, this is most likely due to an incorrect file entered or an unexpected error, try again.")
            else:
                await ctx.send("You have reach your hourly limit for making memes, to make another meme, vote for Kiryu: https://top.gg/bot/747927452138864761/vote")



def setup(bot):
    bot.add_cog(Bakamitai(bot))
