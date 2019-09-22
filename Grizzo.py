import discord
import random
import time
import config

from discord.ext import commands

PREFIX = '!'

COOLDOWN = 10  # In seconds

cooldown_start = time.time()

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content == PREFIX + 'test':
        await message.channel.send('test post')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


#def shutdown():
 #   client.close()
  #  print("Logged out")

#try:
     #client.loop.create_task(update_window())

client.run(config.TOKEN)
#except:
    #shutdown()

#try:
    # client.loop.create_task(update_window())

client.run(TOKEN)
#except:
   # shutdown()
