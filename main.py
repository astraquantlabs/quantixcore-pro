
import discord
from discord.ext import commands
import asyncio
import logging

from config import TOKEN, PREFIX

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.messages = True
intents.reactions = True
intents.presences = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None,
    case_insensitive=True
)

INITIAL_EXTENSIONS = [
    "cogs.help",
    "cogs.info",
    "cogs.utility",
    "cogs.python",
    "cogs.reminders",
    "cogs.moderation",
    "cogs.economy",
    "cogs.eval",
]


@bot.event
async def on_ready():
    print("=" * 50)
    print(f"Logged in as : {bot.user}")
    print(f"ID           : {bot.user.id}")
    print(f"Guilds       : {len(bot.guilds)}")
    print("=" * 50)

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Nikki Labs | !help"
        )
    )


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(
            "❌ Unknown command.\nUse `!help`."
        )

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(
            "❌ You don't have permission to use this command."
        )

    if isinstance(error, commands.BotMissingPermissions):
        return await ctx.send(
            "❌ I don't have the required permissions."
        )

    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(
            f"⏳ Try again in {error.retry_after:.1f}s."
        )

    raise error


async def load_extensions():
    for extension in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(extension)
            print(f"✅ Loaded {extension}")
        except Exception as e:
            print(f"❌ Failed to load {extension}")
            print(e)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())