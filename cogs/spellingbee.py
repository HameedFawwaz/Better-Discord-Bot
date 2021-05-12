import discord
from discord.ext import commands
from discord.utils import get

import pyttsx3
from playsound import playsound
import random
from pydub import AudioSegment
import operator

from datetime import datetime

from utils.quizScore import QuizScoreDB

import asyncio
import os
import json



class Bee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        self.ScoreDB = QuizScoreDB(bot = self.bot, guild = ctx.guild)
        return True


    @commands.command()
    async def spellingbee(self, ctx):

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.runAndWait()

        reactions = []
        
        embed = discord.Embed(title = "Spelling Bee", description = "React if you are participating in the Spelling Bee.")
        message = await ctx.send(embed = embed)

        await message.add_reaction("✅")

        for i in range(10, -1, -1):
            new_embed = discord.Embed(title="Spelling Bee", description = "React if you are participating in the Spelling Bee.")
            new_embed.set_footer(text=f"Time remaining: {i}s")
            await message.edit(embed=new_embed)
            await asyncio.sleep(1)
        else:
            new_message = await ctx.channel.fetch_message(message.id)

            

            for reaction in new_message.reactions:
                for user in await reaction.users().flatten():
                    reactions.append(user.id)
            else:
                voice = get(self.bot.voice_clients, guild = ctx.guild)
                channel = ctx.author.voice.channel
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()

                print(engine.getProperty('voices'))
                
                tts = engine.save_to_file("Let's set up this spelling bee! First off, how many rounds do you want to play?", "resources/setup.mp3")
                engine.runAndWait()

                voice.play(discord.FFmpegPCMAudio("resources/setup.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.25
                await asyncio.sleep(5)

                def first_check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                    
                reply = await self.bot.wait_for("message", check=first_check)
                member_list = {}
                if reply:
                
                    for user in reactions:
                        member = ctx.guild.get_member(user)
                        
                        if not member.bot:
                            member_list.update({member.id: 0})
                            def check(message):
                                return message.author == member and message.channel == ctx.channel

                            spelling_words = ["misspell", "pharaoh", "weird", "intelligence", "pronunciation", "handkerchief", "logorrhea", "chiaroscurist", 'flavor', 'stimulation', 'entertainment', 'prisoner', 'tread', 'intervention', 'hen', 'easy', 'nuance', 'behavior', 'headline', 'rehabilitation', 'wage', 'lay', 'worm', 'bang', 'delivery', 'missile', 'season', 'seem', 'foot', 'pottery', 'money', 'medieval', 'paralyzed', 'disclose', 'public', 'indoor', 'merit', 'physics', 'viable', 'strike', 'float', 'my', 'vegetable', 'fraction', 'ecstasy', 'parallel', 'racism', 'conscious', 'classroom', 'wear', 'foundation', 'breathe', 'inspector', 'fat', 'harass', 'housewife', 'contrast', 'prayer']
                            spelling_message = spelling_words[random.randint(0, 56)]

                            print(spelling_message)
                            
                            engine.save_to_file(f"Ok, {member.name} is up. How do you spell: {spelling_message}?", "resources/word.mp3")
                            engine.runAndWait()
                            engine.stop()

                            voice.play(discord.FFmpegPCMAudio("resources/word.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                            voice.source = discord.PCMVolumeTransformer(voice.source)
                            voice.source.volume = 0.25
                            await asyncio.sleep(5)

                            reply1 = await self.bot.wait_for("message", check=check)
                            if reply1.content.lower() == spelling_message:
                                score = member_list[member.id]
                                new_score = member_list[member.id] = score + 1
                                engine.save_to_file(f"Great! You spelled the word correctly, your score is: {score + 1}.", "resources/result.mp3")
                                engine.runAndWait()
                                engine.stop()

                                
                                voice.play(discord.FFmpegPCMAudio("resources/result.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                                voice.source = discord.PCMVolumeTransformer(voice.source)
                                voice.source.volume = 0.25
                                await asyncio.sleep(7)

                                print(reply.content)
                                for i in range(0, int(reply.content) - 1):
                                    if i != -1:
                                        spelling_words = ["misspell", "pharaoh", "weird", "intelligence", "pronunciation", "handkerchief", "logorrhea", "chiaroscurist", 'flavor', 'stimulation', 'entertainment', 'prisoner', 'tread', 'intervention', 'hen', 'easy', 'nuance', 'behavior', 'headline', 'rehabilitation', 'wage', 'lay', 'worm', 'bang', 'delivery', 'missile', 'season', 'seem', 'foot', 'pottery', 'money', 'medieval', 'paralyzed', 'disclose', 'public', 'indoor', 'merit', 'physics', 'viable', 'strike', 'float', 'my', 'vegetable', 'fraction', 'ecstasy', 'parallel', 'racism', 'conscious', 'classroom', 'wear', 'foundation', 'breathe', 'inspector', 'fat', 'harass', 'housewife', 'contrast', 'prayer']
                                        spelling_message = spelling_words[random.randint(0, 56)]
                                        print(spelling_message)

                                        engine.save_to_file(f"Here's the next word, how do you spell: {spelling_message}?", f"resources/word{i}.mp3")
                                        engine.runAndWait()

                                        voice.play(discord.FFmpegPCMAudio(f"resources/word{i}.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                                        voice.source = discord.PCMVolumeTransformer(voice.source)
                                        voice.source.volume = 0.25
                                        await asyncio.sleep(5)
                                        

                                        reply2 = await self.bot.wait_for("message", check=check)
                                        if reply2.content.lower() == spelling_message:
                                            score = member_list[member.id]
                                            new_score = member_list[member.id] = score + 1
                                            print(member_list)

                                            engine.save_to_file(f"Great! You spelled the word correctly, your score is: {new_score}.", f"resources/result{i}.mp3")
                                            engine.runAndWait()

                                            voice.play(discord.FFmpegPCMAudio(f"resources/result{i}.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                                            voice.source = discord.PCMVolumeTransformer(voice.source)
                                            voice.source.volume = 0.25
                                            
                                        
                                        else:
                                            engine.save_to_file("Oh No! You spelled the word wrong. Now go back to your fucking special ed school. ", "resources/bad.mp3")
                                            engine.runAndWait()

                                            sound1 = AudioSegment.from_mp3("resources/bruh.mp3")
                                            sound2 = AudioSegment.from_mp3("resources/bad.mp3")

                                            total = sound1 + sound2

                                            await asyncio.sleep(5)
                                            total.export("resources/result.mp3", format="mp3")
                                            voice.play(discord.FFmpegPCMAudio("resources/result.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                                            voice.source = discord.PCMVolumeTransformer(voice.source)
                                            voice.source.volume = 0.25
                                            

                            else:
                                engine.save_to_file("Oh No! You spelled the word wrong. Now go back to your fucking special ed school.", "resources/bad.mp3")
                                engine.runAndWait()

                                sound1 = AudioSegment.from_mp3("resources/bruh.mp3")
                                sound2 = AudioSegment.from_mp3("resources/bad.mp3")

                                total = sound1 + sound2

                                total.export("resources/result.mp3", format="mp3")

                                await asyncio.sleep(7)
                                voice.play(discord.FFmpegPCMAudio("resources/result.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                                voice.source = discord.PCMVolumeTransformer(voice.source)
                                voice.source.volume = 0.25
                                
                    else:     
                            x = max(member_list.items(), key=operator.itemgetter(1))[0]
                            score = member_list[x]
                            user = ctx.guild.get_member(x)
                            engine.save_to_file(f"Thank you for participating in the spelling bee, {user.name} has won this spelling bee with a total score of {score}. Congratulations! ", "resources/fake_finish.mp3")
                            engine.runAndWait()

                            await asyncio.sleep(7)
                            voice.play(discord.FFmpegPCMAudio("resources/fake_finish.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe"))
                            voice.source = discord.PCMVolumeTransformer(voice.source)
                            voice.source.volume = 0.25
                            await asyncio.sleep(10)
                            await voice.disconnect()

#other ideas: Would you Rather, Truth Or Dare, adventure type game

    
def setup(bot):
    bot.add_cog(Bee(bot))
