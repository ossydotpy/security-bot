from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension: str):
        """load cogs"""
        try:
            await self.bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded!")
           
            return
        except Exception as e:
            await ctx.send("error")
           
            return

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension: str):
        """unload cogs"""
        try:
            await self.bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded!")
            return
        except Exception as e:
            await ctx.send("error")
            return

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        """reload cogs"""
        try:
            await self.bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} reloaded!")
            return
        except Exception as e:
            await ctx.send("error")
            return

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reloadall(self, ctx):
        """Reload all cogs"""
        try:
            cog_names = list(self.bot.extensions.keys())  # Create a copy of the keys
            for cog_name in cog_names:
                await self.bot.reload_extension(cog_name)
            await ctx.send("All cogs reloaded!")
        except Exception as e:
            await ctx.send("Error occurred while reloading cogs.")



async def setup(bot):
    await bot.add_cog(Admin(bot))

