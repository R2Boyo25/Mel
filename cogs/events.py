import discord, traceback, os
from utils.funcs import *
from database import Database as db
import procmessage

def setup(bot):
    @bot.event
    async def on_ready():

        channel = bot.get_channel(logChannel)
        msg = await channel.send('Bot Has Rebooted')

        sum = len(set(bot.get_all_members()))

        print('logged in as {}'.format(bot.user))

        status = f"over {len(bot.guilds)} servers, {sum} users | .help"
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

    @bot.event
    async def on_message(message):

        if message.author == bot.user:
            return

        await procmessage.processMessage(message, bot)

        if str(message.content).replace(' ', '') == bot.user.mention: 
            await message.channel.send("You poinged? do .help (or [yourserverseprefifix]help)")

        if not message.content[1]=='.':
            await bot.process_commands(message)

    @bot.event
    async def on_member_join(ctx):
        if ctx.guild.system_channel:
            channel = ctx.guild.system_channel
            print(f"Join_channel found for {ctx.guild}")
        else:
            channel = ctx.author
        
        try:
            cdb = db(f"configs/{ctx.guild.id}configs.json")

            rjoinmessage = cdb.get("joinmessage")

            joinmessage = rjoinmessage.replace("member", ctx.mention).replace("server", str(ctx.guild)).replace("memcount", str(len([x for x in ctx.guild.members])))

        except:

            joinmessage = 'Welcome {}! We hope you enjoy your time at {}.'.format(ctx.mention, ctx.guild)

        try:
            cdb = db(f"configs/{ctx.guild.id}configs.json")

            joinurl = cdb.get("joinurl")

        except Exception:

            joinurl = 'https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif'

        embed= discord.Embed(title='Welcome to {}'.format(ctx.guild), description=joinmessage, colour=discord.Color.red())
        embed.set_thumbnail(url=joinurl)
        await channel.send(embed=embed)

    @bot.event
    async def on_member_remove(ctx):
        if ctx.guild.system_channel:
            print(f"Leave_channel found for {ctx.guild}")
        else:
            print(f"Leave_channel not found for {ctx.guild}: Switching To Backups")

        try:
            cdb = db(f"configs/{ctx.guild.id}configs.json")

            rjoinmessage = cdb.get("leavemessage")

            joinmessage = rjoinmessage.replace("member", ctx.mention).replace("server", str(ctx.guild)).replace("memcount", str(len([x for x in ctx.guild.members])))

        except:

            joinmessage = '{} has left. We hope you enjoyed your time at {}.'.format(ctx.name, ctx.guild)

        try:
            cdb = db(f"configs/{ctx.guild.id}configs.json")

            joinurl = cdb.get("leaveurl")

        except Exception:

            joinurl = 'https://media0.giphy.com/media/26u4b45b8KlgAB7iM/200.gif'

        embed = discord.Embed(title='Bye!', description=joinmessage, colour=discord.Color.red())
        embed.set_thumbnail(url=joinurl)
        await ctx.guild.system_channel.send(embed=embed)

    @bot.event
    async def on_guild_join(guild):

        log = bot.get_channel(logChannel)

        embeded = discord.Embed(title="Server joined!", description=f"I have been added to **`{guild.name}`**.", color=0x2ecc71)

        server = guild

        embeded.set_footer(text = guild.id, icon_url = guild.icon_url)

        embeded.add_field(name="Created on:", value=f"```\n{server.created_at.strftime('%d %B %Y at %H:%M UTC+3')}```", inline=False)
        embeded.add_field(name="Server ID:", value=f'```\n{server.id}```', inline=False)
        embeded.add_field(name="Users on server:", value=f'```\n{server.member_count}```', inline=True)
        embeded.add_field(name="Server owner:", value=f'```\n{server.owner} ({server.owner.id})```', inline=True)

        await log.send(embed=embeded)
    