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

from discord import app_commands
from discord.ext import tasks, commands
from roblox import Client
import discord.mentions
from pymongo import MongoClient
#from hosting import keep_alive

import aiohttp
from pkgutil import iter_modules
from collections import defaultdict

#Bot start up!!!
token = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=":", intents=intents)
logging_channel = 1440554108502151329

@bot.event
async def on_ready():
    latency = round(bot.latency * 1000)
    print(f"Logged in as {bot.user} (ID: {bot.user.id} | Ping: {latency}ms)")
    try:
        channel = bot.get_channel(logging_channel)
        if not channel:
            channel = bot.fetch_channel(logging_channel)
        
        if channel:
            latency = round(bot.latency * 1000)
            embed = discord.Embed(
                title="Bot online",
                footer="Ping: {}".format(latency),
                color=discord.Color.green()
            )
            await channel.send(embed=embed)
        else:
            print(f"Logging channel not found. ({logging_channel})")
    except Exception as e:
        print(f"❌ Error sending message to channel ({logging_channel}). `{e}`")

@bot.tree.command(name="testing", description="Obvious what this does 🙄")
async def testing(interaction: discord.Interaction):
    interaction.response.send_message("PLEASE WORK")

@bot.hybrid_command(name="maybetesting")
async def maybetesting(ctx: commands.Context, member: discord.Member):
    ctx.send("hi")

#keep_alive()
bot.run(token)