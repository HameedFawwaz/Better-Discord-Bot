import discord
from discord.ext import commands

import os
import json




class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return True

    
    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send("The help message was sent to your DM")
        embed = discord.Embed(title="Help Command", description = "**=create**: The youtube video compiler which takes clips from videos and puts them together to create a video clip compilation\n**=bakamitai**: Creates a Baka Mitai (Dame Da ne) meme using a picture\n**=spellingbee**: Start a spelling bee, you must be in a voice channel in order for this to work")
        await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))