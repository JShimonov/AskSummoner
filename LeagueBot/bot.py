# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    # if message.author == client.user:
    #     return

    league_status = '-lol'
    if message.content == '-lol':
        await message.channel.send(league_status)

client.run(TOKEN)






#import discord
#from discord.ext import commands

#client = commands.Bot(command_prefix = '.')

#@client.event
#async def on_ready():
#    print('Bot is ready.')

#client.run('NzIwMzEzMjc5MjcyMTg5OTk0.XuEKEg.grW84D7twqQh25qIiqti7UWNS0w')
#NzIwMzEzMjc5MjcyMTg5OTk0.XuEKEg.grW84D7twqQh25qIiqti7UWNS0w
