import json


# function for getting the stored prefix of a server from the json file
def get_prefix(bot, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# Serves a similar function as the above one but only this one isn't being used
def get_blacklist(bot, message):
  
    with open("blacklist.json", "r") as f:
        blacklist = json.load(f)

    return blacklist[str(message.guild.id)]