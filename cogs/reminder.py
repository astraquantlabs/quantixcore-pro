import discord
from discord.ext import commands
import asyncio


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="remind",
        aliases=["reminder", "timer"]
    )
    async def remind(self, ctx, minutes: int, *, reminder: str):
        """Set a reminder."""

        if minutes < 1:
            return await ctx.send(
                "❌ Time must be at least 1 minute."
            )

        if minutes > 10080:
            return await ctx.send(
                "❌ Maximum reminder time is 7 days (10080 minutes)."
            )

        embed = discord.Embed(
            title="⏰ Reminder Set",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Time",
            value=f"{minutes} minute(s)",
            inline=False
        )

        embed.add_field(
            name="Reminder",
            value=reminder,
            inline=False
        )

        await ctx.send(embed=embed)

        await asyncio.sleep(minutes * 60)

        reminder_embed = discord.Embed(
            title="⏰ Reminder",
            description=reminder,
            color=discord.Color.gold()
        )

        try:
            await ctx.author.send(embed=reminder_embed)
        except discord.Forbidden:
            await ctx.send(
                f"{ctx.author.mention}",
                embed=reminder_embed
            )

    @commands.command()
    async def timers(self, ctx):
        """Placeholder for future persistent reminders."""
        await ctx.send(
            "ℹ️ Persistent reminder storage is not implemented yet."
        )


async def setup(bot):
    await bot.add_cog(Reminders(bot))