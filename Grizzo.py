import discord
import random
import time
import praw
import config
import util
import music
import hangman
import youtube_dl
import os
import asyncio
import games

from discord.ext import commands
from discord.utils import get
from hangman import Hangman

PREFIX = '!'

COOLDOWN = 10  # In seconds

cooldown_start = time.time()

bot = commands.Bot(command_prefix=PREFIX)

# reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)

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
                                                                  ' Reddit.')
async def meme(ctx):
    await ctx.send(util.meme(ctx))
    pass


# new bot command for voting on a post
@bot.command(brief='Creates a vote for a quick straw poll of the chatroom.',
             description='Arguments: "question" "choices" timer. Question and choices must be enclosed in quotation '
                         'marks. Choices must be separated by commas.\nFunction: Creates a vote for a quick straw poll '
                         'of the chatroom, ending after \'timer\' seconds')
async def vote(ctx, question, choices, timer=15):
    choices.strip()  # remove leading/trailing spaces from choices
    choices_arr = choices.split(',')  # split choices into array

    # emojis : apple, orange, banana, watermelon, grapes, cherries, pineapples
    emojis = ['🍎', '🍊', '🍌', '🍉', '🍇', '🍒', '🍍']  # emojis array to coincide with choices
    # currently max of 7 (might not properly display in your editor)

    # create message object and announce the vote
    message = await ctx.send(embed=util.vote_start(question, choices_arr, emojis))

    # add reactions
    i = 0
    while i < len(choices_arr):  # add each selectable choice through an emoji to click
        await message.add_reaction(emojis[i])
        i += 1

    # wait for x seconds
    await asyncio.sleep(timer)

    # recreate message object with reactions included
    message = await ctx.fetch_message(message.id)

    # count reactions and announce winner
    await ctx.send(embed=util.tally_up(question, choices_arr, message))
    pass


# new bot command for pulling messages
@bot.command(brief='Pulls a certain amount of messages from a certain channel',
             description='Arguments: channel, number of messages, history number.\nFunction: Pulls a specified number'
                         ' of messages from a specified channel, as far back as specified.')
async def pull(ctx, chan="general", num=5, hist_num=100):  # context, channel, number of messages, how far the history goes
    # defaults included

    # create channel object
    channel = discord.utils.get(ctx.guild.channels, name=chan)
    # create message history
    messages = await channel.history(limit=hist_num).flatten()

    message_list = []

    i = 0
    while i < len(messages):
        message_list.append(messages[i].content)
        i += 1
    await ctx.send(embed=util.pull(ctx, message_list, num))
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


@bot.command(brief='Random stat generator for an NPC')
async def npc(ctx):
    await ctx.send(util.npc(ctx))
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
    voice = get(bot.voice_clients, guild=ctx.guild)

    if ctx.author.voice:  # If grizzo is not in a voice channel, auto join the one the user is in.
        v_channel = ctx.author.voice.channel

        if voice and voice.is_connected():
            await voice.move_to(v_channel)
        else:
            voice = await v_channel.connect()

    else:
        await ctx.send("Please enter a voice channel before requesting Grizzo to play a song.")
        return

    url = music.search(args)

    song = "song" + str(ctx.guild.id) + ".mp3"

    song_there = os.path.isfile(song)  # checks if a song file is present
    try:
        if song_there:
            os.remove(song)
    except PermissionError:
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Preparing request")

    with youtube_dl.YoutubeDL(music.ydl_opts) as ydl:
        ydl.download([url])

    name = music.rename(ctx, song)

    voice.play(discord.FFmpegPCMAudio(song), after=lambda e: print(f"{name} has finished playing"))
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


@bot.command(brief='Play Blackjack', description='Arguments: Optional timer.\n'
                                                 'Function: Plays a game of Blackjack..')
async def blackjack(ctx, timer = 15): # default timer of 15 seconds
    # initial variables
    player_hand = []
    enemy_hand = []
    game_over = 0 # a while loop for this will allow the player to continuously hit if they're allowed to
    
    # blackjack instance
    BJ = games.Blackjack()
    
    # deal cards
    player_hand = BJ.deal_cards()
    enemy_hand = BJ.deal_cards()
    
    # emojis: white_check_mark, x
    emojis = ['✅', '❌'] # emojis array to coincide with hit or stand
    
    embed_text = discord.Embed(title = "Blackjack") 
    
    # initial message
    if BJ.get_total(player_hand) == 21:
        embed_text.add_field(name = "Status", value = "You've already won with a max hand of " 
                             + str(BJ.get_total(player_hand)) + "!")
        await ctx.send(embed=embed_text)
    elif BJ.get_total(enemy_hand) == 21:
        embed_text.add_field(name = "Status", value = "You've already lost with the dealer having a max hand of " 
                             + str(BJ.get_total(enemy_hand)) + "!")
        await ctx.send(embed=embed_text)
        
    else:
        while game_over == 0: # loop until player reaches 21 or greater, or until player chooses to stand
            message = 0
            embed_text = discord.Embed(title = "Blackjack") 
            
            # prompt for choice
            embed_text.add_field(name = "Status", value = "You have " + str(BJ.get_total(player_hand)) 
                                 + " while the dealer has " + str(BJ.get_total(enemy_hand)) + ". Hit or stand?")
            message = await ctx.send(embed=embed_text)
        
            # add reactions
            i = 0
            while i < len(emojis): # represent hit or stand with emojis
                await message.add_reaction(emojis[i])
                i += 1
                
            # wait for x seconds to allow reactions to come in
            await asyncio.sleep(timer)
            
            # recreate message object with reactions included
            message = await ctx.fetch_message(message.id)
            
            # create initial embed
            embed_text = discord.Embed(title = "Blackjack") 
            
            # if reactions point to hit
            if BJ.hit_or_stand(message) == 1: # hit
                BJ.hit(player_hand)
                
                if BJ.get_total(player_hand) >= 21:
                    game_over = 1
            
            else: # if reactions point to stand
                    
                game_over = 1
        # end while
        
        # dealer's turn
        # while dealer's hand is lower than 15 and dealer's hand is less than player's hand, if player's hand is less than 21
        while (BJ.get_total(enemy_hand) < 15  or BJ.get_total(enemy_hand) < BJ.get_total(player_hand)) and BJ.get_total(player_hand) < 21:
            BJ.hit(enemy_hand)
        
        # win/lose and reason for winning/losing
        final_status = BJ.get_result(player_hand, enemy_hand)
        
        # final message
        embed_text.add_field(name = "Status", value = "You have " + str(BJ.get_total(player_hand)) 
                             + " while the dealer has " + str(BJ.get_total(enemy_hand)) + ". " + final_status)
        await ctx.send(embed = embed_text)
        
    # end else
    pass


@bot.command()
async def h(ctx):
    prefix = "Command Prefix: " + PREFIX
    await ctx.send(util.cmd_help(prefix))
    pass

             
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Type !help for help'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

             
@bot.event
async def hangman(ctx);
        game_message = ""
        if len(args) > 1:
            if args[1] == 'start':
                game.start_game()
                game_message = 'A word has been randomly selected (all lowercase). \nGuess leters by using `!hangman z` (z is the guessed letter). \n'
            else:
                game.guess(message.content)
        await message.channel.send(game_message + game.get_game_status())
    
bot.run(config.TOKEN)
