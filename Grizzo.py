import discord
import random
import time
import praw
import config
import util
import music
import youtube_dl
import os


from discord.ext import commands
from discord.utils import get

PREFIX = '!'

COOLDOWN = 10  # In seconds

cooldown_start = time.time()

bot = commands.Bot(command_prefix=PREFIX)

#reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)

voice = None


@bot.command(brief='Sends a test message to a server')
async def test(ctx):
    await ctx.send(util.test(ctx))
    pass


@bot.command(aliases=['r'], brief='Rolls dice of variable number of sides', description='Arguments: XdY. X = # of dice,'
                                                                                        ' Y = # or sides per die.\n'
                                                                                        'Function: rolls dice of '
                                                                                        'variable side lengths.')
async def roll(ctx, arg):
    await ctx.send(util.dice_roller(ctx, arg))
    pass


@bot.command(brief='Sends a random meme from reddit', description='Arguments: None.\nFunction: Posts a meme from'
                                                                  ' Redit.')
async def meme(ctx):
    await ctx.send(util.meme(ctx))
    pass


@bot.command(aliases=['j'], brief='Joins the users current voice channel', description='Arguments: None.\nFunction:'
                                                                                       ' Joins current voice channel of'
                                                                                       ' the author of the command.')
async def join(ctx):
    global voice
    if ctx.author.voice:
        v_channel = ctx.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(v_channel)
        else:
            voice = await v_channel.connect()

    else:
        await ctx.send("Please enter a voice channel before requesting Grizzo to join.")
    pass


@bot.command(aliases=['d'], brief='Disconnects from current voice channel', description='Arguments: None.\n'
                                                                                        'Function: Disconnects from '
                                                                                        'voice.')
async def disconnect(ctx):
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Grizzo is not connected to a voice channel.")
    pass


@bot.command(aliases=['yt', 'y'], brief='Plays audio from a YouTube video', description='Arguments: Youtube search '
                                                                                        'query.\nFunction: Plays '
                                                                                        'audio to a voice channel from '
                                                                                        'a YouTube video')
async def youtube(ctx, *args):
    global voice

    if ctx.author.voice:  # If grizzo is not in a voice channel, auto join the one the user is in.
        v_channel = ctx.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(v_channel)
        else:
            voice = await v_channel.connect()

    else:
        await ctx.send("Please enter a voice channel before requesting Grizzo to play a song.")

    url = music.search(args)

    song_there = os.path.isfile("song.mp3")  # checks if a song file is present
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Preparing request")

    voice = get(bot.voice_clients, guild=ctx.guild)

    with youtube_dl.YoutubeDL(music.ydl_opts) as ydl:
        ydl.download([url])

    name = music.rename(ctx)

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.35

    cut = name.index(music.vid_id)
    name = name[:(cut-1)]
    await ctx.send(f"Now playing: ***{name}***")
    pass


@bot.command(brief='Pauses current audio source', description='Arguments: None.\nFunction: Pauses current audio '
                                                              'source.')
async def pause(ctx):
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    pass


@bot.command(brief='Resumes current audio source if paused', description='Arguments: None.\nFunction: Resumes '
                                                                         'current audio source if paused.')
async def play(ctx):
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    pass


@bot.command(brief='Stops audio source', description='Arguments: None.\nFunction: Stops current audio source.')
async def stop(ctx):
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    pass


@bot.command(aliases=['v'], brief='Changes audio volume', description='Arguments: Number between 0 and 1.\n'
                                                                      'Function: Changes bot audio volume.')
async def volume(ctx, arg: float):
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.source.volume = arg
    pass


@bot.command()
async def h(ctx):
    prefix = "Command Prefix: " + PREFIX
    await ctx.send(util.cmd_help(prefix))
    pass


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(config.TOKEN)
