# Importing some libraries
import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from os import getenv
from Keeping_alive import keep_alive
import json
from utils.util import get_prefix
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

#loads the secret file containg the bot's password
load_dotenv()

intents = discord.Intents.all()

# defining a few things
bot = commands.Bot(command_prefix=get_prefix,
                   owner_id=722168161713127435,
                   intents=discord.Intents.all(),
                   help_command=None)

# extenstion list, the extentions are located in the "cogs" folder
cogs = ["cogs.mod", "cogs.fun", "cogs.utility", "cogs.help", "cogs.errors", "cogs.helptest"]

# loads the extensions apon startup
for cog in cogs:
    bot.load_extension(cog)

# Set's the bot's status apon startup
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('..help'))

# When the bot joins a server, it adds the server to the database, along with it's prefix
@bot.event
async def on_guild_join(guild):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ".."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)

# Command group for performing bot admin actions
@bot.group()
@commands.is_owner()
async def sudo(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(
            "Use `..sudo <command>` to perform your bot admin actions.")

# load an extension
@sudo.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Sucessfully loaded the `{extension}` Cog.")

# Unload an extension
@sudo.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(
        f"Successfully unloaded the `{extension}` Cog.\nLol why are u making me more useless?"
    )

# Reload an extension
@sudo.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Done. Reloaded The `{extension}` Cog.")

# Shuts the bot down by logging out
@sudo.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("logging out... bye!")
    await ctx.bot.logout()

# local variable for the command below
bot.launch_time = datetime.utcnow()

# Gives how long the bot has been running
@bot.command()
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def uptime(ctx):
  delta_uptime = datetime.utcnow() - bot.launch_time
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  await ctx.send(f"The bot has been up for`{days}`days , `{hours}`hours and `{minutes}`minutes.")

# Runs the flask file
keep_alive()

# Logs the bot into discord
bot.run(getenv("TOKEN"))
