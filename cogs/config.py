import discord
from discord.ext import commands
from mel.utils.jdb import JSONDatabase
from mel.utils.serverconf import ServerConf
from mel import Mel
from typing import List, cast


class Config(commands.Cog):
    "Commands for configuring the bot"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mel: Mel = bot.mel  # type: ignore

    async def autocomplete_name(
        self, interaction: discord.Interaction, current: str
    ) -> List[discord.app_commands.Choice[str]]:
        return [
            discord.app_commands.Choice(name=option, value=option)
            for option in self.mel.config_options
            if current.lower() in option.lower()
        ]

    @commands.hybrid_group(name="config", fallback="list")
    async def config_group(self, ctx: commands.Context[commands.Bot]) -> None:
        "Configure the bot"

        if ctx.guild is None:
            raise NotImplementedError("Config called without a guild")

        embed = discord.Embed(title=f"Configuration Values for {ctx.guild.name}")

        srvcnf = ServerConf(ctx.guild.id)
        for configkey in self.mel.config_options:
            embed.add_field(
                name=configkey, value=await srvcnf.get(configkey, "Not set")
            )

        await ctx.send(embed=embed, ephemeral=True)

    @config_group.command(name="set", help="Set a config value")
    @commands.has_permissions(manage_guild=True)
    @discord.app_commands.describe(
        name="The name of the setting to set",
        setting="What to set the setting to. Leaving unspecified resets the setting to default.",
    )
    @discord.app_commands.autocomplete(name=autocomplete_name)
    async def set_config_value(
        self, ctx: commands.Context[commands.Bot], name: str, setting: str | None = None
    ) -> None:
        if ctx.guild is None:
            raise NotImplementedError("Config called without a guild")

        await ServerConf(ctx.guild.id).set(name, setting)
        await ctx.send(f"`{name}` has been set to `{setting}`", ephemeral=True)

    @config_group.command(name="get", help="Get a config's value")
    @discord.app_commands.describe(name="The name of the setting to get")
    @discord.app_commands.autocomplete(name=autocomplete_name)
    async def get_config_value(
        self, ctx: commands.Context[commands.Bot], name: str
    ) -> None:
        if ctx.guild is None:
            raise NotImplementedError("Config called without a guild")

        await ctx.send(
            await ServerConf(ctx.guild.id).get(name, f"`{name}` is not set"),
            ephemeral=True,
        )

    @commands.command(name="prefix")
    async def prefixcom(
        self, ctx: commands.Context[commands.Bot], *, prefix: str = "get"
    ) -> None:
        "Set or get the server's prefix"

        if ctx.guild is None:
            raise NotImplementedError("Config called without a guild")

        data = await JSONDatabase.load("prefixes")

        if prefix == "get":
            if str(ctx.guild.id) in data.keys():
                retrieved_prefix = await data.get(
                    str(ctx.guild.id), self.mel.config("default_bot_prefix")
                )

                await ctx.send(
                    f"Prefix for **{ctx.guild.name}** is '{retrieved_prefix}'"
                )

            else:
                await ctx.send(
                    f"**{ctx.guild.name}** does not have a custom prefix yet, set one with `.prefix newprefix`"
                )

        elif cast(discord.Member, ctx.author).guild_permissions.manage_guild:
            if len(prefix) > 1:
                await ctx.send(
                    f'The bot does not support prefixes longer than 1 character (as in, the bot breaks), your prefix has been shortened to "{prefix[0]}"'
                )
            await data.set(str(ctx.guild.id), prefix[0])

        else:
            await ctx.send("You do not have permission to change this server's prefix.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Config(bot))
