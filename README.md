# Various Media Editing Features

This bot is mainly focused around memes and a game that is present in it. There are 3 main features of this bot and they are the Spelling Bee Game, a deepfake meme generator, and a Youtube Video Compiler. 

The Spelling Bee Game is just as it sounds. It plays the word you need to spell into a discord voice channel and you are required to spell the word correctly. The score is kept and mentioned to the player after every point. 

The Deep Fake Meme Generator uses the First Order Motion Model from https://github.com/AliaksandrSiarohin/first-order-model with minor modifications to allow it to work with only a CPU and without a Graphics Processor with CUDA cores (This modification is necessary so that the bot can run on a VPS which is more affordable as a VPS with a graphics card generally costs more. This benefit in price does affect the performance significantly as a CPU is much less effective at processing the deepfakes). The deepfake meme generator essentially takes an image that the user inputs and turns it into a deepfake meme. 

The Youtube Compiler Bot is a very useful tool for video editors who edit videos for youtube videos. The Compiler goes through Youtube videos and downloads portions of them and then clips them together into one video. This is useful for video editors who are looking to generate some background footage for a video. It also significantly saves time as it is completely automated and allows the editor to do other tasks while the video is being generated. 
