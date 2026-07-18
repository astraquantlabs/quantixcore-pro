
import asyncio

@commands.command()
async def remind(self, ctx, minutes: int, *, reminder: str):
    """Set a reminder and DM the user when the time is up."""

    if minutes < 1:
        return await ctx.send("❌ Time must be at least 1 minute.")

    if minutes > 10080:  # 7 days
        return await ctx.send("❌ Maximum reminder time is 10080 minutes (7 days).")

    embed = discord.Embed(
        title="⏰ Reminder Set",
        description=f"**Reminder:** {reminder}",
        color=discord.Color.gold()
    )
    embed.add_field(name="Time", value=f"{minutes} minute(s)")
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
        await ctx.send(f"{ctx.author.mention}", embed=reminder_embed)