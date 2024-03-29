import discord  # type: ignore
import json
from discord.ext import commands  # type: ignore
from utils.jdb import JSONDatabase as jdb
from utils.serverconf import ServerConf as sc
from typing import Any, Optional


class ConfigError(Exception):
    pass


def strtobool(val: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', 'ye', 'yep', 'yeah', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', 'nope', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    if type(val) is bool:
        return val
    
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "ye", "yep", "yeah", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "nope", "0"):
        return False
    else:
        raise ValueError(
            "I don't know what '%r' means in the context of yes/no" % (val,)
        )


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


def config(key: str, default: Optional[Any] = None) -> Any:
    try:
        try:
            cdb = jdb("config.json")

        except:
            raise ConfigError("Config improperly formatted")

        if key in cdb.keys():
            return cdb.get(key)

        if default is not None:
            return default

        raise ConfigError(f"Config missing {key} and no default passed to config()")

    except ConfigError as e:
        print(e)
        quit()


# Load Config

ErrorChannel = int(config("logChannel"))
logChannel = int(config("errorChannel"))
TOKEN = config("token")
