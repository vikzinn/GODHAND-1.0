import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True   
intents.bans = True
intents.guilds = True    

bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    async with bot:
        await bot.load_extension("cogs.chat")
        await bot.load_extension("cogs.moderacao")
        await bot.start(TOKEN)
    
asyncio.run(main())
