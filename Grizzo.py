import discord
import random
import time
import token

#from discord.ext import commands

TOKEN = 'token.TOKEN'
PREFIX = '!'

#COOLDOWN = 10  # In seconds

#cooldown_start = time.time()

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content == PREFIX + 'test':
        msg = 'Test post please ignore {0.author.mention}'.format(message)


    await client.send_message(message.channel, msg)

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
    # client.loop.create_task(update_window())

client.run(TOKEN)
#except:
   # shutdown()
