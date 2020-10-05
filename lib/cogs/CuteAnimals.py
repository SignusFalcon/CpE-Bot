from aiohttp import request
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument
from discord.ext.commands import command
from discord import File, Embed
from discord.ext.commands import BadArgument


class CuteAnimals(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="send")
    async def send_img(self, ctx, animal: str):
        print(f"{ctx.author.name} used the send image command in {ctx.guild.name}")

        animal_dict = {"dog": "https://some-random-api.ml/img/dog",
                       "cat": "https://some-random-api.ml/img/cat",
                       "birb": "https://some-random-api.ml/img/birb",
                       "bird": "https://some-random-api.ml/img/birb",
                       "panda": "https://some-random-api.ml/img/panda",
                       "fox": "https://some-random-api.ml/img/fox"}
        try:
            URL = animal_dict[animal]
        except KeyError:
            await ctx.send("Invalid arguments.")
            raise BadArgument

        async with request("GET", URL, headers={}) as response:
            if response.status == 200: # means its ok
                data = await response.json() # returns a dictionary object, passes it to data

                e = Embed()
                e.set_image(url=data["link"])
                await ctx.send(embed=e)

            else:
                await ctx.send(f"API return a {response.status} status")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("CuteAnimals")


def setup(bot):
    bot.add_cog(CuteAnimals(bot))