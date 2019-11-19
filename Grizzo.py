import discord
import random
import time
import praw
import config
import util
import music
import youtube_dl
import os
import asyncio

from discord.ext import commands
from discord.utils import get

PREFIX = '!'

COOLDOWN = 10  # In seconds

cooldown_start = time.time()

bot = commands.Bot(command_prefix=PREFIX)

#reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)

voice = None


@bot.command()
async def test(ctx):
    await ctx.send(util.test(ctx))
    pass


@bot.command(aliases=['r'])
async def roll(ctx, arg):
    await ctx.send(util.dice_roller(ctx, arg))
    pass


@bot.command()
async def meme(ctx):
    await ctx.send(util.meme(ctx))
    pass

# new bot command for voting on a post
@bot.command()
async def vote(ctx, question, choices):
    
    choices.strip() # remove leading/trailing spaces from choices
    choices_arr = choices.split(',') # split choices into array
    # emojis : apple, orange, banana, watermelon, grapes, cherries, pineapples
    emojis = ['🍎', '🍊', '🍌', '🍉', '🍇', '🍒', '🍍'] # emojis array to coincide with choices
    # currently max of 7 (might not properly display in your editor)
    
    # create message object and announce the vote
    message = await ctx.send(embed = util.vote_start(question, choices_arr, emojis))
    
    # add reactions
    i = 0
    while i < len(choices_arr): # add each selectable choice through an emoji to click
        await message.add_reaction(emojis[i])
        i += 1
        
    # wait for x seconds
    await asyncio.sleep(15)
    
    # recreate message object with reactions included
    message = await ctx.fetch_message(message.id)
    
    # count reactions and announce winner
    await ctx.send(embed = util.tally_up(question, choices_arr, message))
    pass

# new bot command for pulling messages
@bot.command()
async def pull(ctx, chan = "general", num = 5, hist_num = 100): # context, channel, number of messages, how far the history goes
    # defaults included
    
    # create channel object
    channel = discord.utils.get(ctx.guild.channels,name = chan)
    # create message history
    messages = await channel.history(limit= hist_num).flatten()
    
    message_list = []
    
    i = 0
    while i < len(messages):
        message_list.append(messages[i].content)
        i += 1
    await ctx.send(embed = util.pull(ctx, message_list, num))
    pass

@bot.command(aliases=['j'])
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

@bot.command()
async def npc(ctx):
    await ctx.send(util.npc(ctx))
    pass


@bot.command(aliases=['d'])
async def disconnect(ctx):
    global voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Grizzo is not connected to a voice channel.")
    pass


@bot.command(aliases=['yt', 'y'])
async def youtube(ctx, *args):
    global voice

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


@bot.command(aliases=['v'])
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
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Type !h for help'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(config.TOKEN)
