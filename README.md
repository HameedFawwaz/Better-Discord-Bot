# A Discord Bot With Fun Features!

This bot is mainly focused on memes and a game that is present in it. There are 3 main features of this bot and they are a Deepfake Meme Generator, a Youtube Video Compiler, and a Spelling Bee Game. This project was finalized in 2021 when I was in Grade 10 and showcases my ability to develop using object-oriented programming in Python as well as my ability to use a various number of libraries in Python.

# Deep Fake Meme Generator

The Deep Fake Meme Geneartor takes a user specified image and turns it into a Deep Faked video of the character/person in the picture singing _Baka Mitai_ which is a very popular song from the Yakuza franchise. The reason I made this was because I saw how popular the meme was back in 2020 and I wanted to make a way to automate it on a platform that many use. 

The Deep Fake Meme Generator uses the First Order Motion Model from https://github.com/AliaksandrSiarohin/first-order-model with minor modifications to allow it to work with only a CPU and without a Graphics Processor with CUDA cores (This modification is necessary so that the bot can run on a VPS which is more affordable as a VPS with a graphics card generally costs more. This benefit in price does affect the performance significantly as a CPU is much less effective at processing the deepfakes). The project also relies on moviepy in order to process the images and videos. 

Here is an example of its output:

https://github.com/HameedFawwaz/Video-Compiler-Bot/assets/55466919/eb890c7a-4381-42c0-b720-a91979ed0071

Things I learned from developing this feature:
 - Object Oriented Programming principles such as classes and abstraction
 - Asynchronous Programming principles
 - Time Complexity

# Youtube Video Compiler

The YouTube Compiler Bot is a handy tool for video editors who edit videos for YouTube videos. The Compiler goes through YouTube videos and downloads portions of them and then clips them together into one video. This is useful for video editors who are looking to generate some background footage for a video. It also significantly saves time as it is completely automated and allows the editor to do other tasks while the video is being generated. 

This feature relies on moviepy, PyTube, google.cloud, and a few other libraries.

Here is an example of its output:

https://github.com/HameedFawwaz/Video-Compiler-Bot/assets/55466919/2e8e9166-c0e5-413b-a719-814fa2655616

Things I learned from developing this feature:
 - How to edit video files with moviepy
 - How to work with google cloud services to store files on their cloud storage
 - Nore Time Complexity
 - More Asynchronous Programming Principles
 - More Object Oriented Programming Principles
 - Database management with sqlite3

# Spelling Bee Game

The Spelling Bee Game is just as it sounds. It plays the word you need to spell into a discord voice channel and you are required to spell the word correctly. The score is kept and mentioned to the player after every point. 

This feature relies on several high-level libraries such as ttsx3 and playsound which are involved with generating text-to-speech prompts and turning them into audio files which are played to the user. 

Things I learned from developing this feature:
 - How to work with text-to-speech
 - How to work with Discord.py elements such as reactions and user messages
 - How to generate randomized speech prompts
 - Database management with sqlite3

# How to Run the Discord Bot

 - Clone the Repository
 - Download the Python packages in requirements.txt with pip
 - Input a Discord Bot Token generated on the Discord Developer Portal (More info here https://www.writebots.com/discord-bot-token/) into main.py at the very bottom
 - Create an invite link for the Discord Bot (More info here https://discordpy.readthedocs.io/en/stable/discord.html) and invite the bot to your server.=
 - run main.py in Python
 - Enter in =help in a channel in your server to see all of the commands
 - Enjoy! :)




