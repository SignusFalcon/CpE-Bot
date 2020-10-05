from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import Greedy
from discord import Member
from discord.ext.commands import BadArgument
from typing import Optional
import random as rand


class GenFunc(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.greetings = ["hi", "uwu hi", "im shy :<", "henlo"]

    @command(name="hello", aliases=["hi"])
    async def send_hello(self, ctx):
        await ctx.send(f"{rand.choice(self.greetings)} {ctx.author.mention}!")

    @command()
    async def ping(self, ctx):
        print(f"{ctx.message.author} used the ping command")
        await ctx.send(f'{round(self.bot.latency, 3) * 100}ms')
        print(f'{ctx.message.author} was pinged.')

    @command()
    async def roles(self, ctx):
        print(f"{ctx.message.author} used the roles command")
        await ctx.send("You have the following roles")
        for role in ctx.message.author.roles:
            if str(role.name) == "@everyone":
                continue
            await ctx.send(role.name)

    # ===================== SLAP COMMAND ====================

    @command(name="slap", aliases=["hit"])
    async def slap(self, ctx, member: Greedy[Member], *, reason: Optional[str] = "no reason"):
        await ctx.message.delete()
        print(f"{ctx.message.author} used the slap command in {ctx.guild.name}")
        if not member:
            rand_user = rand.choice(ctx.channel.members)
            await ctx.send(f'{ctx.message.author.mention} slaps the life out of {rand_user.mention} for '
                           f'{reason}')
        else:
            await ctx.send(f'{ctx.message.author.mention} slaps the life out of {" and ".join([user.mention for user in member])} for '
                       f'{reason}!')

    @slap.error
    async def slap_error(self, ctx, exc):
        if isintance(exc.original, BadArgument):
            await ctx.send("You need to mention at least one person!")

    # ===================== ============ ====================
    # ===================== CHOOSE COMMAND ==================

    @command(name="choose")
    async def random_mention(self, ctx):
        print(f"{ctx.message.author} used to choose command in {ctx.guild.name}")
        user = rand.choice(ctx.channel.members)
        await ctx.send(f"I choose {user.mention}")

    @command(name="echo", aliases=["say"])
    async def echo(self, ctx, *, message):
        print(f"{ctx.message.author} used the echo command in {ctx.guild.name}")
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("GenFunc")


def setup(bot):
    bot.add_cog(GenFunc(bot))
