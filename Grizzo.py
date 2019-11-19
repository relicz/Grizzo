import discord
import random
import time
import praw
import config
import util
import asyncio

from discord.ext import commands
from discord.utils import get

PREFIX = '!'

COOLDOWN = 10  # In seconds

cooldown_start = time.time()

bot = commands.Bot(command_prefix=PREFIX)

#reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)


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

@bot.command()
async def h(ctx):
    await ctx.send(util.cmd_help(ctx))
    pass


#@client.event
#async def on_message(message):
    # we do not want the bot to reply to itself
    #if message.author == client.user:
      #  return

   # if message.content == PREFIX + 'test':
       # await message.channel.send('test post')

    #if message.content == PREFIX + 'meme':
     #   post = sub.random()
      #  await message.channel.send(post.url, post.permalink)

 #   if message.content.startswith(util.ROLL_COMMAND):
      #  await message.channel.send(util.dice_roller(message))

   # if message.content.startswith(util.TEST_COMMAND):
       # await message.channel.send(util.test(message))

  #  if message.content.startswith(util.MEME_COMMAND):
      #  await message.channel.send(util.meme(message))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(config.TOKEN)
