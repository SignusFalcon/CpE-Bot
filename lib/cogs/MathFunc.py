from discord.ext.commands import Cog
from discord.ext.commands import command
from ..ext.rootExtractor import extract_root


class MathFunc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["roots", "root"])
    async def extract(self, ctx, arg):
        print(f"{ctx.message.author} used the extract command: {ctx.message}")
        await ctx.send(f'The roots of: {arg}')
        for x in range(len(roots := extract_root(str(arg)))):
            await ctx.send(f'x{x + 1} = {roots[x]}')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("MathFunc")


def setup(bot):
    bot.add_cog(MathFunc(bot))

    # If you want to add a scheduled cog method execution:
    # bot.scheduler.add_job()
