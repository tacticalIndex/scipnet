import discord
from discord import app_commands
from discord.ext import tasks, commands
from discord.ui import View, Button
from roblox import Client
import discord.mentions

import datetime
import json
import logging
import logging.handlers
import time
from dataclasses import MISSING
import re
from collections import defaultdict
import os
import asyncio
import requests
import logging
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pathlib import Path
from utils.globalLogging import send_log

#from hosting import keep_alive

import aiohttp
from pkgutil import iter_modules
from collections import defaultdict
import jishaku
from utils.mongo import PreferencesManager

#Bot start up!!!
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DB_URI = os.getenv("MONGODB_URI")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=":", intents=intents)
logging_channel = 1440554108502151329
LOGFILE = os.getenv("LOGFILE")
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logger.getLogger("discord.http").setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename=LOGFILE,
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Keep up to 5 log files
)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
handler.setFormatter(formatter)
logger.addHandler(handler)



async def load_extensions():
    """Scans cogs and loads the modules"""
    cogs_dir = Path(__file__).parent / "cogs"

    try:
        await bot.load_extension("jishaku")
        print("Jishaku loaded")
    except Exception as e:
        print(f"Failed to load Jishaku")

    for file in cogs_dir.rglob("*.py"):
        if file.name in {"__init__.py", "globalLogging.py"}:
            continue

        cog_name = ".".join(file.relative_to(cogs_dir.parent).with_suffix("").parts)
        try:
            await bot.load_extension(cog_name)
            print(f"Successfully loaded cog: {cog_name}")
        except Exception as e:
            print(f"Failed to load cog: {cog_name} ({e})")

@bot.event
async def on_ready():
    latency = round(bot.latency * 1000)
    print(f"Logged in as {bot.user} (ID: {bot.user.id} | Ping: {latency}ms)")
    send_log(bot, "Bot Status", f"Bot is online! Ping: {latency}ms", LOGGING_CHANNEL, discord.Color.green())



async def main():
    async with bot:
        await load_extensions()
        await bot.run(TOKEN, reconnect=True, log_handler=None)



async def sendLogMessage(bot: commands.Bot, message: str, title: str):
    
    """Sends a log message to the specified logging channel.

    Parameters:
        bot (commands.Bot): The discord bot instance.
        message (str): The log message to send.
        title (str): The title of the log message."""
    
    try:
        channel = bot.get_channel(logging_channel)
        if not channel:
            channel = bot.fetch_channel(logging_channel)

        if channel:
            embed = discord.Embed(
                title=title,
                description=message,
                color=discord.Color.yellow()
            )
            embed.set_footer(text="Log Message")
            await channel.send(embed=embed)
        else:
            print(f"Logging channel not found. ({logging_channel})")
    except Exception as e:
        print(f"❌ Error sending message to channel ({logging_channel}). `{e}`")

discord.utils.setup_logging()
asyncio.run(main())