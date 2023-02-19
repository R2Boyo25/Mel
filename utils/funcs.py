import discord  # type: ignore
import json
from discord.ext import commands  # type: ignore
from utils.jdb import JSONDatabase as jdb
from utils.serverconf import ServerConf as sc
from typing import Any


class ConfigError(Exception):
    pass


async def get_prefix(bot: commands.Bot, message: discord.Message) -> Any:

    prefix = config("prefix")

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:

        # No prefix in dms
        return ""

    else:

        # Open prefixes.json and save it to keys
        with open("prefixes.json") as json_file:

            keys = json.load(json_file)

        # Check if the guild is in keys, and if so return the custom prefix
        if str(message.guild.id) in keys:

            prefixes = keys[str(message.guild.id)]

        else:

            if str(type(prefix)) == "<class 'list'>":
                prefixes = [i for i in prefix]
            else:
                prefixes = [prefix]

    # If we are in a guild, we allow for the user to mention us or use the custom prefix.
    return commands.when_mentioned_or(*prefixes)(bot, message)


def config(key: str) -> Any:
    try:

        try:

            cdb = jdb("config.json")

        except:

            raise ConfigError("Config improperly formatted")

        try:

            return cdb.get(key)

        except:

            raise ConfigError(f"Config missing {key}")

    except ConfigError as e:

        print(e)
        quit()


# Load Config

ErrorChannel = int(config("logChannel"))
logChannel = int(config("errorChannel"))
TOKEN = config("token")
