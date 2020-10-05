from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument
from discord.errors import HTTPException, Forbidden
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os

from ..db import db

load_dotenv()

PREFIX = "c-"
OWNER_IDS = [213930257684758528]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


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

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        if not self.ready:
            # add_job function adds a job inside the scheduler
            # self.scheduler.add_job(self.timed_message, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

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

            print("\n======================================\nBot is connected to:")
            for guild in self.guilds:
                print(f"{guild.name} (id: {guild.id} )")

            print("======================================")

        else:
            print("Bot reconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        print("An exception occured somewhere around the code.")
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc, BadArgument):
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")
        elif isinstance(exc.original, HTTPException):
            await ctx.send("Unable to send message.")
        elif isinstance(exc.original, Forbidden):
            await ctx.send("I do not have the permission to do that. Contact the admin for assistance.")
        else:
            raise exc.original

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()
