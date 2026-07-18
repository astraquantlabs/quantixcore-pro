import discord
from discord.ext import commands
import random

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message):
        """Make the bot repeat a message."""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def echo(self, ctx, *, message):
        await ctx.send(message)

    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(
            title="📊 Poll",
            description=question,
            color=discord.Color.blue()
        )

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command()
    async def choose(self, ctx, *, options):
        choices = [c.strip() for c in options.split(",")]

        if len(choices) < 2:
            return await ctx.send(
                "Usage: `pls choose option1, option2, option3`"
            )

        await ctx.send(f"🎲 I choose: **{random.choice(choices)}**")

    @commands.command()
    async def coinflip(self, ctx):
        await ctx.send(f"🪙 **{random.choice(['Heads', 'Tails'])}**")

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, sides: int = 6):
        if sides < 2:
            sides = 6

        await ctx.send(f"🎲 You rolled **{random.randint(1, sides)}**")

    @commands.command()
    async def randomnumber(self, ctx, minimum: int, maximum: int):
        if minimum >= maximum:
            return await ctx.send("Minimum must be smaller than maximum.")

        await ctx.send(
            f"🎲 {random.randint(minimum, maximum)}"
        )

    @commands.command()
    async def remind(self, ctx, minutes: int, *, reminder):
        if minutes <= 0:
            return await ctx.send("Minutes must be greater than 0.")

        await ctx.send(
            f"⏰ Reminder set for **{minutes}** minute(s)."
        )

        await discord.utils.sleep_until(
            discord.utils.utcnow() +
            discord.timedelta(minutes=minutes)
        )

        try:
            await ctx.author.send(
                f"⏰ Reminder:\n{reminder}"
            )
        except discord.Forbidden:
            await ctx.send(
                f"{ctx.author.mention} Reminder: {reminder}"
            )

    @commands.command()
    async def embed(self, ctx, *, text):
        embed = discord.Embed(
            description=text,
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def color(self, ctx):
        colour = discord.Color.random()

        embed = discord.Embed(
            title="Random Color",
            description=str(colour),
            color=colour
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))