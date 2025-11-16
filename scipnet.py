import datetime
import json
import logging
import time
from dataclasses import MISSING
import re
from collections import defaultdict
import os
import asyncio

from discord import app_commands
from discord.ext import tasks, commands
from roblox import Client
import discord.mentions

import aiohttp
from pkgutil import iter_modules
from collections import defaultdict

roblox = Client()

async def main(uid):
    user = await roblox.get_user(uid)
    print("Name", user.name)
    print("Display Name:", user.display_name)
    print("Description:", user.description)


asyncio.get_event_loop().run_until_complete(main())

class Bot(commands.AutoShardedBot):
    time.sleep(3)

def run():
    print("test")

main(5256141118)