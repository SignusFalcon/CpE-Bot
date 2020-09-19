# bot.py
import os
from rootExtractor import extract_root

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='c!')


@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guild:')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')


    """
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    """


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server with your bot!')


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server with your bot!')


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency, 3) * 100}ms')
    print(f'{ctx.message.author} was pinged.')


@client.command()
async def extract(ctx, arg):
    await ctx.send(f'The roots of: {arg}')
    roots = extract_root(str(arg))
    for x in range(len(roots)):
        await ctx.send(f'x{x+1} = {roots[x]}')


client.run(TOKEN)