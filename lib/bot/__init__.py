from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os

from ..db import db

load_dotenv()

PREFIX = "c!"
OWNER_IDS = [213930257684758528]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded.")

        print("Setup complete!")

    def run(self, version):
        self.VERSION = version
        self.TOKEN = os.getenv('DISCORD_TOKEN')

        print("Running setup...")
        self.setup()

        print("Bot running...")
        super().run(self.TOKEN, reconnect=True)

    async def timed_message(self):
        await self.channel.send("I am a timed notification.")

    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        if not self.ready:
            # Guild and channel setup :>
            self.guild = self.get_guild(757241489125539880)
            self.channel = self.get_channel(757246258766282762)

            self.scheduler.add_job(self.timed_message, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            await self.channel.send("Connected to this server.")

            #embed = Embed(title="Now online in " + str(self.guild.name),
            #              description="Do c!help for more information.",
            #              colour=0x00FF00,
            #              timestamp=datetime.utcnow())
            #
            #fields = [("TestBot", "Value", False),
            #          ("Another field", "This field is next to the other one", False),
            #          ("A non-inline field", "This field will appear on it's own row", False),
            #          ("Name", "Field", False)]
            #
            #for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            #
            #embed.set_author(name="TestBot", icon_url=self.guild.icon_url)
            #embed.set_footer(text="TestBot here to serve since 2020.")
            #embed.set_thumbnail(url=self.guild.icon_url)
            #embed.set_image(url=self.guild.icon_url)
            #await channel.send(embed=embed)
            #await channel.send(file=File("./data/images/side meme 1.jpg"))

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("Bot ready")

        else:
            print("Bot reconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.channel.send("An error occured.")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Wrong command! Do c!help for more info.")
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()
