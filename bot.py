# bot.py
import os
from lib.ext.rootExtractor import extract_root

import random as rand
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='c!')
debug = False


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
async def debug(ctx, arg):
    if "Iancraft" not in [str(role.name) for role in ctx.message.author.roles]:
        await ctx.send("You do not have the permission to use this command!")
    else:
        if arg == "true":
            await ctx.send("Debug is now turned on")
            debug = True
        if arg == "false":
            debug = False
            await ctx.send("Debug is now turned off")

@client.command()
async def roles(ctx):
    if debug:
        print(f"{ctx.message.author} used the roles command")
    await ctx.send("You have the following roles")
    for role in ctx.message.author.roles:
        if str(role.name) == "@everyone":
            continue
        await ctx.send(role.name)


@client.command()
async def ping(ctx):
    if debug:
        print(f"{ctx.message.author} used the ping command")
    await ctx.send(f'{round(client.latency, 3) * 100}ms')
    print(f'{ctx.message.author} was pinged.')


@client.command()
async def extract(ctx, arg):
    if debug:
        print(f"{ctx.message.author} used the extract command: {ctx.message}")
    await ctx.send(f'The roots of: {arg}')
    for x in range(len(roots := extract_root(str(arg)))):
        await ctx.send(f'x{x+1} = {roots[x]}')


@client.command()
async def randchoose(ctx):
    if debug:
        print(f"{ctx.message.author} used the randchoose command.")
    await ctx.send(f'I choose @{rand.choice(ctx.guild.members)}')


client.run(TOKEN)