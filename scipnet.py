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
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import tasks, commands
from discord.ui import View, Button
from roblox import Client
import discord.mentions
from pymongo import MongoClient
#from hosting import keep_alive

import aiohttp
from pkgutil import iter_modules
from collections import defaultdict
import jishaku
from utils.mongo import PreferencesManager

#Bot start up!!!
load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=":", intents=intents)
logging_channel = 1440554108502151329

# Start functions

async def sendLogMessage(bot: commands.Bot, message: str, title: str):
    """
    Sends a log message to the specified logging channel.

    Parameters:
        bot (commands.Bot): The discord bot instance.
        message (str): The log message to send.
        title (str): The title of the log message.
    """
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
            await bot.load_extension("jishaku") # Load jishaku extension
            print("Jishaku loaded.")
        else:
            print(f"Logging channel not found. ({logging_channel})")
    except Exception as e:
        print(f"❌ Error sending message to channel ({logging_channel}). `{e}`")
    await bot.tree.sync()

@bot.event
async def on_command(ctx):
    if ctx.cog and ctx.cog.qualified_name == "Jishaku":
        log_message = f"Jishaku command used by {ctx.author} ({ctx.author.id}) in {ctx.guild} ({ctx.guild.id})"
        sendLogMessage(bot, log_message, "Jishaku Command Used")

@bot.event
async def on_message_delete(message): # Placeholder to notify owner when a user deletes a log message.
    guild = message.guild
    channel = message.channel
    embeds = message.embeds
    author = message.author
    if guild == 1180631112251351161 and channel == 1440554108502151329:
        if embeds.footer and embeds.footer.text == "Log Message":
            embed = discord.Embed(
                title="Member Deleted Log Message",
                description=f"Member, {author} ({author.id}), deleted a Log Message in {channel.jump_url}. Attention is advised."
            )
            embed.set_footer(text="Anti-Nuke System")
            guild.owner.send(embed=embed)
            sendLogMessage(bot, f"Log Message deleted by {author} ({author.id}), Authorized Administrators have been notified.", "Member Deleted Log Message")

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

@bot.hybrid_command(name="ping", description="Check the bot's latency")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! `{latency}ms`")

@bot.hybrid_command(name="info", description="Learn information about the bot.")
async def info(ctx):
    class MyView(View):
        def __init__(self):
            super().__init__(timeout=None)  # No timeout
        @discord.ui.button(label="Website", url="https://scipnet.xyz", style=discord.ButtonStyle.link)
        async def website_button(self, interaction: discord.Interaction, button: Button):
            pass  # Link buttons do not need a callback
        @discord.ui.button(label="Support Server", url="https://discord.gg/scipnet", style=discord.ButtonStyle.link)
        async def support_button(self, interaction: discord.Interaction, button: Button):
            pass  # Link buttons do not need a callback
        
    embed = discord.Embed(
        title="**SCiPNET Help**",
        description="Here is some information about the bot:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Prefix", value="The bot's prefix is `:`", inline=False)
    embed.add_field(name="Commands", value="Use `/` to see the list of slash commands available.", inline=False)
    embed.set_footer(text="SCiPNET | Secure Containment Internet Protocol Network")
    await ctx.send(embed=embed, view=MyView) # Placeholder for future views

@tasks.loop(minutes=1)
async def potaNotify(bot):
    try:
        r = requests.get("https://api.pota.app/spot/activator")
        data = r.json()
        spots = []
        fields = []
        
        for spot in data:
            frequency = spot["frequency"]
            ping = True if frequency >= 28000 and frequency <= 28500 else False
            if "US" in spot["reference"]:
                spots.append(spot)
        if spots:
            channel = bot.get_channel(1440554108502151329)
            for spot in spots:
                if spot["reference"] and spot["frequency"] and spot["mode"]:
                    fields.append(f"**Reference:** {spot['reference']}\n**Frequency:** {spot['frequency']} kHz\n**Mode:** {spot['mode']}")
            embed = discord.Embed(
                title="POTA Activator Spots Detected",
                description="\n\n".join(fields),
                color=discord.Color.orange()
            )
            embed.set_footer(text="Data provided by POTA API")
            if ping == True:
                await channel.send(content=f"<@${bot.owner_id}>", embed=embed)
            elif ping == False:
                await channel.send(embed=embed)
    except Exception as e:
        print(f"Error fetching POTA data: {e}")


            

bot.run(token)