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

#from hosting import keep_alive

import aiohttp
from pkgutil import iter_modules
from collections import defaultdict
import jishaku
from utils.mongo import PreferencesManager

#Bot start up!!!
load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")
db_uri = os.getenv("MONGODB_URI")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=":", intents=intents)
logging_channel = 1440554108502151329
# Start functions



async def load_extensions():
    """Scans cogs and loads the modules"""
    cogs_dir = Path(__file__).parent / "cogs"

    try:
        await bot.load_extension("jishaku")
        print("Jishaku loaded")
    except Exception as e:
        print(f"Failed to load Jishaku")

    for file in cogs_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue

        cog_name = f"cogs.{file.stem}"
        try:
            await bot.load_extension(cog_name)
            print(f"Successfully loaded cog: {cog_name}")
        except Exception as e:
            print(f"Failed to load cog: {cog_name} ({e})")

@bot.event
async def on_ready():
    latency = round(bot.latency * 1000)
    print(f"Logged in as {bot.user} (ID: {bot.user.id} | Ping: {latency}ms)")



async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)



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

asyncio.run(main())