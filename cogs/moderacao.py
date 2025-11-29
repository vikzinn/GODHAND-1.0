import discord
from discord.ext import commands

# View pra confirmação
class ConfirmBanView(discord.ui.View):
    def __init__(self, ctx, member, reason):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.member = member
        self.reason = reason
        self.confirmed = False

    @discord.ui.button(label="✅ Confirmar", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("Sem permisssão.", ephemeral=True)
        self.confirmed = True
        await interaction.response.edit_message(content=f"Ban confirmado: {self.member.mention}", view=None)
        self.stop()

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("Não mete o dedo aqui não.", ephemeral=True)
        await interaction.response.edit_message(content="Ban cancelado.", view=None)
        self.stop()


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        """Expulsa um membro do servidor"""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"👢 {member.mention} foi expulso. Motivo: {reason if reason else 'não informado'}")
        except Exception as e:
            await ctx.send(f"❌ Não consegui expulsar: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        """Bane um membro do servidor (com confirmação)"""
        try:
            view = ConfirmBanView(ctx, member, reason)
            msg = await ctx.send(
                f"{ctx.author.mention}, confirma que quer banir {member.mention}?\nMotivo: {reason if reason else 'não informado'}",
                view=view
            )
            view.message = msg
            await view.wait()

            if view.confirmed:
                await member.ban(reason=reason)
                await ctx.send(f"🔨 {member.mention} foi banido. Motivo: {reason if reason else 'não informado'}")
            else:
                await ctx.send("❌ Operação de ban cancelada.")
        except Exception as e:
            await ctx.send(f"❌ Não consegui banir: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"🔓 {user} foi desbanido.")
        except Exception as e:
            await ctx.send(f"❌ Não consegui desbanir: {e}")


async def setup(bot):
    await bot.add_cog(Mod(bot))