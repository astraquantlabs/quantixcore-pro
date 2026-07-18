import discord
from discord.ext import commands
import aiohttp
import timeit
import io
import contextlib
import traceback
import unicodedata


class Python(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def docs(self, ctx, *, query=None):
        """Search Python documentation."""
        if not query:
            return await ctx.send("https://docs.python.org/3/")

        url = f"https://docs.python.org/3/search.html?q={query}"
        embed = discord.Embed(
            title="Python Documentation",
            description=f"Search results for **{query}**",
            url=url,
            color=0x3776AB
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def pypi(self, ctx, package=None):
        """Look up a package on PyPI."""
        if not package:
            return await ctx.send("Usage: `pls pypi <package>`")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://pypi.org/pypi/{package}/json"
            ) as resp:

                if resp.status != 200:
                    return await ctx.send("Package not found.")

                data = await resp.json()

        info = data["info"]

        embed = discord.Embed(
            title=f"{info['name']} {info['version']}",
            description=info.get("summary") or "No description.",
            url=info["package_url"],
            color=0x3776AB
        )

        embed.add_field(
            name="Python",
            value=info.get("requires_python") or "Unknown"
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def pep(self, ctx, number: int):
        """Open a Python Enhancement Proposal."""
        url = f"https://peps.python.org/pep-{number:04d}/"

        embed = discord.Embed(
            title=f"PEP {number}",
            url=url,
            description=url,
            color=0x3776AB
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def zen(self, ctx):
        """Show the Zen of Python."""
        zen = (
            "Beautiful is better than ugly.\n"
            "Explicit is better than implicit.\n"
            "Simple is better than complex.\n"
            "Complex is better than complicated.\n"
            "Readability counts."
        )

        embed = discord.Embed(
            title="The Zen of Python",
            description=f"```{zen}```",
            color=0x3776AB
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def charinfo(self, ctx, *, text):
        """Unicode information."""
        if len(text) > 25:
            return await ctx.send("Maximum 25 characters.")

        lines = []

        for c in text:
            lines.append(
                f"`{c}` → U+{ord(c):04X} • {unicodedata.name(c,'UNKNOWN')}"
            )

        await ctx.send("\n".join(lines))

    @commands.command()
    async def timeit(self, ctx, *, code):
        """Benchmark a Python expression."""

        try:
            result = timeit.timeit(code, number=100)
            await ctx.send(
                f"Executed 100 runs in `{result:.6f}` seconds."
            )
        except Exception as e:
            await ctx.send(f"Error:\n```{e}```")

    @commands.command(name="e", aliases=["eval"])
    @commands.is_owner()
    async def eval_cmd(self, ctx, *, code):
        """Owner-only Python evaluator."""

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "discord": discord
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(code, env)

            output = stdout.getvalue()

            if not output:
                output = "Executed successfully."

            await ctx.send(f"```py\n{output[:1900]}\n```")

        except Exception:
            await ctx.send(
                f"```py\n{traceback.format_exc()[:1900]}\n```"
            )


async def setup(bot):
    await bot.add_cog(Python(bot))