from discord.ext.commands import Cog
from discord.ext.commands import command
import random as rand
from ..ext.rootExtractor import extract_root


class MathFunc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="extract", aliases=["roots", "root"])
    async def extract(self, ctx, arg):
        print(f"{ctx.message.author} used the extract command: {ctx.message.content}")
        await ctx.send(f'The roots of: {arg}')
        for x in range(len(roots := extract_root(str(arg)))):
            await ctx.send(f'x{x + 1} = {roots[x]}')

    @command(name="dice", aliases=["roll"], ignore_extra=False)
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 25:
            rolls = [rand.randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(digit) for digit in rolls]) + f" = {sum(rolls)}")
        else:
            await ctx.send("I can't roll that many dice. Please try lower or equal than 25")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("MathFunc")


def setup(bot):
    bot.add_cog(MathFunc(bot))

    # If you want to add a scheduled cog method execution:
    # bot.scheduler.add_job()
