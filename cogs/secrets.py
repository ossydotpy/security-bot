import re
import discord
from discord.ext import commands
from discord import app_commands

class Secrets(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def add_secret(self, ctx, secret: str):
        if re.match("^[A-Z]+$",secret):
            with open("secrets.txt","a") as f:
                f.write(secret.strip() + "\n")
            await ctx.reply("new secret added")
        else:
            await ctx.reply("invalid secret format")

    @app_commands.command(name="secrets")
    async def secrets(self, interaction: discord.Interaction):
        """list all secret codes"""
        with open("secrets.txt") as f:
            secrets = f.readlines()
        
        secret_embed = discord.Embed(title="Secrets", description="Available Secret Codes.", color=discord.Color.greyple())
        for x in secrets:
            secret_embed.add_field(name="", value= f"{x}\n", inline=False)

        await interaction.response.send_message(content="use any of these codes to access testing channels",embed=secret_embed)

async def setup(bot):
    await bot.add_cog(Secrets(bot))