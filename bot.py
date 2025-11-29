import discord
import asyncio
from config import TOKEN
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True   
intents.bans = True
intents.guilds = True    

bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    async with bot:
        await bot.load_extension("cogs.moderacao")
        await bot.load_extension("cogs.chat") 
        await bot.start(TOKEN)
    
asyncio.run(main())
