from discord.ext import commands


class Errors(commands.Cog):
    """A cog that handles on command errors."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context,
                               error: commands.CommandError):

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "Looks like are missing the required permissions to run this command."
        elif isinstance(error, commands.UserInputError):
            message = "Something about your input was wrong, Please try again."
        else:
            message = "Oops! Something went wrong while running the command. :man_shrugging:"

        await ctx.send(message, delete_after=5)


def setup(bot: commands.Bot):
    bot.add_cog(Errors(bot))