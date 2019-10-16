import discord
import random
import time
import praw
import config
import util

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


@bot.command()
async def roll(ctx, arg):
    await ctx.send(util.dice_roller(ctx, arg))
    pass


@bot.command()
async def meme(ctx):
    await ctx.send(util.meme(ctx))
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
