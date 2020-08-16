import asyncio

import discord
from discord.ext import commands
import time
import random
# Simple fun stuff, ie: text based
import requests
import random
from bs4 import BeautifulSoup


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command(aliases=["8ball"])
    # The star combines multiple arguments as one argument past that point
    async def _8ball(self, ctx, *, question):
        """Randomly returns an answer from responses to a given question"""
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @commands.command()
    async def cat_fact(self, ctx):
        """Gets a random cat fact"""
        page = requests.get("https://cat-fact.herokuapp.com/facts")
        if page:
            response = page.json()
            facts = response["all"]
            fact = random.choice(facts)["text"]
            await ctx.send(fact)
        else:
            await ctx.send("Page not found")

    @commands.command()
    async def anagram(self, ctx, *, words):
        """Gets an anagram of the given text"""
        # The site I use for this terrible and this a terrible way of doing it but I can't be bothered to make my own one
        if (len(words) < 6) or (len(words) > 30):
            # The site complains otherwise
            await ctx.send("That's too short, 7-30 letters is recommenced")
        else:
            formatted_word = "".join(["+" if i == " " else i for i in words])  # So the word can just be dropped into the url
            url = f"https://www.anagramgenius.com/server.php?source_text={formatted_word}&emphasis=1&gender=2&vulgar=0&seen=true"
            page = requests.get(url)
            if page:
                soup = BeautifulSoup(page.content, 'html.parser')
                results = soup.find('h3')  # Get the actual output part of the website
                if results:
                    text = " ".join(results.text.split("'"))  # Format the text nicely
                    try:
                        await ctx.send(text)
                    except discord.HTTPException:
                        await ctx.send("Sorry, an anagram could not be found. Try again or try some other words")
                else:
                    await ctx.send("Sorry, an anagram could not be found. Try again or try some other words")

            else:
                await ctx.send("Sorry, an anagram could not be found. Try again or try some other words")

    @commands.command()
    async def gangnamstyle(self, ctx):
        """Ethan wanted this, I blame him"""
        await ctx.send(random.choice(["https://tenor.com/view/psy-dance-horses-gangnam-style-music-gif-5419832", "https://media.tenor.com/images/786533a95e746b8a816c0bcf3cf1757c/tenor.gif"]))

    @commands.command()
    async def dance(self, ctx):
        """Dance!"""
        msg = await ctx.send("┏(・o･)┛")
        num = 0.5
        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await asyncio.sleep(num)
        await msg.edit(content="┏(・o･)┛")

        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await asyncio.sleep(num)
        await msg.edit(content="┏(・o･)┛")

        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await asyncio.sleep(num)
        await msg.edit(content="┏(・o･)┛")

        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await asyncio.sleep(num)
        await msg.edit(content="┏(・o･)┛")

        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await asyncio.sleep(num)
        await msg.edit(content="┏(・o･)┛")

        await asyncio.sleep(num)
        await msg.edit(content="┗ ( ･o･) ┓")

        await msg.delete()

    @commands.command(aliases=["dadjoke"])
    async def dad_joke(self, ctx, *, term=None):
        """Gets a random dad joke, or a dad joke about a particular thing"""
        if not term:
            response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"}).json()
            joke = response["joke"]
        elif term:
            response = requests.get(f"https://icanhazdadjoke.com/search?term={term}",
                                    headers={"Accept": "application/json"}).json()
            if response["results"]:
                joke = response["results"][0]["joke"]
            else:
                await ctx.send("Sorry, no joke found")
                return None

        await ctx.send(joke)

    @commands.command()
    async def cat1(self, ctx):
        """Cat dance"""
        await ctx.send("https://cdn.discordapp.com/attachments/586641157279186981/743077213783457822/image0.gif")

    @commands.command()
    async def cat2(self, ctx):
        """Rainbow cat dance"""
        await ctx.send("https://cdn.discordapp.com/attachments/586641157279186981/743108094682464297/image0-2-1.gif")

    @commands.command()
    async def cat3(self, ctx):
        """Cats dance"""
        await ctx.send("https://media.discordapp.net/attachments/685535901635706951/743516545442906212/image0.gif")

    @commands.command()
    async def emojify(self, ctx, *, text):
        """Turn  text into emojis"""
        emoji_dict = {
            "a": "🇦",
            "b": "🇧",
            "c": "🇨",
            "d": "🇩",
            "e": "🇪",
            "f": "🇫",
            "g": "🇬",
            "h": "🇭",
            "i": "🇮",
            "j": "🇯",
            "k": "🇰",
            "l": "🇱",
            "m": "🇲",
            "n": "🇳",
            "o": "🇴",
            "p": "🇵",
            "q": "🇶",
            "r": "🇷",
            "s": "🇸",
            "t": "🇹",
            "u": "🇺",
            "v": "🇻",
            "w": "🇼",
            "x": "🇽",
            "y": "🇾",
            "z": "🇿",
            "1": "1⃣",
            "2": "2⃣",
            "3": "3⃣",
            "4": "4⃣",
            "5": "5⃣",
            "6": "6⃣",
            "7": "7⃣",
            "8": "8⃣",
            "9": "9⃣",
            " ": " "
        }
        try:
            out = " ".join([emoji_dict[i] for i in text.lower()])
            await ctx.send(out)
        except KeyError as e:
            await ctx.send(f"You had an invalid character, {e}")


def setup(client):
    client.add_cog(Fun(client))
