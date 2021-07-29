import discord, os
from discord.ext import commands
from utils.funcs import *
from database import Database as db

class Config(commands.Cog):
    "Commands for configuring the bot"
    
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Run .help config for a list of valid options")

    @config.command(name='joinmessage')
    @commands.has_permissions(manage_guild=True)
    async def joinmset(self, ctx, * , message:str):
        if not os.path.exists(f"configs/{ctx.guild.id}configs.json"): 
            with open(f'configs/{ctx.guild.id}configs.json', 'w') as f:
                f.write('{}')
        cdb = db(f"configs/{ctx.guild.id}configs.json")
        cdb.set("joinmessage", message)

    @config.command(name='joinurl')
    @commands.has_permissions(manage_guild=True)
    async def joinurlset(self, ctx, * , message:str):
        if not os.path.exists(f"configs/{ctx.guild.id}configs.json"): 
            with open(f'configs/{ctx.guild.id}configs.json', 'w') as f:
                f.write('{}')
        cdb = db(f"configs/{ctx.guild.id}configs.json")
        cdb.set("joinurl", message)

    @config.command(name='leavemessage')
    @commands.has_permissions(manage_guild=True)
    async def leavemset(self, ctx, * , message:str):
        if not os.path.exists(f"configs/{ctx.guild.id}configs.json"): 
            with open(f'configs/{ctx.guild.id}configs.json', 'w') as f:
                f.write('{}')
        cdb = db(f"configs/{ctx.guild.id}configs.json")
        cdb.set("leavemessage", message)

    @config.command(name='leaveurl')
    @commands.has_permissions(manage_guild=True)
    async def leaveurlset(self, ctx, * , message:str):
        if not os.path.exists(f"configs/{ctx.guild.id}configs.json"): 
            with open(f'configs/{ctx.guild.id}configs.json', 'w') as f:
                f.write('{}')
        cdb = db(f"configs/{ctx.guild.id}configs.json")
        cdb.set("leaveurl", message)

    @commands.command(name='prefix')
    async def prefixcom(self, ctx, * , prefix:str='get'):
        with open("prefixes.json") as json_file:
            keys = json.load(json_file)
        data = db('prefixes.json')
        if prefix != 'get':
            if ctx.author.guild_permissions.manage_guild:
                if len(prefix)>1:
                    await ctx.send(f"The bot does not support prefixes longer than 1 character (as in, the bot breaks), your prefix has been shortened to \"{prefix[0]}\"")
                data.set(str(ctx.guild.id), prefix[0])
            else:
                await ctx.send("You do not have permission to change this server's prefix.")
        else:
            if str(ctx.guild.id) in keys:
                await ctx.send(f"Prefix for **{ctx.guild.name}** is '{keys[str(ctx.guild.id)]}'")
            else:
                await ctx.send(f"**{ctx.guild.name}** does not have a custom prefix yet, set one with `.prefix newprefix`")

def setup(bot):
    bot.add_cog(Config(bot))