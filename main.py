import os
import json
import logging
import datetime

import discord
from pathlib import Path
import motor.motor_asyncio
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

from utils.mongo import Document
from Keeping_alive import keep_alive

load_dotenv()

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


async def get_prefix(bot, message):
    
    if not message.guild:
        return commands.when_mentioned_or("..")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or("..")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("..")(bot, message)


bot = commands.Bot(
    command_prefix=get_prefix, case_insensitive=True, owner_id=722168161713127435,
    help_command=None
)
bot.config_token = os.getenv("TOKEN")
bot.connection_url = os.getenv("MONGO")
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

@bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {bot.user.name}\n-----\nUser id: {bot.user.id}\n-----\nMy current prefix is: ..\n-----"
    )
    await bot.change_presence(
        activity=discord.Game(
            name="..help"
        ),
      status=discord.Status.dnd
    ) 

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["jaaagdocs"]
    bot.config = Document(bot.db, "config")
    bot.modlog = Document(bot.db, "modlogchannel")
    print("Initializing Database\n-----")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id in bot.blacklisted_users:
        return

    if message.content.startswith(f"<@!{bot.user.id}>") and \
        len(message.content) == len(f"<@!{bot.user.id}>"
    ):
        data = await bot.config.get_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = ".."
        else:
            prefix = data["prefix"]
        await message.channel.send(f"My prefix here is `{prefix}`")

    await bot.process_commands(message)


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(
      f'cogs.{extension}'
      )
    await ctx.send(
      f"`{extension}` Cog ha been loaded."
    )


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(
      f'cogs.{extension}'
      )
    await ctx.send(
        f"`{extension}` Cog has been unloaded."
    )


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(
      f'cogs.{extension}'
      )
    bot.load_extension(
      f'cogs.{extension}'
      )
    await ctx.send(
      f"`{extension}` Cog has been reloaded."
    )


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send(
      "logging out... bye!"
      )
    await ctx.bot.close()

keep_alive()

if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)
    