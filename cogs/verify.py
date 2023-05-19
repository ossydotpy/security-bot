import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
from components import VerificationModal, VerifyButton


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # verify command
    @commands.command()
    async def verify(self, ctx):
        button = VerifyButton("Verify")
        embed = discord.Embed(
            title="Begin Verification",
            description="clicke the button below to gain access to the server commands",
        )
        view = View()
        view.add_item(button)
        await ctx.reply(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
