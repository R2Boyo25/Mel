import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db

class GitCog(commands.Cog):
    '''Git Commands'''
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(GitCog(bot))
    