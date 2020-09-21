from discord.ext.commands import Cog
from discord.ext.commands import command
import random as rand


class GenFunc(Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @command()
    async def randchoose(self, ctx):
        print(f"{ctx.message.author} used the randchoose command in {ctx.guild.name}")
        user = rand.choice(ctx.channel.members)
        await ctx.send(f'I choose {user.mention}')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("GenFunc")


def setup(bot):
    bot.add_cog(GenFunc(bot))
