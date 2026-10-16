import discord
from discord import app_commands
from discord.ext import tasks, commands
from discord.ui import View, Button
from roblox import Client
import discord.mentions

import datetime
import json
import logging
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
LOGGING_CHANNEL = os.getenv("LOGGING_CHANNEL")
# Start functions

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
    send_log(bot, f"Bot is online! Ping: {latency}ms", "Bot Status", LOGGING_CHANNEL, discord.Color.green())



async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

discord.utils.setup_logging()
asyncio.run(main())