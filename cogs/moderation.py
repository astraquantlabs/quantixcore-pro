import discord
from discord.ext import commands
from datetime import timedelta


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.guild is not None

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Delete messages."""

        if amount < 1:
            return await ctx.send("Amount must be at least 1.")

        await ctx.channel.purge(limit=amount + 1)

        msg = await ctx.send(f"✅ Deleted {amount} messages.")
        await msg.delete(delay=5)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked **{member}**")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned **{member}**")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned **{user}**")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):

        if minutes < 1:
            return await ctx.send("Minutes must be at least 1.")

        await member.timeout(
            timedelta(minutes=minutes),
            reason=reason
        )

        await ctx.send(
            f"⏳ Timed out **{member}** for **{minutes} minutes**."
        )

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"✅ Removed timeout from **{member}**")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):

        if seconds < 0 or seconds > 21600:
            return await ctx.send(
                "Slowmode must be between 0 and 21600 seconds."
            )

        await ctx.channel.edit(slowmode_delay=seconds)

        await ctx.send(f"🐌 Slowmode set to **{seconds}s**")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False

        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            overwrite=overwrite
        )

        await ctx.send("🔒 Channel locked.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None

        await ctx.channel.set_permissions(
            ctx.guild.default_role,
            overwrite=overwrite
        )

        await ctx.send("🔓 Channel unlocked.")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nickname=None):
        await member.edit(nick=nickname)
        await ctx.send(f"✏️ Nickname updated for **{member}**")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, *, role: discord.Role):

        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"➖ Removed **{role.name}** from {member.mention}")
        else:
            await member.add_roles(role)
            await ctx.send(f"➕ Added **{role.name}** to {member.mention}")

    @kick.error
    @ban.error
    @purge.error
    @timeout.error
    @untimeout.error
    @slowmode.error
    @lock.error
    @unlock.error
    @nick.error
    @role.error
    async def permission_error(self, ctx, error):

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Member not found.")

        elif isinstance(error, commands.RoleNotFound):
            await ctx.send("❌ Role not found.")

        else:
            raise error


async def setup(bot):
    await bot.add_cog(Moderation(bot))