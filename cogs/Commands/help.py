import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import app_commands

class helpView(discord.ui.view):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Website", url="https://scipnet.xyz", style=discord.ButtonStyle.link, disabled=True)
    async def website_button(self, interaction: discord.Interaction, button: Button):
        pass

    @discord.ui.button(label="Support Server", url="https://discord.com/scipnet", style=discord.ButtonStyle.link, disabled=True)
    async def support_server_button(self, interaction: discord.Interaction, button: Button):
        pass

    embed = discord.Embed(
        title="**SCiPNET Help**",
        description="Here is some information about the bot:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Prefix", value="The bot's prefix is `:`", inline=False)
    embed.add_field(name="Commands", value="Use `/` to see the list of slash commands available.", inline=False)
    embed.set_footer(text="SCiPNET | Secure Containment Internet Protocol Network")

class help(commands.GroupCog, name="help"):

    @app_commands.command(name="general", description="View Commands/Documentation")
    async def general_help_command(self, interaction: discord.Interaction):
        await interaction.responce.send_message(
            embed=helpView.embed,
            view=helpView()
        )



async def setup(bot):
    await bot.add_cog(help(bot))