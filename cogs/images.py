import discord
from discord.ext import commands
import time
import requests
import json
import random


class Images(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def inspirobot(self, ctx):
        """Gets a random image from the inspirobot website, I make no promises as to the content"""
        page = requests.get("http://inspirobot.me/api?generate=true")
        if page:
            imgurl = page.text
            embed = discord.Embed()
            embed.set_image(url=imgurl)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Page not found")

    @commands.command()
    async def cat(self, ctx):
        """Gets a random cat picture"""
        page = requests.get("https://api.thecatapi.com/v1/images/search")
        if page:
            text = page.text
            text_dict = json.loads(text)
            imgurl = (text_dict[0]["url"])
            embed = discord.Embed()
            # The image is sent in an embed because discord doesn't always show previews for links, but does always for embeds
            embed.set_image(url=imgurl)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Page not found")

    # TODO: Implement xkcd commands
