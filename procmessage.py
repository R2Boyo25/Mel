import discord # type: ignore
import random
from utils.funcs import *
from utils.jdb   import JSONDatabase as jdb

async def processMessage(message: discord.Message, bot: commands.Bot) -> None:
    pass # remove this line once you add custom handlers

    # add your own message handlers here.

    # Example

    # await xp(message) 

# example message handler thing
async def xp(message: discord.Message) -> None:
    if len(message.content) > 0:

        if message.content[0] in "!/\?|.,<{}[]-=+":
            return
        
    pxp = int(random.randint(5, 20) * 2)

    data = jdb("rank.json")

    a = str(message.author.id)

    if a in data.keys():
        fxp = data.get(a)['xp'] + pxp

        if fxp >= data.get(a)['rank'] ** (4 if data.get(a)['rank'] < 11 else 3):
            rank = data.get(a)['rank'] + 1

        else:
            rank = data.get(a)['rank']

        orank = data.get(a)['rank']
    
    else:

        orank = 1

        fxp = pxp

        rank = 1
    
    if orank < rank:

        await message.channel.send(f"Congratulations {message.author.mention}! You have leveled up to level {rank-1}!", delete_after=120)
    
    data.set(message.author.id, {'rank':rank, 'xp':fxp})
