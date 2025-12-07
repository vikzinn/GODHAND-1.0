import discord
from discord.ext import commands

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 50):
        """Limpa de 0 a 50 mensagens instantaneamente (default 50)"""
        if amount < 0 or amount > 50:
            await ctx.send("❌ Escolhe um valor entre 0 e 50 ")
            return
        # apaga o comando junto 
        deleted = await ctx.channel.purge(limit=amount+1, bulk=True)

        # feedback rpd que some
        confirm = await ctx.send(f" Limpei {len(deleted)-1} mensagens ")
        await confirm.delete(delay=2)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        """nuke"""
        channel = ctx.channel
        new_channel = await channel.clone(reason=f"nukado por {ctx.author}")
        await channel.delete()
        embed = discord.Embed(title="💥💥💥", color=discord.Color.red())
        embed.set_image(url="https://media.giphy.com/media/oe33xf3B50fsc/giphy.gif")
        await new_channel.send(embed=embed)

async def setup(bot):

    await bot.add_cog(Chat(bot))
