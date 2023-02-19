#!/usr/bin/env python

import os

if not os.path.exists("./config.json"):
    with open("./config.json", "w") as f:
        f.write(
            '{\n    "token": "token-goes-here",\n    "logChannel": id-goes-here,\n    "errorChannel": id-goes-here,\n    "prefix": ","\n}'
        )

    print(
        "This is the first run of the bot,\nYou need to fill in the configuration\noptions in config.json for the bot to function"
    )
    quit()

import sys

sys.path = sys.path + ["."]

import traceback
import discord  # type: ignore
from discord.ext import commands  # type: ignore
from pretty_help import PrettyHelp  # type: ignore
from utils.funcs import *
from utils.jdb import JSONDatabase as jdb
from typing import Any
import logging

# default imports for new extensions/cogs
imports = """import discord # type: ignore
from discord.ext import commands # type: ignore
from utils.funcs import *
from utils.jdb   import JSONDatabase as jdb"""

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.txt", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
logger = logging.getLogger("TemplateBot")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

cogs = {}


def print(*messages: str) -> None:
    logger.info(" ".join(messages))

    __builtins__.print(*messages)


if "PrettyHelp" in globals():
    if hasattr(discord, "Intents"):
        intents = discord.Intents.all()

        bot = commands.Bot(
            command_prefix=get_prefix,
            help_command=PrettyHelp(),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=True
            ),
            intents=intents,
        )

    else:
        bot = commands.Bot(
            command_prefix=get_prefix,
            help_command=PrettyHelp(),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=True
            ),
        )

else:
    if hasattr(discord, "Intents"):
        intents = discord.Intents.all()

        bot = commands.Bot(
            command_prefix=get_prefix,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=True
            ),
            intents=intents,
        )

    else:
        bot = commands.Bot(
            command_prefix=get_prefix,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=True
            ),
        )


@bot.listen()
async def on_ready() -> None:
    errors = []

    for _, _, filenames in os.walk("./cogs"):
        exts = filenames
        break

    with open("disabled.txt", "r") as f:
        a = f.read().strip("\n").split("\n")

    for ext in exts:
        if ext.endswith("~"):
            continue

        if ext.startswith("#") and ext.endswith("#"):
            continue

        try:
            if ext.replace(".py", "") in a:
                raise Exception("DisabledExtension")

            await bot.load_extension(f'cogs.{ext.replace(".py", "")}')
            print(f"Loaded {ext}")
            cogs[ext.replace(".py", "")] = True

        except Exception as e:
            se = str(e)
            if "DisabledExtension" in se:
                print(f"Didn't load disabled extension {ext}")
                cogs[ext.replace(".py", "")] = False

            elif se.startswith("Extension 'cogs.") and se.endswith("' is already loaded"):
                continue
                
            else:
                print(f"Failed to load {ext}")
                cogs[ext.replace(".py", "")] = False

                errors.append(e)

    for i, error in enumerate(errors):
        log = bot.get_channel(ErrorChannel)

        embed = discord.Embed(
            title="Error",
            description="```py\n{}\n```".format(
                "".join(
                    traceback.format_exception(type(error), error, error.__traceback__)
                ).replace("```", "\`\`\`")
            ),
            color=0x9C0B21,
        )

        await log.send(embed=embed)

        del errors[i]


@bot.command("load", hidden=True)
@commands.is_owner()
async def loadExtension(ctx: commands.Context, extension: str) -> None:
    global cogs

    ext = extension

    try:
        isLoaded = cogs[ext]

    except:
        isLoaded = False

    if not isLoaded:
        try:
            await bot.load_extension(f'cogs.{ext.replace(".py", "")}')
            print(f"Loaded {ext}")
            cogs[ext] = True

            await ctx.send(f":white_check_mark: Loaded {ext}")

        except Exception as error:
            print(f"Failed to load {ext}")
            cogs[ext] = False

            embed = discord.Embed(
                title=f"Failed to load {ext}",
                description="```py\n{}\n```".format(error),
                color=0x9C0B21,
            )
            await ctx.send(embed=embed)

    else:
        try:
            await bot.reload_extension(f'cogs.{ext.replace(".py", "")}')
            print(f"Reloaded {ext}")
            cogs[ext] = True

            await ctx.send(f":white_check_mark: Reloaded {ext}")

        except Exception as error:
            print(f"Failed to reload {ext}")

            embed = discord.Embed(
                title=f"Failed to reload {ext}",
                description="```py\n{}\n```".format(error),
                color=0x9C0B21,
            )
            await ctx.send(embed=embed)


@bot.command("unload", hidden=True)
@commands.is_owner()
async def unloadExtension(ctx: commands.Context, extension: str) -> None:
    global cogs

    ext = extension

    try:
        isLoaded = cogs[ext]

    except:
        isLoaded = False

    if isLoaded:
        try:
            await bot.unload_extension(f'cogs.{ext.replace(".py", "")}')
            print(f"Unloaded {ext}")
            cogs[ext] = False

            await ctx.send(f":white_check_mark: Unloaded {ext}")

        except Exception as error:
            print(f"Failed to unload {ext}")
            cogs[ext] = True

            embed = discord.Embed(
                title=f"Failed to unload {ext}",
                description="```py\n{}\n```".format(error),
                color=0x9C0B21,
            )
            await ctx.send(embed=embed)

    else:
        await ctx.send(f":x: Failed to unload {ext}, {ext} is not already loaded")


@bot.command("extensions", hidden=True)
@commands.is_owner()
async def listExtensions(ctx: commands.Context) -> None:
    global cogs

    embeded = discord.Embed(
        title="Extensions", description=f"Status of my extensions.", color=0x2ECC71
    )

    for i in cogs.keys():
        embeded.add_field(
            name=i,
            value=str(cogs[i])
            .replace("True", ":white_check_mark:")
            .replace("False", ":x:"),
        )

    await ctx.send(embed=embeded)


@bot.command("reloadall", hidden=True)
@commands.is_owner()
async def reloadAllExtensions(ctx: commands.Context) -> None:
    for _, _, filenames in os.walk("./cogs"):
        exts = filenames
        break

    for ext in exts:
        try:
            await bot.reload_extension(f'cogs.{ext.replace(".py", "")}')
            print(f"Reloaded {ext}")
            cogs[ext.replace(".py", "")] = True

        except:
            print(f"Failed to reload {ext}")

    await ctx.send(":white_check_mark: Reloaded extensions")


@bot.command("enableextension", hidden=True)
@commands.is_owner()
async def enableExtension(ctx: commands.Context, ext: str) -> None:
    with open("disabled.txt", "r") as f:
        a = f.read().split("\n")

    if ext in a:
        del a[a.index(ext)]
        with open("disabled.txt", "w") as f:
            f.write("\n".join(a))


@bot.command("disableextension", hidden=True)
@commands.is_owner()
async def disableExtension(ctx: commands.Context, ext: str) -> None:
    with open("disabled.txt", "r") as f:
        a = f.read().split("\n")

    if ext not in a:
        a.append(ext)
        with open("disabled.txt", "w") as f:
            f.write("\n".join(a))


@bot.command("newcog", hidden=True)
@commands.is_owner()
async def genNewCog(ctx: commands.Context, fname: str, cogname: str) -> None:
    template = f"""{imports}

class {cogname.title()}(commands.Cog):
    \'\'\'{cogname.title()} Commands\'\'\'
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog({cogname.title()}(bot))
    """

    fname = fname.lower().rstrip(".py") + ".py"

    for _, _, filenames in os.walk("./cogs"):
        exts = filenames
        break

    if fname not in exts:
        with open(f"./cogs/{fname}", "w") as f:
            f.write(template)

        await ctx.send(f":white_check_mark: Generated extension {fname}")

    else:
        await ctx.send(
            f":x: Failed to generate extension {fname}, extension already exists"
        )


@bot.command("newext", hidden=True)
@commands.is_owner()
async def genNewExt(ctx: commands.Context, fname: str) -> None:
    template = f"""{imports}

async def setup(bot: commands.Bot) -> None:
    #put code here
    """

    fname = fname.lower().rstrip(".py") + ".py"

    for _, _, filenames in os.walk("./cogs"):
        exts = filenames
        break

    if fname not in exts:
        with open(f"./cogs/{fname}", "w") as f:
            f.write(template)

        await ctx.send(f":white_check_mark: Generated extension {fname}")

    else:
        await ctx.send(
            f":x: Failed to generate extension {fname}, extension already exists"
        )


@bot.command("tocog", hidden=True)
@commands.is_owner()
async def convertCommand(ctx: commands.Context, *, code: str) -> None:
    code = code.replace("@bot", "@commands")
    code = code.replace("bot.", "self.bot.")
    code = code.replace("(ctx", "(self, ctx")
    code = code.replace("```", "\`\`\`")

    await ctx.send(code)


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception) -> None:
    if hasattr(ctx, "handled"):
        if ctx.handled:
            return

    if str(error) == "MissingPermission":
        await ctx.send("You don't have permission to do that!")

    elif (
        str(error).startswith("You are on cooldown. Try again in")
        or (
            str(error).startswith('Command "') and str(error).endswith('" is not found')
        )
        or str(error).endswith("is a required argument that is missing.")
    ):
        await ctx.send(error)

    else:
        tb = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )

        print(tb)

        embed = discord.Embed(
            title="Unknown Error",
            description="Users: Check to see if you made any mistakes with your command.\nDevs: Check the log channel for errors.",
            color=0x9C0B21,
        )
        await ctx.send(embed=embed)

        log = bot.get_channel(ErrorChannel)

        embed = discord.Embed(
            title="Error",
            description="```py\n{}\n```".format(
                "".join(
                    traceback.format_exception(type(error), error, error.__traceback__)
                )
            ),
            color=0x9C0B21,
        )
        embed.add_field(name="Author", value=f"{ctx.author.id}\n({ctx.author})")
        embed.add_field(name="Message Content", value=f"```{ctx.message.content}```")
        await log.send(embed=embed)


@bot.event
async def on_error(ctx: commands.Context, *args: Any, **kwargs: Any) -> None:
    tb = traceback.format_exc()

    print(tb)

    log = bot.get_channel(ErrorChannel)

    embed = discord.Embed(
        title="Error",
        description="```py\n{}\n```".format(tb.replace("```", "\`\`\`")),
        color=0x9C0B21,
    )

    await log.send(embed=embed)


if __name__ == "__main__":
    bot.run(TOKEN)
