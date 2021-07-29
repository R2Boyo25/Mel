import discord
from discord.ext import commands
from utils.funcs import *
from database import Database as db
import subprocess

#Example Cog
class GitCog(commands.Cog):
    '''Git Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command("git")
    @commands.is_owner()
    async def git(self, ctx, * , command):

        try:

            if command.split()[0] == "commit":

                command2 = " ".join(command.split()[2:])
                command1 = "git commit -m".split() + [f'{command2}']

                a = subprocess.check_output("git commit -m".split() + [f'{command2}'.strip("\"")], timeout=5)

            else:

                command1 = ("git " + command).split()

                a = subprocess.check_output(("git " + command).split(), stderr=subprocess.STDOUT)

            b = a.decode().replace('```', '\`\`\`')

        except subprocess.CalledProcessError as exc:
            b = str(exc.returncode) + " " + exc.output.decode()

        embed = discord.Embed(title = " ".join(command1), description=f"```\n{b}\n```")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GitCog(bot))
    