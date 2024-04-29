import random

import discord
from discord.ext import commands

from mel.utils.funcs import *
from mel.utils.jdb import JSONDatabase as jdb


async def processMessage(message: discord.Message, bot: commands.Bot) -> None:
    ...  # remove this line once you add custom handlers

    # add your own message handlers here.
    # await handle_xp(message)


async def handle_xp(message: discord.Message) -> None:
    if len(message.content) > 0 and message.content[0] in "!/\?|.,<{}]-=+":
        return

    def should_rank_up(current_xp: int, rank: int) -> bool:
        return current_xp >= rank ** (4 if rank < 11 else 3)

    gained_xp = random.randint(5, 20) * 2
    data = jdb("rank.json")

    if str(message.author.id) in data.keys():
        author = data.get(str(message.author.id))
        current_xp = author["xp"] + gained_xp
        old_rank: int = author["rank"]
        rank: int = old_rank

        if should_rank_up(current_xp, rank):
            rank += 1

    else:
        old_rank = 1
        current_xp = gained_xp
        rank = 1

    if old_rank < rank:
        await message.channel.send(
            f"Congratulations {message.author.mention}! You have leveled up to level {rank-1}!",
            delete_after=120,
        )

    data.set(message.author.id, {"rank": rank, "xp": current_xp})
