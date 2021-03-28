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
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds. :hourglass_flowing_sand:"
        elif isinstance(error, commands.MissingPermissions):
            message = "Looks like you are missing the required permissions to run this command. Sad..."
        elif isinstance(error, commands.UserInputError):
            message = "Something about your input seems really wrong, Please try again."
        else:
            message = "Oops! Something went wrong while running the command. :man_shrugging:"

        await ctx.send(message, delete_after=6)


def setup(bot: commands.Bot):
    bot.add_cog(Errors(bot))
