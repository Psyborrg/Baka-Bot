import asyncio
import time

import discord
from discord.ext import commands

from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

# List variable to hold the player objects for music
music_queue = []

class Music(commands.Cog, description="music"):

    def __init__(self, bot):
        self.bot = bot

    #Leave command to have the bot disconnect from the channel
    @commands.command(name='leave', help='Disconnect the bot from its current voice channel')
    async def leave(self, ctx):
        #If the bot is in a voice channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Bye Bye!")
        #If not in a voice channel
        else:
            await ctx.send("I'm not in a voice channel silly!")

    # # Suppress noise about console usage from errors
    # youtube_dl.utils.bug_reports_message = lambda: ''


    @commands.command(name='stop', help='stops the music')
    async def stop(self, ctx):

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        await ctx.send('stopped the music')

    @commands.command()
    async def play(self, ctx, url : str):
        
        if ctx.voice_client is None:
            if ctx.author.voice:
                #Connect to the message author's voice channel
                channel = ctx.message.author.voice.channel
                await channel.connect()
            else:
                await ctx.send("I'm not sure which channel to join. Do you think you could join a voice channel for me?")

        with YoutubeDL(ytdl_format_options) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']

        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(FFmpegPCMAudio(URL, **ffmpeg_options), after=lambda x: self.play_next(ctx))
            ctx.voice_client.is_playing()
            await ctx.send(f"Playing: {info['title']}")
            print(f"playing {info['title']}")
        else:
            music_queue.append(URL)
            await ctx.send(f"Added {info['title']} to the queue")
            print(f"Added {info['title']} to the queue")

    def play_next(self, ctx):
        
        # wait until there is nothing playing
        while ctx.voice_client.is_playing():
            print("I'm playing right now, stop it")
            time.sleep(2)

        # If there is a song in the queue, get it and then pop it from the queue
        if (len(music_queue) >= 1):
            url = music_queue[0]
            music_queue.pop(0)

            # Play the popped player, and then repeat this function after the source has ended
            with YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            ctx.voice_client.play(FFmpegPCMAudio(URL, **ffmpeg_options), after=lambda x: self.play_next(ctx))
            ctx.voice_client.is_playing()
            asyncio.run_coroutine_threadsafe(ctx.send(f"playing {info['title']}"), self.bot.loop)
            print(f"playing {info['title']}")
        
        else:
            asyncio.run_coroutine_threadsafe(ctx.send("No more songs in the queue"), self.bot.loop)
            time.sleep(5)
            asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), self.bot.loop)