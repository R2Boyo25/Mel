import discord # type: ignore
import traceback
import os
from utils.funcs import *
from utils.jdb   import JSONDatabase as jdb
from utils.serverconf import ServerConf as sc
import procmessage

async def setup(bot: commands.Bot) -> None:
    @bot.event
    async def on_ready() -> None:
        channel = bot.get_channel(logChannel)
        msg = await channel.send('Bot Has Rebooted')

        users = len(set(bot.get_all_members()))

        print('logged in as {}'.format(bot.user))

        status = f"over {len(bot.guilds)} servers, {users} users | .help"
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

    @bot.event
    async def on_message(message: discord.Message) -> None:
        if message.author == bot.user:
            return

        if not message.content:
            return

        await procmessage.processMessage(message, bot)

        if str(message.content).replace(' ', '') == bot.user.mention:
            prefix = jdb("prefixes.json").get(str(message.guild.id))
            await message.channel.send(f"You pinged? do {prefix}help)")

        if not len(message.content) < 2:
            if not message.content[1] == '.':
                await bot.process_commands(message)

    @bot.event
    async def on_member_join(ctx: commands.Context) -> None:
        if ctx.guild.system_channel:
            channel = ctx.guild.system_channel
            
        else:
            channel = ctx.author

        sconf = sc(ctx.guild.id)

        joinmessage = sconf.get("joinmessage",
                                'Welcome {}! We hope you enjoy your time at {}.'.format(ctx.mention, ctx.guild),
                                lambda message: message.replace("member", ctx.mention).replace("server", str(ctx.guild)).replace("memcount", str(len([x for x in ctx.guild.members]))))

        joinurl = sconf.get("joinurl",
                            'https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif')

        embed= discord.Embed(title='Welcome to {}'.format(ctx.guild), description=joinmessage, colour=discord.Color.red())
        embed.set_thumbnail(url=joinurl)
        await channel.send(embed=embed)

    @bot.event
    async def on_member_remove(ctx: commands.Context) -> None:
        if ctx.guild.system_channel:
            print(f"Leave_channel found for {ctx.guild}")
            
        else:
            print(f"Leave_channel not found for {ctx.guild}: Switching To Backups")

        sconf = sc(ctx.guild.id)

        leavemessage = sconf.get("leavemessage",
                                 '{} has left. We hope you enjoyed your time at {}.'.format(ctx.name, ctx.guild),
                                lambda message: message.replace("member", ctx.mention).replace("server", str(ctx.guild)).replace("memcount", str(len([x for x in ctx.guild.members]))))

        leaveurl = sconf.get("leaveurl",
                             'https://media0.giphy.com/media/26u4b45b8KlgAB7iM/200.gif')

        embed = discord.Embed(title='Bye!', description=leavemessage, colour=discord.Color.red())
        embed.set_thumbnail(url=leaveurl)
        await ctx.guild.system_channel.send(embed=embed)

    @bot.event
    async def on_guild_join(guild: discord.Guild) -> None:
        log = bot.get_channel(logChannel)

        embed = discord.Embed(title="Server joined!", description=f"I have been added to **`{guild.name}`**.", color=0x2ecc71)

        server = guild

        embed.set_footer(text = guild.id, icon_url = guild.icon_url)

        embed.add_field(name="Created on:", value=f"```\n{server.created_at.strftime('%d %B %Y at %H:%M UTC+3')}```", inline=False)
        embed.add_field(name="Server ID:", value=f'```\n{server.id}```', inline=False)
        embed.add_field(name="Users on server:", value=f'```\n{server.member_count}```', inline=True)
        embed.add_field(name="Server owner:", value=f'```\n{server.owner} ({server.owner.id})```', inline=True)

        await log.send(embed=embed)
    
