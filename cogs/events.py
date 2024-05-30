from typing import cast
import discord
from discord.ext import commands
from mel.utils.jdb import JSONDatabase as JSONDatabase
from mel.utils.serverconf import ServerConf as sc
from mel.utils import strtobool
from mel import Mel


class Events(commands.Cog):
    "Background listeners that allow the bot to do what it does."

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mel: Mel = bot.mel  # type: ignore
        self.mel.config_options.update(
            [
                "join.send",
                "join.message",
                "join.url",
                "leave.send",
                "leave.message",
                "leave.url",
            ]
        )

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.mel.error_handler.log("logged in as {}".format(self.bot.user))

        users = len(set(self.bot.get_all_members()))

        status = f"over {len(self.bot.guilds)} servers, {users} users"
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=status)
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return

        if not message.content:
            return

        if not message.guild:
            return

        prefix = await (await JSONDatabase.load("prefixes")).get(
            str(message.guild.id), self.mel.config("default_bot_prefix")
        )

        if (
            str(message.content).replace(" ", "")
            == cast(discord.ClientUser, self.bot.user).mention
        ):
            await message.channel.send(f"You pinged? do {prefix}help)")

        elif not len(message.content) < 2:
            if not message.content[1] == prefix:
                await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, ctx: commands.Context[commands.Bot]) -> None:
        channel: discord.TextChannel | discord.User | discord.Member

        if ctx.guild is None:
            raise NotImplementedError("on_member_join called without a guild")

        guild = ctx.guild

        if guild.system_channel is not None:
            channel = guild.system_channel

        else:
            channel = ctx.author

        sconf = sc(ctx.guild.id)

        if not strtobool(await sconf.get("join.send", True)):
            return

        joinmessage = await sconf.get(
            "join.message",
            "Welcome {}! We hope you enjoy your time in {}.".format(
                ctx.author.mention, ctx.guild
            ),
            lambda message: message.replace("member", ctx.author.mention)
            .replace("server", guild.name)
            .replace("memcount", str(len(guild.members))),
        )

        joinurl = await sconf.get(
            "join.url", "https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif"
        )

        embed = discord.Embed(
            title="Welcome to {}".format(ctx.guild),
            description=joinmessage,
            colour=discord.Color.red(),
        )
        embed.set_thumbnail(url=joinurl)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, ctx: commands.Context[commands.Bot]) -> None:
        if ctx.guild is None:
            raise NotImplementedError("on_member_remove called without a guild")

        guild = ctx.guild

        if guild.system_channel is None:
            return

        sconf = sc(guild.id)

        if not strtobool(await sconf.get("leave.send", True)):
            return

        leavemessage = await sconf.get(
            "leave.message",
            "{} has left. We hope you enjoyed your time in {}.".format(
                ctx.author.name, ctx.guild
            ),
            lambda message: message.replace("member", ctx.author.mention)
            .replace("server", guild.name)
            .replace("memcount", str(len(guild.members))),
        )

        leaveurl = await sconf.get(
            "leave.url", "https://media0.giphy.com/media/26u4b45b8KlgAB7iM/200.gif"
        )

        embed = discord.Embed(
            title="Bye!", description=leavemessage, colour=discord.Color.red()
        )
        embed.set_thumbnail(url=leaveurl)
        await guild.system_channel.send(embed=embed)

    # @commands.Cog.listener()
    # async def on_guild_join(self, guild: discord.Guild) -> None:
    #     log = cast(discord.TextChannel, self.bot.get_channel(logChannel))

    #     embed = discord.Embed(
    #         title="Server joined!",
    #         description=f"I have been added to **`{guild.name}`**.",
    #         color=0x2ECC71,
    #     )

    #     embed.set_footer(
    #         text=guild.id, icon_url=None if guild.icon is None else guild.icon.url
    #     )

    #     embed.add_field(
    #         name="Created on:",
    #         value=f"```\n{guild.created_at.strftime('%d %B %Y at %H:%M UTC+3')}```",
    #         inline=False,
    #     )
    #     embed.add_field(name="Server ID:", value=f"```\n{guild.id}```", inline=False)
    #     embed.add_field(
    #         name="Users on server:", value=f"```\n{guild.member_count}```", inline=True
    #     )
    #     embed.add_field(
    #         name="Server owner:",
    #         value=f"```\n{guild.owner} ({None if guild.owner is None else guild.owner.id})```",
    #         inline=True,
    #     )

    #     await log.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    # this is here to prevent the bot from automatically processing commands.
    @bot.event
    async def on_message(ctx: commands.Context[commands.Bot]) -> None:
        pass

    await bot.add_cog(Events(bot))
