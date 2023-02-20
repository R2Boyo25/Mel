import discord  # type: ignore
import traceback
import os
from utils.funcs import *
from utils.jdb import JSONDatabase as jdb
from utils.serverconf import ServerConf as sc

class Events(commands.Cog):
    "Background listeners that allow the bot to do what it does."

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        channel = self.bot.get_channel(logChannel)
        msg = await channel.send("Bot Has Rebooted")

        users = len(set(self.bot.get_all_members()))

        print("logged in as {}".format(self.bot.user))

        prefix = jdb("prefixes.json").get(str(message.guild.id), config("prefix"))
        status = f"over {len(self.bot.guilds)} servers, {users} users | {prefix}help"
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=status)
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return

        if not message.content:
            return

        prefix = jdb("prefixes.json").get(str(message.guild.id), config("prefix"))
        
        if str(message.content).replace(" ", "") == self.bot.user.mention:
            await message.channel.send(f"You pinged? do {prefix}help)")

        elif not len(message.content) < 2:
            if not message.content[1] == prefix:
                await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, ctx: commands.Context) -> None:
        if ctx.guild.system_channel:
            channel = ctx.guild.system_channel

        else:
            channel = ctx.author

        sconf = sc(ctx.guild.id)

        joinmessage = sconf.get(
            "join.message",
            "Welcome {}! We hope you enjoy your time at {}.".format(
                ctx.mention, ctx.guild
            ),
            lambda message: message.replace("member", ctx.mention)
            .replace("server", str(ctx.guild))
            .replace("memcount", str(len([x for x in ctx.guild.members]))),
        )

        joinurl = sconf.get(
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
    async def on_member_remove(self, ctx: commands.Context) -> None:
        if ctx.guild.system_channel:
            print(f"Leave_channel found for {ctx.guild}")

        else:
            print(f"Leave_channel not found for {ctx.guild}: Switching To Backups")

        sconf = sc(ctx.guild.id)

        leavemessage = sconf.get(
            "leave.message",
            "{} has left. We hope you enjoyed your time at {}.".format(
                ctx.name, ctx.guild
            ),
            lambda message: message.replace("member", ctx.mention)
            .replace("server", str(ctx.guild))
            .replace("memcount", str(len([x for x in ctx.guild.members]))),
        )

        leaveurl = sconf.get(
            "leave.url", "https://media0.giphy.com/media/26u4b45b8KlgAB7iM/200.gif"
        )

        embed = discord.Embed(
            title="Bye!", description=leavemessage, colour=discord.Color.red()
        )
        embed.set_thumbnail(url=leaveurl)
        await ctx.guild.system_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        log = self.bot.get_channel(logChannel)

        embed = discord.Embed(
            title="Server joined!",
            description=f"I have been added to **`{guild.name}`**.",
            color=0x2ECC71,
        )

        server = guild

        embed.set_footer(text=guild.id, icon_url=guild.icon_url)

        embed.add_field(
            name="Created on:",
            value=f"```\n{server.created_at.strftime('%d %B %Y at %H:%M UTC+3')}```",
            inline=False,
        )
        embed.add_field(name="Server ID:", value=f"```\n{server.id}```", inline=False)
        embed.add_field(
            name="Users on server:", value=f"```\n{server.member_count}```", inline=True
        )
        embed.add_field(
            name="Server owner:",
            value=f"```\n{server.owner} ({server.owner.id})```",
            inline=True,
        )

        await log.send(embed=embed)


async def setup(bot: commands.Bot) -> None:

    # this is here to prevent the bot from automatically processing commands.
    @bot.event
    async def on_message(ctx: commands.Context) -> None:
        pass
    
    await bot.add_cog(Events(bot))
