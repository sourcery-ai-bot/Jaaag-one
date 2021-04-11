# Imports
import discord
from discord.ext import commands


# Intializing the extension
class Errors(commands.Cog):
    """A cog that handles on command errors."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Prints on the console when the extension is loaded 
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} listener has been loaded\n-----")
        
    # Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context,
                               error: commands.CommandError):

        if isinstance(error, commands.CommandNotFound):
            message = ":x: **Error:**\n Command not found."
        elif isinstance(error, commands.CommandOnCooldown):
            message = f":x: **Error:**\nThis command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = ":x: **Error:**\nLooks like you are missing the required permission(s) to run this command."
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                message = f":x: **Error:**\nThe command `{ctx.command}` cannot be used in Private Messages."
            except discord.HTTPException:
                pass
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f":x: **Error:**\nThe command `{ctx.command}` is currently disabled.")
        elif isinstance(error, commands.UserInputError):
            message = ":x: **Error:**\nSomething about your input seems wrong, Please try again."
        else:
            message = ":x: **Error:**\nSomething went wrong while running the command."

        await ctx.send(message)


# Adds the extention
def setup(bot: commands.Bot):
    bot.add_cog(Errors(bot))
