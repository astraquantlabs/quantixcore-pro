import discord
from discord.ext import commands
import platform
import datetime
import time

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! `{latency}ms`")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar",
            color=discord.Color.blurple()
        )
        embed.set_image(url=member.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(
            title=f"{member}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blurple()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Bot", value=member.bot)
        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(member.created_at, "F"),
            inline=False
        )

        if isinstance(member, discord.Member):
            embed.add_field(
                name="Joined",
                value=discord.utils.format_dt(member.joined_at, "F"),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        guild = ctx.guild

        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.green()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(guild.created_at, "F"),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        uptime = int(time.time() - self.start_time)

        embed = discord.Embed(
            title="NikkiBot",
            color=discord.Color.blurple()
        )

        embed.add_field(name="Python", value=platform.python_version())
        embed.add_field(name="discord.py", value=discord.__version__)
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(self.bot.users))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency*1000)}ms")
        embed.add_field(name="Uptime", value=f"{uptime}s")

        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        uptime = int(time.time() - self.start_time)
        await ctx.send(f"⏱️ Uptime: **{uptime} seconds**")

    @commands.command()
    async def charinfo(self, ctx, *, text):
        embed = discord.Embed(
            title="Character Info",
            color=discord.Color.orange()
        )

        lines = []

        for c in text[:25]:
            lines.append(f"`{c}` → U+{ord(c):04X}")

        embed.description = "\n".join(lines)

        await ctx.send(embed=embed)

    @commands.command()
    async def snowflake(self, ctx, snowflake: int):
        discord_epoch = 1420070400000
        timestamp = ((snowflake >> 22) + discord_epoch) / 1000
        created = datetime.datetime.fromtimestamp(
            timestamp,
            tz=datetime.timezone.utc
        )

        embed = discord.Embed(
            title="Snowflake Information",
            color=discord.Color.blurple()
        )

        embed.add_field(name="ID", value=snowflake, inline=False)
        embed.add_field(
            name="Created",
            value=discord.utils.format_dt(created, "F"),
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))