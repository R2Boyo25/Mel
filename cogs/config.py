import discord  # type: ignore
import os
from discord.ext import commands  # type: ignore
from utils.funcs import *
from utils.jdb import JSONDatabase as jdb
from utils.serverconf import ServerConf as sc


class Config(commands.Cog):
    "Commands for configuring the bot"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def config(self, ctx: commands.Context) -> None:
        "Command group for configuring bot per-server"
        if ctx.invoked_subcommand is None:
            await ctx.send("Run .help config for a list of valid options")

    @config.command(name="joinmessage")
    @commands.has_permissions(manage_guild=True)
    async def joinmset(self, ctx: commands.Context, *, message: str) -> None:
        sc(ctx.guild.id).set("joinmessage", message)

    @config.command(name="joinurl")
    @commands.has_permissions(manage_guild=True)
    async def joinurlset(self, ctx: commands.Context, *, message: str) -> None:
        sc(ctx.guild.id).set("joinurl", message)

    @config.command(name="leavemessage")
    @commands.has_permissions(manage_guild=True)
    async def leavemset(self, ctx: commands.Context, *, message: str) -> None:
        sc(ctx.guild.id).set("leavemessage", message)

    @config.command(name="leaveurl")
    @commands.has_permissions(manage_guild=True)
    async def leaveurlset(self, ctx: commands.Context, *, message: str) -> None:
        sc(ctx.guild.id).set("leaveurl", message)

    @commands.command(name="prefix")
    async def prefixcom(self, ctx: commands.Context, *, prefix: str = "get") -> None:
        "Set or get the server's prefix"
        data = jdb("prefixes.json")

        if prefix == "get":
            if str(ctx.guild.id) in data.keys():
                await ctx.send(
                    f"Prefix for **{ctx.guild.name}** is '{data.get(str(ctx.guild.id))}'"
                )
            else:
                await ctx.send(
                    f"**{ctx.guild.name}** does not have a custom prefix yet, set one with `.prefix newprefix`"
                )
        if ctx.author.guild_permissions.manage_guild:
            if len(prefix) > 1:
                await ctx.send(
                    f'The bot does not support prefixes longer than 1 character (as in, the bot breaks), your prefix has been shortened to "{prefix[0]}"'
                )
            data.set(str(ctx.guild.id), prefix[0])
        else:
            await ctx.send("You do not have permission to change this server's prefix.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Config(bot))
