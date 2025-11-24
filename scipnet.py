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

import discord
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
                color=discord.Color.green()
            )
            embed.set_footer(text="Ping: {}".format(latency))
            await channel.send(embed=embed)
        else:
            print(f"Logging channel not found. ({logging_channel})")
    except Exception as e:
        print(f"❌ Error sending message to channel ({logging_channel}). `{e}`")
    await bot.tree.sync()

@bot.tree.command(name="testing", description="Obvious what this does 🙄")
async def testing(interaction: discord.Interaction):
    res = interaction.response
    await res.send_message("PLEASE WORK")


@bot.hybrid_command(name="maybetesting")
async def maybetesting(ctx, member: discord.Member):
    if member is None:
        ctx.send("Please mention a member.")
    embed = discord.Embed(
        title="**Testing!!!**",
        color=discord.Color.green()
    )
    embed.set_footer(text="This is a footer")
    embed.set_author(name="This is an author line")
    await ctx.send(embed=embed)

@bot.hybrid_command(name="dm", description="Sends a DM to a user")
async def dm(ctx, member: discord.Member, *, message: str):
    try:
        await member.send(message)
        dm_message = await ctx.send(f"DM sent to {member.display_name} successfully!")
        messageId = dm_message.id

        await ctx.send(f"The message ID was: `{messageId}`")
    except discord.Forbidden:
        await ctx.send(f"I cannot send a DM to {member.display_name}: they might have DMs disabled.")
    
@bot.hybrid_command(name="message_react", description="Add a reaction to a message")
async def message_react(ctx, channelid: str, messageid: str, reaction: str):
    try:
        channel = await bot.fetch_channel(channelid)
        if not isinstance(channel, discord.TextChannel):
            await ctx.send("Thats not a text channel!")
            return
        
        message = channel.fetch_message(messageid)
        await message.add_reaction(reaction)
        ctx.send("Reaction added.")

    except discord.Forbidden:
        await ctx.send("I cannot add reactions within that channel.")
    except discord.NotFound:
        await ctx.send("Message/Channel Not Found. Double-check the IDs used.")
    except Exception as e:
        await ctx.send(f"Error occured. `{e}`")
#keep_alive()
bot.run(token)