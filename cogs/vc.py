import discord
from discord.ext import commands
from discord.utils import get

from youtubesearchpython import VideosSearch
from youtubesearchpython import ResultMode
from youtubesearchpython import ChannelsSearch

from pytube import Playlist
from pytube import YouTube

from moviepy.editor import *

import json
import youtube_dl
import os, re, os.path, sys
import asyncio
import random

import functools

from google.cloud import storage

from utils.baka import Mitai

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.processing_list = []
    
    def cog_check(self, ctx):
        return True



    def compile(self, ctx, time, number, term):
        

        actual_time = int(time.content)

        video = VideosSearch(term.content, limit = int(number.content))

        filename_list = []
        youtube_list = []
        clip_list = []


        for i in range(int(number.content)):

            ydl_opts = {
            'format' : '136',
            'outtmpl': f"/root/vc/video/{str(video.result()['result'][i]['id'])}.mp4",
            'ignoreerrors': True}


            video_link = video.result()['result'][i]['link']

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
            try:
                length = video.result()['result'][i]['duration']

                calculated_length = sum(int(x) * 60 ** i for i, x in enumerate(reversed(length.split(":"))))
                if calculated_length < 1800:
                    stripped_length = calculated_length/2 - actual_time

                    clip = VideoFileClip(f"/root/vc/video/{str(video.result()['result'][i]['id'])}.mp4")
                    clip = clip.subclip(stripped_length, calculated_length/2)
                    clip = clip.crossfadein(1.0)
                    clip = clip.crossfadeout(1.0)
                    clip.write_videofile(filename = f"video/{ctx.author.name}{[i]}.mp4", threads = 64, fps = 30)

                    filename_list.append(clip)
                    clip_list.append(f"video/{ctx.author.name}{[i]}.mp4")
                    youtube_list.append(f"{str(video.result()['result'][i]['id'])}.mp4")
                else:
                    int(number.content) + 1
                    pass
            except Exception as e:
                print(e)
                pass

        else:
            final_clip = concatenate_videoclips(filename_list, method = "compose")
            final_clip.write_videofile(f"video/{ctx.author.id}.mp4", threads = 64, fps = 30)

            client = storage.Client.from_service_account_json(json_credentials_path="/root/vc/config.json")

            bucket = client.get_bucket('compiledvideos')

            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
            send_name.upload_from_filename(f"video/{ctx.author.id}.mp4")

            mypath = "/root/vc/video"
            for root, dirs, files in os.walk(mypath):
                for file in files:
                    if file in youtube_list:
                        os.remove(os.path.join(root, file))
                    elif file in clip_list:
                        os.remove(os.path.join(root, file))

    def alternate_compile(self, ctx, time, number, term):
        actual_time = int(time.content)

        video = VideosSearch(term.content, limit = int(number.content))

        filename_list = []
        youtube_list = []
        clip_list = []


        for i in range(int(number.content)):

            ydl_opts = {
            'format' : '136',
            'outtmpl': f"/root/vc/video/{str(video.result()['result'][i]['id'])}.mp4",
            'ignoreerrors': True}


            video_link = video.result()['result'][i]['link']

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
            try:
                length = video.result()['result'][i]['duration']

                calculated_length = sum(int(x) * 60 ** i for i, x in enumerate(reversed(length.split(":"))))
                if calculated_length > 1800:
                    stripped_length = calculated_length/2 - actual_time

                    clip = VideoFileClip(f"/root/vc/video/{str(video.result()['result'][i]['id'])}.mp4")
                    clip = clip.subclip(stripped_length, calculated_length/2)
                    clip = clip.crossfadein(1.0)
                    clip = clip.crossfadeout(1.0)
                    clip.resize(width = 1280, height = 720)
                    clip.write_videofile(filename = f"video/{ctx.author.name}{[i]}.mp4", threads = 64, fps = 30)

                    filename_list.append(clip)
                    #duration_list.append(clip.duration)

                else:
                    int(number.content) + 1
                    pass

            except Exception as e:
                print(e)
                pass

        else:

            #video_fx_list = [filename_list[0]]
            

            final_clip = concatenate_videoclips(filename_list, method = "compose")
            final_clip.write_videofile(f"video/{ctx.author.name}.mp4", threads = 64, fps = 30)

            client = storage.Client.from_service_account_json(json_credentials_path="/root/vc/config.json")

            bucket = client.get_bucket('compiledvideos')

            blobs = client.list_blobs('compiledvideos')     
    
            
            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
            send_name.upload_from_filename(f"video/{ctx.author.name}.mp4")

            mypath = "/root/vc/video"
            for root, dirs, files in os.walk(mypath):
                for file in files:
                    if file in youtube_list:
                        os.remove(os.path.join(root, file))
                    elif file in clip_list:
                        os.remove(os.path.join(root, file))

    def playlist_compile(self, ctx, time, playlist):
        actual_time = int(time.content)


        playlist = Playlist(playlist_url.content)


        filename_list = []
        clip_list = []


        print(len(playlist))
        
        for video in playlist.videos:

            new_video = video.streams.get_highest_resolution()
            print(new_video)
            new_video.download(output_path = "/root/vc/video", filename=f"{video.length}{video.views}.mp4")


            clip = VideoFileClip(f"/root/vc/video/{video.length}{video.views}mp4.mp4")

            stripped_length = clip.duration/2 - actual_time

            clip = clip.subclip(stripped_length, clip.duration/2)
            clip = clip.crossfadein(1.0)
            clip = clip.crossfadeout(1.0)
            clip.write_videofile(filename = f"video/{ctx.author.name}{video.views}.mp4", threads = 8)

            filename_list.append(clip)

        else:
            final_clip = concatenate_videoclips(filename_list, method = "compose")
            final_clip.write_videofile(f"video/{ctx.author.name}.mp4", threads = 8)

            client = storage.Client.from_service_account_json(json_credentials_path="C:/root/vc/config.json")

            bucket = client.get_bucket('compiledvideos')

            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
            send_name.upload_from_filename(f"video/{ctx.author.name}.mp4")

            mypath = "/root/vc/video"
            for root, dirs, files in os.walk(mypath):
                for file in files:
                    if file in clip_list:
                        os.remove(os.path.join(root, file))

    def link_compile(self, ctx, time, link, clips):
        actual_time = int(time.content)
                        
        ydl_opts = {
            'format' : '136',
            'outtmpl': f"/root/vc/video/{str(video.result()['result'][i]['id'])}.mp4",
            'ignoreerrors': True}


    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("downloading something")
            ydl.download([link.content])
        
        filename_list = []
        youtube_list = []
        clip_list = []

        clip_number = int(clips.content)
        length = VideoFileClip(f"/root/vc/video/{str(ctx.author.id)}.mp4").duration
        calculated_length = length

        for i in range(0, clip_number):
            number = random.randint(0, int(calculated_length))
            stripped_length = number - actual_time

            clip = VideoFileClip(f"/root/vc/video/{str(ctx.author.id)}.mp4")
            clip = clip.subclip(stripped_length, number)
            clip = clip.crossfadein(1.0)
            clip = clip.crossfadeout(1.0)
            clip.write_videofile(filename = f"video/{ctx.author.name}{[i]}.mp4", threads = 8)

            filename_list.append(clip)
        
        else:
            final_clip = concatenate_videoclips(filename_list, method = "compose")
            final_clip.write_videofile(f"video/{ctx.author.name}.mp4", threads = 8)

            client = storage.Client.from_service_account_json(json_credentials_path="/root/vc/config.json")

            bucket = client.get_bucket('compiledvideos')


            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
            send_name.upload_from_filename(f"video/{ctx.author.name}.mp4")


            mypath = "/root/vc/video"
            for root, dirs, files in os.walk(mypath):
                for file in files:
                    if file in youtube_list:
                        os.remove(os.path.join(root, file))
                    elif file in clip_list:
                        os.remove(os.path.join(root, file))

    @commands.command()
    async def create(self, ctx):
        mitai = Mitai()

        track = mitai._get_vc(user_id=ctx.author.id)
        pat, useless = mitai._get_user_info(user_id=ctx.author.id)

        if pat == 1:
        
            embed = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "What would you like to search for? \n\n**Term**\n(As if you were to search something on youtube, can use multiple videos)\n\n**Link**\n(Grab clips from a specific video)\n\n**Playlist**\n(Grab clips from every video in a playlist)")
            await ctx.send(embed=embed)
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            
            type_ = await self.bot.wait_for('message', check=check)
            
            if type_.content.lower() == "term":
                embed1 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Enter in the term that you would like to search")
                
                await ctx.send(embed=embed1)
                term = await self.bot.wait_for('message', check=check)
                if term.content:
                    embed2 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How many videos would you like to go through?")
                    await ctx.send(embed=embed2)
                    number = await self.bot.wait_for('message', check=check)
                    if int(number.content) > 1:
                        embed3 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long of a clip do you want to grab from each video?")
                        await ctx.send(embed=embed3)

                        time = await self.bot.wait_for('message', check=check)

                        if time.content:
                            async with ctx.typing():

                                self.processing_list.append(1)

                                added_time = int(number.content) * int(time.content)
                                rounded_time = round(added_time/60)

                                await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")

                                try:
                                    args = functools.partial(self.compile, ctx, time, number, term)

                                    await self.bot.loop.run_in_executor(None, args)
                                except Exception as e:
                                    print(e)

                                    args = functools.partial(self.alternate_compile, ctx, time, number, term)

                                    await self.bot.loop.run_in_executor(None, args)

                                embed4 = discord.Embed(color = discord.Color.red(), title = "Video Created!")

                                self.processing_list.remove(1)

                            await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")

                            mitai.update_value(user_id=ctx.author.id, column="vtrack", value=1)

                            await asyncio.sleep(86400)
                            bucket = client.get_bucket('compiledvideos')
                            
                            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                            send_name.delete()

                                            

                    elif int(number.content) == 1:
                        embed4 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How many clips do you want to grab from this video?")
                        await ctx.send(embed=embed4)

                        clips = await self.bot.wait_for('message', check=check)
                        if clips:
                            embed5 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long do you want each clip to be?")
                            await ctx.send(embed=embed5)

                            time = await self.bot.wait_for('message', check=check)
                            if time.content:

                                async with ctx.typing():

                                    self.processing_list.append(1)

                                    added_time = int(number.content) * int(time.content)
                                    rounded_time = round(added_time/60)

                                    await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")


                                    args = functools.partial(self.compile, ctx, time, number, term)

                                    try:
                                        await self.bot.loop.run_in_executor(None, args)
                                    except:
                                        args = functools.partial(self.alternate_compile, ctx, time, number, term)

                                        await self.bot.loop.run_in_executor(None, args)
                                        
                                    self.processing_list.remove(1)

                                await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")



                                await asyncio.sleep(86400)
                        
                                send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                                send_name.delete()

                                await ctx.author.send("The video that was created has been deleted")

            elif type_.content.lower() == "playlist":
                embed2 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Enter the URL of the Youtube Playlist")
                await ctx.send(embed=embed2)
                playlist_url = await self.bot.wait_for('message', check=check)

                if playlist_url.content:

                    embed3 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long of a clip do you want to grab from each video?")
                    await ctx.send(embed=embed3)
                    time = await self.bot.wait_for('message', check=check)

                    if int(time.content) > 1:
                        self.processing_list.append(1)

                        async with ctx.typing():
                            added_time = int(number.content) * int(time.content)
                            rounded_time = round(added_time/60)

                            await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")


                            args = functools.partial(self.playlist_compile, ctx, time, playlist)

                            await self.bot.loop.run_in_executor(None, args)

                            self.processing_list.remove(1)

                        await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")


                        await asyncio.sleep(86400)
                            
                        send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                        send_name.delete()

            elif type_.content.lower():
                embed2 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Enter the link that you would like to grab clips from")
                await ctx.send(embed=embed2)
                link = await self.bot.wait_for('message', check=check)

                if link.content:
                    embed4 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How many clips do you want to grab from this video?")
                    await ctx.send(embed=embed4)

                    clips = await self.bot.wait_for('message', check=check)
                    if clips:
                        embed5 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long do you want each clip to be?")
                        await ctx.send(embed=embed5)

                        time = await self.bot.wait_for('message', check=check)
                        if time.content:
                            self.processing_list.append(1)

                            async with ctx.typing():


                                added_time = int(clips.content) * int(time.content)
                                rounded_time = round(added_time/60)

                                await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")


                                args = functools.partial(self.link_compile, ctx, time, link, clips)

                                await self.bot.loop.run_in_executor(None, args)
                                    
                                self.processing_list.remove(1)

                            await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")


                            await asyncio.sleep(86400)
                            
                            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                            send_name.delete() 
        elif track == 0:
            embed = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "What would you like to search for? \n\n**Term**\n(As if you were to search something on youtube, can use multiple videos)\n\n**Link**\n(Grab clips from a specific video)\n\n**Playlist**\n(Grab clips from every video in a playlist)")
            await ctx.send(embed=embed)
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            
            type_ = await self.bot.wait_for('message', check=check)
            
            if type_.content.lower() == "term":
                embed1 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Enter in the term that you would like to search")
                
                await ctx.send(embed=embed1)
                term = await self.bot.wait_for('message', check=check)
                if term.content:
                    embed2 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How many videos would you like to go through?")
                    await ctx.send(embed=embed2)
                    number = await self.bot.wait_for('message', check=check)
                    if int(number.content) >= 10:
                        embed3 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "The amount of videos that you have selected is too high, to get unlimited access to Kiryu, use =patreon. ")
                        await ctx.send(embed=embed3)
                    elif int(number.content) > 1:
                        embed3 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long of a clip do you want to grab from each video?")
                        await ctx.send(embed=embed3)

                        time = await self.bot.wait_for('message', check=check)

                        if time.content:
                            async with ctx.typing():

                                self.processing_list.append(1)

                                added_time = int(number.content) * int(time.content)
                                rounded_time = round(added_time/60)

                                await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")

                                try:
                                    args = functools.partial(self.compile, ctx, time, number, term)

                                    await self.bot.loop.run_in_executor(None, args)
                                except Exception as e:
                                    print(e)

                                    args = functools.partial(self.alternate_compile, ctx, time, number, term)

                                    await self.bot.loop.run_in_executor(None, args)

                                embed4 = discord.Embed(color = discord.Color.red(), title = "Video Created!")

                                self.processing_list.remove(1)

                            await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")

                            mitai.update_value(user_id=ctx.author.id, column="vtrack", value=1)

                            await asyncio.sleep(86400)

                            mitai.update_value(user_id=ctx.author.id, column="vtrack", value=0)
                            bucket = client.get_bucket('compiledvideos')
                            
                            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                            send_name.delete()

                            await ctx.author.send("Your daily cooldown has expired, you may now make another video compilation!")

                                            

                    elif int(number.content) == 1:
                        embed4 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How many clips do you want to grab from this video?")
                        await ctx.send(embed=embed4)

                        clips = await self.bot.wait_for('message', check=check)
                        if clips:
                            embed5 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long do you want each clip to be?")
                            await ctx.send(embed=embed5)

                            time = await self.bot.wait_for('message', check=check)
                            if time.content:

                                async with ctx.typing():

                                    self.processing_list.append(1)

                                    added_time = int(number.content) * int(time.content)
                                    rounded_time = round(added_time/60)

                                    await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")


                                    args = functools.partial(self.compile, ctx, time, number, term)

                                    try:
                                        await self.bot.loop.run_in_executor(None, args)
                                    except:
                                        args = functools.partial(self.alternate_compile, ctx, time, number, term)

                                        await self.bot.loop.run_in_executor(None, args)
                                        
                                    self.processing_list.remove(1)

                                await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")

                                await asyncio.sleep(86400)
                                
                                mitai.update_value(user_id=ctx.author.id, column="vtrack", value=0)
                                send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                                send_name.delete()

                                await ctx.author.send("Your daily cooldown has expired, you may now make another video compilation!")

            elif type_.content.lower() == "playlist":
                embed2 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Enter the URL of the Youtube Playlist")
                await ctx.send(embed=embed2)
                playlist_url = await self.bot.wait_for('message', check=check)

                if playlist_url.content:

                    embed3 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long of a clip do you want to grab from each video?")
                    await ctx.send(embed=embed3)
                    time = await self.bot.wait_for('message', check=check)

                    if int(time.content) > 1:
                        self.processing_list.append(1)

                        async with ctx.typing():
                            added_time = int(number.content) * int(time.content)
                            rounded_time = round(added_time/60)

                            await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")


                            args = functools.partial(self.playlist_compile, ctx, time, playlist)

                            await self.bot.loop.run_in_executor(None, args)

                            self.processing_list.remove(1)

                        await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")


                        await asyncio.sleep(86400)
                            
                        mitai.update_value(user_id=ctx.author.id, column="vtrack", value=0)
                        send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                        send_name.delete()

                        await ctx.author.send("Your daily cooldown has expired, you may now make another video compilation!")
            
            elif type_.content.lower() == "link":
                embed2 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Enter the link that you would like to grab clips from")
                await ctx.send(embed=embed2)
                link = await self.bot.wait_for('message', check=check)

                if link.content:
                    embed4 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How many clips do you want to grab from this video?")
                    await ctx.send(embed=embed4)

                    clips = await self.bot.wait_for('message', check=check)
                    if clips:
                        embed5 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "How long do you want each clip to be?")
                        await ctx.send(embed=embed5)

                        time = await self.bot.wait_for('message', check=check)
                        if time.content:
                            self.processing_list.append(1)

                            async with ctx.typing():


                                added_time = int(clips.content) * int(time.content)
                                rounded_time = round(added_time/60)

                                await ctx.send(f"Processing your request, there are currently {len(self.processing_list)} videos being processed at the moment.\nIt will take approximately {rounded_time * 3} minutes to process your video")


                                args = functools.partial(self.link_compile, ctx, time, link, clips)

                                await self.bot.loop.run_in_executor(None, args)
                                    
                                self.processing_list.remove(1)

                            await ctx.send(f"Here is the link for the video generated:\nhttps://storage.googleapis.com/compiledvideos/videos/{ctx.message.id}.mp4\nNote: This file will only be available for 24 hours.\n{ctx.author.mention}")


                            await asyncio.sleep(86400)
                            
                            mitai.update_value(user_id=ctx.author.id, column="vtrack", value=0)
                            send_name = bucket.blob(f"videos/{ctx.message.id}.mp4")
                            send_name.delete() 
                            await ctx.author.send("Your daily cooldown has expired, you may now make another video compilation!")

            else:
                embed2 = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Invalid Input")
                await ctx.send(embed = embed2)

        else:
            embed = discord.Embed(color = discord.Color.red(), title="Video Clip Compiler", description = "Unfortunately, you have reached your daily limit for creating video compilations, use =vote to be able to create another compilation or use =patreon to get unlimited access. ")
            await ctx.send(embed=embed)

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)


    @commands.command()
    async def restart(self, ctx):
        if ctx.author.id == 338678933434138634 or ctx.author.id == 609120492984598532:
            await ctx.send("Restarting bot, please allow 5 seconds. ")
            self.restart_program()

def setup(bot):
    bot.add_cog(Main(bot))