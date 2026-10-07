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

class General(commands.GroupCog, name="general"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    General = app_commands.Group(

    )

    @commands.hybrid_command(name="help", description="Get help relating to the bot's features")
    async def help(self, ctx: commands.Context):
        await ctx.send(View=helpView)



async def setup(bot):
    await bot.add_cog(General(bot))