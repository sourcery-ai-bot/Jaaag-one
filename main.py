import os
import logging

import discord
from pathlib import Path
import motor.motor_asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

from Jaaagbot.utils.mongo import Document
from Jaaagbot.core.Keeping_alive import keep_alive

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

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=get_prefix, case_insensitive=True, owner_id=722168161713127435,
    help_command=None,
    intents=intents
)
bot.config_token = os.getenv("TOKEN")
bot.connection_url = os.getenv("MONGO")
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.blacklisted_guilds = []
bot.cwd = cwd


@bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {bot.user.name}\n-----\nUser id: {bot.user.id}\n-----\nBase prefix: ..\n-----"
    )
    await bot.change_presence(
        activity=discord.Game(
            name="..help"
        ),
      status=discord.Status.dnd
    ) 

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(
      bot.connection_url
      )
    )
    bot.db = bot.mongo["jaaagdocs"]
    bot.config = Document(bot.db, "config")
    bot.modlog = Document(bot.db, "modlogchannel")
    bot.muterole = Document(bot.db, "muterole")
    print("Initializing Database\n-----")


@bot.event
async def on_guild_join(guild):
    if guild.id in bot.blacklisted_guilds:
        await guild.leave()
    return


@bot.event
async def on_command(command):
    if command.guild.id in bot.blacklisted_guilds:
        embed = discord.Embed(
            title="Notice:",
            description=
                "```xml\nI have left this guild because it has been blacklisted.```",
            color=discord.Color.red(),
            timestamp=datetime.utcnow())
        embed.set_author(name="Jaaag Error Menu",
                        icon_url=f"{bot.user.avatar_url}")
        await command.channel.send(embed=embed)
        await command.guild.leave()
        return


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
        await message.channel.send(
          f"My prefix here is `{prefix}`"
        )

    await bot.process_commands(message)
    

@bot.command(brief="Load a Cog",
help="loads a specific Cog.")
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(
      f'Jaaagbot.cogs.{extension}'
      )
    await ctx.send(
      f"`{extension}` Cog has been loaded."
    )


@bot.command(brief="Unload a Cog",
help="unloads a specific Cog.")
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(
      f'Jaaagbot.cogs.{extension}'
      )
    await ctx.send(
        f"`{extension}` Cog has been unloaded."
    )


keep_alive()

bot.load_extension("Jaaagbot.core.error_handler")


if __name__ == "__main__":
    for file in os.listdir(cwd + "/Jaaagbot/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"Jaaagbot.cogs.{file[:-3]}")

    bot.run(bot.config_token)
    