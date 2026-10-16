import discord


def send_log(bot, title: str, description: str, channel_link: str = "https://discord.com/channels/1180631112251351161/1440554108502151329", color: discord.Color = discord.Color.blue()):
    """
        Sends a message to a specified Discord channel using an embed.

        param bot: Bot instance, (discord.Client or commands.Bot)
        param title: Title of the embed message
        param description: Description of the embed message
        param channel_link: Link to the Discord channel where the message will be sent
        param color: Color of the embed message (default: discord.Color.blue())
    """
    
    # Extract the channel ID from the channel link
    channel_id = int(channel_link.split("/")[-1])
    server_id = int(channel_link.split("/")[-2])

    if channel_id is None or server_id is None:
        raise ValueError("Invalid channel link provided.")

    channel = bot.get_guild(server_id).get_channel(channel_id)

    if channel is None:
        raise ValueError("Channel not found. Please check the channel link.")

    # Create an embed message
    embed = discord.Embed(title=title, description=description, color=color)

    # Send the embed message to the specified channel
    bot.loop.create_task(channel.send(embed=embed))

    return f"Message sent to channel: {channel.name} in server: {channel.guild.name}"

