import os
import sys
import discord
from discord.ext import commands
from pretty_help import PrettyHelp  # type: ignore
from mel import Mel
from typing import Any


# default imports for new extensions/cogs
imports = """import discord
from discord.ext import commands
from utils.funcs import *
from utils.jdb   import JSONDatabase as jdb"""

cogs: dict[str, bool] = {}

mel_ = Mel(bot=None)  # type: ignore


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=mel_.get_prefix,
    help_command=PrettyHelp(),
    allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=True),
    intents=intents,
)

mel_.bot = bot
bot.mel = mel_  # type: ignore


@bot.listen()
async def on_ready() -> None:
    errors = []

    for _, _, filenames in os.walk("./cogs"):
        extension_paths = filenames
        break

    disabled_extensions = mel_.mel_config.get("disabled", [])

    for ext in extension_paths:
        if ext.endswith("~"):
            continue

        if ext.startswith("#") and ext.endswith("#"):
            continue

        ext_import_name = ext.replace(".py", "").replace("/", ".")

        try:
            if ext_import_name in disabled_extensions:
                cogs[ext_import_name] = False
                continue

            await bot.load_extension(f"cogs.{ext_import_name}")
            cogs[ext_import_name] = True

        except commands.errors.ExtensionAlreadyLoaded:
            continue

        except Exception as e:
            cogs[ext_import_name] = False

            errors.append(e)

    for i, error in enumerate(errors):
        await mel_.error_handler.report(error)


@bot.command("sync", hidden=True)
@commands.is_owner()
async def sync_slash_commands(ctx: commands.Context[commands.Bot]) -> None:
    synced = await bot.tree.sync()

    if not len(synced):
        return

    print("Synchronized commands:\n\t- " + "\n\t- ".join(map(str, synced)))


@bot.command("load", hidden=True)
@commands.is_owner()
async def load_extension(ctx: commands.Context[commands.Bot], extension: str) -> None:
    global cogs

    ext = extension
    ext_import_name = ext.replace(".py", "").replace("/", ".")
    is_loaded = cogs.get(ext, False)

    if not is_loaded:
        try:
            await bot.load_extension(f"cogs.{ext_import_name}")
            cogs[ext] = True

            await ctx.send(f":white_check_mark: Loaded {ext}")

        except Exception as error:
            cogs[ext] = False

            embed = discord.Embed(
                title=f"Failed to load {ext}",
                description="```py\n{}\n```".format(error),
                color=0x9C0B21,
            )

            await ctx.send(embed=embed)

    else:
        try:
            await bot.reload_extension(f"cogs.{ext_import_name}")
            cogs[ext] = True

            await ctx.send(f":white_check_mark: Reloaded {ext}")

        except Exception as error:
            embed = discord.Embed(
                title=f"Failed to reload {ext}",
                description="```py\n{}\n```".format(error),
                color=0x9C0B21,
            )

            await ctx.send(embed=embed)


@bot.command("unload", hidden=True)
@commands.is_owner()
async def unloadExtension(ctx: commands.Context[commands.Bot], extension: str) -> None:
    global cogs

    ext = extension

    try:
        isLoaded = cogs[ext]

    except:
        isLoaded = False

    if isLoaded:
        try:
            ext_import_name = ext.replace(".py", "").replace("/", ".")

            await bot.unload_extension(f"cogs.{ext_import_name}")
            cogs[ext] = False

            await ctx.send(f":white_check_mark: Unloaded {ext}")

        except Exception as error:
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
async def listExtensions(ctx: commands.Context[commands.Bot]) -> None:
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
async def reloadAllExtensions(ctx: commands.Context[commands.Bot]) -> None:
    for _, _, filenames in os.walk("./cogs"):
        exts = filenames
        break

    for ext in exts:
        ext_import_name = ext.replace(".py", "").replace("/", ".")

        try:
            await bot.reload_extension(f"cogs.{ext_import_name}")
            cogs[ext_import_name] = True

        except Exception as error:
            await mel_.error_handler.report(error)

    await ctx.send(":white_check_mark: Reloaded extensions")


@bot.command("enableextension", hidden=True)
@commands.is_owner()
async def enableExtension(ctx: commands.Context[commands.Bot], ext: str) -> None:
    disabled: list[str] = mel_.mel_config.get("disabled", [])

    if ext not in disabled:
        return

    disabled.remove(ext)
    mel_.mel_config.set("disabled", disabled)


@bot.command("disableextension", hidden=True)
@commands.is_owner()
async def disableExtension(ctx: commands.Context[commands.Bot], ext: str) -> None:
    disabled: list[str] = mel_.mel_config.get("disabled", [])

    if ext in disabled:
        return

    disabled.append(ext)
    mel_.mel_config.set("disabled", disabled)


@bot.command("newcog", hidden=True)
@commands.is_owner()
async def genNewCog(
    ctx: commands.Context[commands.Bot], fname: str, cogname: str
) -> None:
    fname = fname.lower().rstrip(".py") + ".py"

    for _, _, filenames in os.walk("./cogs"):
        exts = filenames
        break

    if fname in exts:
        await ctx.send(
            f":x: Failed to generate extension {fname}, extension already exists"
        )

        return

    template = f"""{imports}

class {cogname.title()}(commands.Cog):
    \"\"\"{cogname.title()} Commands\"\"\"
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog({cogname.title()}(bot))
    """

    with open(f"./cogs/{fname}", "w") as f:
        f.write(template)

    await ctx.send(f":white_check_mark: Generated extension {fname}")


@bot.command("newext", hidden=True)
@commands.is_owner()
async def genNewExt(ctx: commands.Context[commands.Bot], fname: str) -> None:
    template = f"""{imports}


async def setup(bot: commands.Bot) -> None:
    # put code here
    ...
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


@bot.event
async def on_command_error(
    ctx: commands.Context[commands.Bot], error: Exception
) -> None:
    if hasattr(ctx, "handled") and ctx.handled:
        return

    if type(error) is commands.MissingPermissions:
        await ctx.send("You don't have permission to do that!", ephemeral=True)
        return

    if (
        str(error).startswith("You are on cooldown. Try again in")
        or (
            str(error).startswith('Command "') and str(error).endswith('" is not found')
        )
        or str(error).endswith("is a required argument that is missing.")
    ):
        await ctx.send(str(error), ephemeral=True)
        return

    response = (
        await mel_.error_handler.report(
            error,
            context={"content": ctx.message.content},
            user={"id": ctx.author.id, "username": ctx.author.name},
        )
        or ""
    )

    embed = discord.Embed(
        title="Unknown Error",
        description=f"Users: Check to see if you made any mistakes with your command.\n\n{response}".strip(),
        color=0x9C0B21,
    )

    await ctx.send(embed=embed, ephemeral=True)


@bot.event
async def on_error(
    ctx: commands.Context[commands.Bot], *args: Any, **kwargs: Any
) -> None:
    info = sys.exc_info()

    if info[1] is None:
        return

    await mel_.error_handler.report(
        info[1],
        context={"content": ctx.message.content},
        user={"id": ctx.author.id, "username": ctx.author.name},
    )
