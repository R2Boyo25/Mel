import discord # type: ignore
from discord.ext import commands # type: ignore
from utils.funcs import *
import subprocess

#Example Cog
class GitCog(commands.Cog):
    '''Git Commands'''
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("git")
    @commands.is_owner()
    async def git(self, ctx: commands.Context, *, command: str) -> None:
        try:
            command1 = ("git " + command).split()

            a = subprocess.check_output(("git " + command).split(), stderr=subprocess.STDOUT)

            b = a.decode().replace('```', '\`\`\`')

        except subprocess.CalledProcessError as exc:
            b = str(exc.returncode) + " " + exc.output.decode()

        embed = discord.Embed(title = " ".join(command1), description=f"```\n{b}\n```")

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GitCog(bot))
    
