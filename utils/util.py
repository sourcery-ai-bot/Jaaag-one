import json


def get_prefix(bot, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


def get_blacklist(bot, message):
  
    with open("blacklist.json", "r") as f:
        blacklist = json.load(f)

    return blacklist[str(message.guild.id)]