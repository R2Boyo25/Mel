import discord  # type: ignore
import os
from discord.ext import commands  # type: ignore
from utils.funcs import *
from utils.jdb import JSONDatabase as jdb
from utils.serverconf import ServerConf as sc
from typing import List


class Config(commands.Cog):
    "Commands for configuring the bot"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.config_options.update(["join.message", "join.url", "leave.message", "leave.url"])

    async def autocomplete_name(self, interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
        return [discord.app_commands.Choice(name=option, value=option) for option in self.bot.config_options if current.lower() in option.lower()]
        
    @commands.hybrid_command(name="config")
    @discord.app_commands.autocomplete(name=autocomplete_name)
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx: commands.Context, name: str = None, setting: str = None) -> None:
        "Configure the bot"
        
        if name is None:
            embed = discord.Embed(title=f"Configuration Values for {ctx.guild.name}")

            srvcnf = sc(ctx.guild.id)
            for configkey in self.bot.config_options:
                embed.add_field(name=configkey, value=srvcnf.get(configkey, "Not set"))

            await ctx.send(embed=embed, ephemeral=True)

            return
                
        if setting is None:
            await ctx.send(sc(ctx.guild.id).get(name, f"`{name}` is not set"), ephemeral=True)
            return

        sc(ctx.guild.id).set(name, setting)
        await ctx.send(f"`{name}` has been set to `{setting}`", ephemeral=True)
        return

    @commands.command(name="prefix")
    async def prefixcom(self, ctx: commands.Context, *, prefix: str = "get") -> None:
        "Set or get the server's prefix"
        data = jdb("prefixes.json")

        if prefix == "get":
            if str(ctx.guild.id) in data.keys():
                await ctx.send(
                    f"Prefix for **{ctx.guild.name}** is '{data.get(str(ctx.guild.id), config('prefix'))}'"
                )
                
            else:
                await ctx.send(
                    f"**{ctx.guild.name}** does not have a custom prefix yet, set one with `.prefix newprefix`"
                )
                
        elif ctx.author.guild_permissions.manage_guild:
            if len(prefix) > 1:
                await ctx.send(
                    f'The bot does not support prefixes longer than 1 character (as in, the bot breaks), your prefix has been shortened to "{prefix[0]}"'
                )
            data.set(str(ctx.guild.id), prefix[0])
            
        else:
            await ctx.send("You do not have permission to change this server's prefix.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Config(bot))
