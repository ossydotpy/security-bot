import discord
from discord.ext import commands
from discord.ui import View
from components import  VerifyButton
import re
import json


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_channel = None
        self.load_verification_channels()

    def load_verification_channels(self):
        try:
            with open("verification_channels.json", "r") as f:
                self.verification_channel = json.load(f)
        except FileNotFoundError:
            self.verification_channel = {}

    def save_verification_channels(self):
        with open("verification_channels.json", "w") as f:
            json.dump(self.verification_channel, f, indent=4)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_verification_channel(self, ctx, channel: discord.TextChannel):
        """Set the verification channel"""

        guild_id = str(ctx.guild.id)
        self.verification_channel[guild_id] = channel.id
        self.save_verification_channels()
        await ctx.reply(f"Verification channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def check_verification_channel(self, ctx):
        """Check the currently set verification channel."""
        guild_id = str(ctx.guild.id)
        if guild_id in self.verification_channel:
            channel_id = self.verification_channel[guild_id]
            channel = self.bot.get_channel(channel_id)
            if channel:
                await ctx.send(f"Verification channel is set to {channel.mention}")
                return
        await ctx.send("No Verification channel has been set yet.")

    # verify command
    @commands.command()
    async def verify(self, ctx):
        """show the verify button"""
        guild_id = str(ctx.guild.id)
        if guild_id in self.verification_channel:
            channel_id = self.verification_channel[guild_id]
            channel = self.bot.get_channel(channel_id)
            if channel and ctx.channel == channel:
                button = VerifyButton("Verify")
                embed = discord.Embed(
                    title="Begin Verification",
                    description="click the button below to gain access to the server commands",
                )
                view = View()
                view.add_item(button)
                await ctx.reply(embed=embed, view=view)
                return
            else:
                await ctx.reply(f"This command can only be executed in {self.verification_channel.mention}.")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def add_secret(self, ctx, secret: str):
        if re.match("^[A-Z]+$",secret):
            with open("secrets.txt","a") as f:
                f.writelines(secret.strip())
            await ctx.reply("new secret added")
        else:
            await ctx.reply("invalid secret format")


async def setup(bot):
    await bot.add_cog(Verify(bot))
