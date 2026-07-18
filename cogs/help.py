import discord
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=180)
        self.embeds = embeds
        self.page = 0

    async def update(self, interaction):
        await interaction.response.edit_message(
            embed=self.embeds[self.page],
            view=self
        )

    @discord.ui.button(label="◀", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
        await self.update(interaction)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < len(self.embeds) - 1:
            self.page += 1
        await self.update(interaction)


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):

        pages = []

        page1 = discord.Embed(
            title="📖 NikkiBot Help (1/3)",
            color=0x5865F2
        )

        page1.add_field(
            name="Information",
            value="""
`pls help`
`pls ping`
`pls botinfo`
`pls avatar`
`pls user`
`pls server`
`pls uptime`
""",
            inline=False
        )

        pages.append(page1)

        page2 = discord.Embed(
            title="📖 NikkiBot Help (2/3)",
            color=0x5865F2
        )

        page2.add_field(
            name="Python",
            value="""
`pls docs`
`pls pep`
`pls pypi`
`pls resources`
`pls zen`
`pls charinfo`
`pls snowflake`
`pls source`
`pls eval`
`pls timeit`
""",
            inline=False
        )

        pages.append(page2)

        page3 = discord.Embed(
            title="📖 NikkiBot Help (3/3)",
            color=0x5865F2
        )

        page3.add_field(
            name="Utility",
            value="""
`pls remind`
`pls poll`
`pls choose`
`pls roll`
`pls coinflip`
`pls say`
`pls raw`
`pls rules`
`pls branding`
""",
            inline=False
        )

        pages.append(page3)

        await ctx.send(
            embed=pages[0],
            view=HelpView(pages)
        )


async def setup(bot):
    await bot.add_cog(Help(bot))