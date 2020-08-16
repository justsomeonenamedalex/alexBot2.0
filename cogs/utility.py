import discord
from discord.ext import commands
import time
import asyncio
from GoogleNews import GoogleNews
from tinydb import TinyDB, Query
import wikipedia
import random
from googletrans import Translator


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def ping(self, ctx):
        """Returns the response time of the bot in ms"""
        await ctx.send(f"Pong! `{round(self.client.latency * 1000)}ms`")

    @commands.command(aliases=["reminder"])
    async def remind(self, ctx, time_minutes: float, *, text):
        """Creates a reminder that will be sent after n minutes"""
        time_seconds = abs(time_minutes) * 60
        await ctx.send(f"Created reminder for {ctx.author.mention}:\n`{text}`\nWhich will be sent in {time_minutes} minutes.")
        await asyncio.sleep(time_seconds)
        await ctx.send(f"{ctx.author.mention}, I'm reminding you:\n`{text}`")

    @commands.command()
    async def news(self, ctx, *, search):
        """Gets the top google news result for a specific search over the past day"""
        # Todo make this an embed, maybe have it change pages, use eve's stuff from teabot(maybe sudos's code?)
        async with ctx.typing():

            google_news = GoogleNews()
            google_news.setlang("en")
            google_news.setperiod("d")
            google_news.search(search)
            results = google_news.result()
            print(google_news.result())

            articles = results[:5]

            try:
                article = articles[0]
                embed = discord.Embed(title=article["title"], description=article["desc"], url=article["link"])
                embed.set_image(url=article["img"])
                await ctx.send(embed=embed)
            except IndexError:
                await ctx.send("Sorry, no articles found")

    @commands.command()
    async def poll(self, ctx, title: str, *args):
        """Creates a poll than can be voted upon with reactions"""
        options = args
        emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
        lines = []

        if len(options) > 9:
            await ctx.send("Sorry, there is a maximum of 9 options")
            return None

        # Generates the description based on the number if options
        for x, i in enumerate(options):
            lines.append(f"{emojis[x]} : `{i}`")

        desc = "\n".join(lines)
        embed = discord.Embed(title=title, description=desc)
        poll_message = await ctx.send(embed=embed)

        # Adds a reaction for each option
        for x, i in enumerate(options):
            await poll_message.add_reaction(emojis[x])

    @commands.command()
    async def rain(self, ctx):
        """Link to spotify rain sounds playlist"""
        await ctx.send("https://open.spotify.com/playlist/37i9dQZF1DX8ymr6UES7vc?si=OGy4WO69Q6Gacpg5WYREPw")

    @commands.command()
    async def white_noise(self, ctx):
        """Link to spotify white noise playlist"""
        await ctx.send("https://open.spotify.com/playlist/37i9dQZF1DWUZ5bk6qqDSy?si=w9vqzloJQLOlyIKTFkXKAg")

    @commands.command()
    async def loading(self, ctx):
        """Simple loading bar animation, because why not"""
        # TODO: FInd a way to fix the sizes of characters in discord, as these still don't match
        space_char = "—"
        done_char = "▇"
        total = 10  # Total number of spaces, could be changed for longer/shorter bars
        spaces = total
        done = 0

        bar = f"[{done_char * done}{space_char * spaces}] {done * 10}%"
        msg = await ctx.send(bar)
        await asyncio.sleep(1)

        # Increase the number of done spaces, and decrease the number of empty spaces

        for i in range(total):
            done += 1
            spaces -= 1
            bar = f"[{done_char * done}{space_char * spaces}] {done * 10}%"
            await msg.edit(content=bar)
            await asyncio.sleep(1)

    @commands.command()
    async def translate(self, ctx, txt, dest=None):
        """Translates the given phrase into another language using google translate"""
        # If destination language isn't specified, assume the destination is english
        try:
            if dest is None:
                translated = self.translator.translate(txt)
                response = translated.text
                src = translated.src
                dest = translated.dest
            else:
                translated = self.translator.translate(txt, dest=dest.lower())
                response = translated.text
                src = translated.src
                dest = translated.dest

            await ctx.send(f"`{response}` Translated from {src} to {dest}.")
        except ValueError:
            await ctx.send("Invalid destination, destinations should be two letter version of the language\nEg: es, fr, en")


def setup(client):
    client.add_cog(Utility(client))
