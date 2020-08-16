import asyncio
import discord
from discord.ext import commands
import time
import wikipedia
import reverse_geocoder as rg


async def get_page(title: str) -> wikipedia.WikipediaPage:
    try:
        page = wikipedia.page(title, auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        print("DisambiguationError")
        print(e.options)
        print(e.options[0])
        # Todo: fix this
        page = await get_page(e.options[1])
    if page is None:
        raise wikipedia.WikipediaException
    return page


async def format_page(page: wikipedia.WikipediaPage) -> discord.Embed:
    embed = discord.Embed(title=page.title, description=page.summary[:252]+"...")
    try:
        embed.set_thumbnail(url=page.images[0])
    except IndexError:
        pass
    embed.url = page.url
    return embed


class WikiCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.group(invoke_without_command=True, aliases=["wikipedia"])
    async def wiki(self, ctx, *, term):
        search_command: commands.Command = self.wiki.get_command("search")
        await ctx.invoke(search_command, term=term)

    @wiki.command(aliases=["s", "find"])
    async def search(self, ctx, *, term):
        suggested_titles = wikipedia.search(term, results=5)

        if not suggested_titles:
            await ctx.send("Sorry, no page was found.")
            return None

        def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❎")

        final_title = None

        for title in suggested_titles:
            check_message: discord.Message = await ctx.send(f"Got page for `{title}`. Is this the page you wanted?")
            await check_message.add_reaction("✅")
            await check_message.add_reaction("❎")

            try:
                response_reaction, user = await self.client.wait_for("reaction_add", timeout=10.0, check=check)

            except asyncio.TimeoutError:
                await ctx.send("Sorry, you took too long to respond.")
                return None

            if str(response_reaction.emoji) == "✅":
                final_title = title
                break

            elif str(response_reaction.emoji) == "❎":
                await ctx.send("Ok")
                pass

        if final_title is not None:
            page = await get_page(final_title)
            embed = await format_page(page)
            await ctx.send(embed=embed)

        elif final_title is None:
            await ctx.send("Well then. Try searching again.")
            return None

    @wiki.command(aliases=["rand", "r", "random"])
    async def random_page(self, ctx):
        title = wikipedia.random()
        page = await get_page(title)
        embed = await format_page(page)
        await ctx.send(embed=embed)

    @wiki.command(aliases=["whereis", "where", "w"])
    async def where_is(self, ctx, *, term):
        title = wikipedia.search(term, results=1)[0]
        page = await get_page(title)
        try:
            if page.coordinates is not None:
                results = rg.search(page.coordinates, mode=1)[0]
                name = results["name"]
                area = results["admin2"]
                country = results["admin1"]
                locations = [i for i in [name, area, country] if i]
                location = ", ".join(locations)
                await ctx.send(f"`{page.title}` is here: `{location}`.")
            else:
                await ctx.send("That page doesn't have a location, sorry.")
        except KeyError:
            await ctx.send("That page doesn't have a location, sorry.")


def setup(client):
    client.add_cog(WikiCommands(client))
