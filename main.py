import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional
from discord.ext.commands import Greedy, Context  # or a subclass of yours

import os
from dotenv import load_dotenv
import asyncio
import tracemalloc, logging, logging.handlers
import datetime
from discord import Activity, ActivityType

load_dotenv()

# Get bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Define intents
intents = discord.Intents.all()
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix=".", intents=intents)


# Load cogs on startup
@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(
        activity=Activity(type=ActivityType.watching, name="everything...")
    )
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename[:-3]} loaded successfully.")
            except Exception as e:
                print(f"Error loading {filename}: {e}")


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: Context,
    guilds: Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="waiting")
    await member.add_roles(role)


## error handling for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NotOwner):
        author = ctx.author
        try:
            await author.send(
                "FAFO :imp: \n You don't have permission to use that command."
            )
        except discord.errors.Forbidden:
            await ctx.reply("skill issue")
        await ctx.message.delete()


tracemalloc.start()
timestamp = datetime.datetime.utcnow()


async def main():  # Run the bot
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    await bot.start(TOKEN)


asyncio.run(main())
