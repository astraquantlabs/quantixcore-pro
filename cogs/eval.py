import discord
from discord.ext import commands
import contextlib
import io
import traceback


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", aliases=["e"])
    @commands.is_owner()
    async def eval_command(self, ctx, *, code: str):
        """Execute Python code (Bot owner only)."""

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "discord": discord,
            "commands": commands,
            "__builtins__": __builtins__,
        }

        # Remove code blocks
        if code.startswith("```") and code.endswith("```"):
            code = "\n".join(code.split("\n")[1:-1])

        body = (
            "async def _eval():\n"
            + "\n".join(f"    {line}" for line in code.split("\n"))
        )

        stdout = io.StringIO()

        try:
            exec(body, env)

            with contextlib.redirect_stdout(stdout):
                result = await env["_eval"]()

            output = stdout.getvalue()

            if result is not None:
                output += repr(result)

            if not output:
                output = "Executed successfully."

            embed = discord.Embed(
                title="✅ Eval Output",
                description=f"```py\n{output[:4000]}\n```",
                color=discord.Color.green()
            )

            await ctx.send(embed=embed)

        except Exception:
            error = traceback.format_exc()

            embed = discord.Embed(
                title="❌ Eval Error",
                description=f"```py\n{error[:4000]}\n```",
                color=discord.Color.red()
            )

            await ctx.send(embed=embed)

    @eval_command.error
    async def eval_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("❌ Only the bot owner can use this command.")
        else:
            raise error


async def setup(bot):
    await bot.add_cog(Eval(bot))