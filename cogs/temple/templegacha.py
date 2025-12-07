import discord
import json
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(name= "pull")
    async def pull(self, ctx):
        with open("personagens.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        resultado = random.choice(data["personagens"])
        await ctx.send(f"voce tirou o {resultado}")
async def setup(bot):
    await bot.add_cog(Gacha(bot))
