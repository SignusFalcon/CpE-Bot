from datetime import datetime

from discord.ext.commands import Bot as BotBase
from discord import Embed, file
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os

load_dotenv()

PREFIX = "c!"
OWNER_IDS = [213930257684758528]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def run(self, version):
        self.VERSION = version
        self.TOKEN = os.getenv('DISCORD_TOKEN')

        print("Bot running...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        if not self.ready:
            print("Bot ready")
            self.ready = True
            self.guild = self.get_guild(488183478811230220)

            channel = self.get_channel(757154303755681882)
            await channel.send("Connected to this server.")

            embed = Embed(title="Now online in " + str(self.guild.name),
                          description="Do c!help for more information.",
                          colour=0x00FF00,
                          timestamp=datetime.utcnow())

            fields = [("TestBot", "Value", False),
                      ("Another field", "This field is next to the other one", False),
                      ("A non-inline field", "This field will appear on it's own row", False),
                      ("Name", "Field", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_author(name="TestBot", icon_url=self.guild.icon_url)
            embed.set_footer(text="TestBot here to serve since 2020.")
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)
            await channel.send(file=file("./data/images/"))

        else:
            print("Bot reconnected")

    async def on_message(self, message):
        pass

bot = Bot()
