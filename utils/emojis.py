import os

import discord


class Emojis:
    pass


async def upload(bot: discord.Client, name: str, path: str):
    with open(path, "rb") as f:
        return await bot.create_application_emoji(name=name, image=f.read())


async def load(bot: discord.Client):
    for emoji in await bot.fetch_application_emojis():
        if hasattr(Emojis, emoji.name):
            setattr(Emojis, emoji.name, str(emoji))


async def uploadAll(bot: discord.Client, folder: str = "emojis"):
    existing = {e.name for e in await bot.fetch_application_emojis()}

    for filename in os.listdir(folder):
        name, ext = os.path.splitext(filename)

        if ext.lower() not in (".png", ".gif", ".jpg", ".jpeg"):
            continue

        if name in existing:
            continue

        await upload(bot, name, os.path.join(folder, filename))

    await load(bot)