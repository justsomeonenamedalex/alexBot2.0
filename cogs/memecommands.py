import asyncio

import discord
from discord.ext import commands
import requests
import random


class MemeCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

        # Get the list of the top 100 memes, and format them into a dictionary and a useable list
        data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
        self.images = [{'name': image['name'], 'url': image['url'], 'id': image['id']} for image in data]
        self.meme_list = []
        for n, img in enumerate(self.images):
            self.meme_list.append((n+1, img['name']))
        self.meme_ids = [i["id"] for i in self.images]

    @commands.command()
    async def memes(self, ctx):
        """Gets the list of memes ids"""
        memes_one = self.meme_list[:50]
        memes_two = self.meme_list[50:]
        msg_one = await ctx.send(memes_one)
        msg_two = await ctx.send(memes_two)
        await asyncio.sleep(20)
        await msg_one.edit(
            content="This message has been deleted to reduce spam, to get a new list of memes, use:\n`.memes`")
        await msg_two.delete()

    @commands.command()
    async def meme(self, ctx, meme_id="1", *args):

        imgflip_username = self.config["imgflip_username"]
        imgflip_password = self.config["imgflip_password"]

        """Creates a meme with a template specified by the meme_id, and with text boxes specifed by the other arguments"""
        url = 'https://api.imgflip.com/caption_image'

        meme_template_id = self.images[int(meme_id) - 1]['id']
        if args:
            text = args[0]
        else:
            text = "TEXT"

        params = {
            'username': imgflip_username,
            'password': imgflip_password,
            'template_id': meme_template_id,
            'boxes[0][text]': text
        }

        # This adds a new text box for each extra argument, to account for templates with varying numbers of text boxes
        if args:
            for i, arg in enumerate(args):
                box = f'boxes[{i}][text]'
                params[box] = arg

        with ctx.typing():
            response = requests.request('POST', url, params=params).json()  # Creates the meme
            print(response)
            if response:
                try:
                    img_url = response['data']['url']

                    # Again, the image is sent in an embed because discord doesn't always show previews for links, but does always for embeds
                    embed = discord.Embed(title="Meme :)", url=img_url)
                    embed.set_image(url=img_url)
                    await ctx.send(embed=embed)
                except KeyError as e:
                    await ctx.send("Something went wrong, sorry")
            else:
                await ctx.send("Sorry, page not found")

    @commands.command()
    async def server_meme(self, ctx, channel: discord.TextChannel = None, num: int = 3555):
        """Creates a random meme from messages in a channel"""

        imgflip_username = self.config["imgflip_username"]
        imgflip_password = self.config["imgflip_password"]

        with ctx.typing():
            if channel is None:
                channel = ctx.channel

            # Get the messages
            messages = []
            async for message in channel.history(limit=num):
                if not(message.content.startswith(".")) and not(message.author.bot):
                    messages.append(message.content)

            meme_id = random.choice(self.meme_ids)
            top_text = random.choice(messages)
            bottom_text = random.choice(messages)

            url = 'https://api.imgflip.com/caption_image'
            params = {
                'username': imgflip_username,
                'password': imgflip_password,
                'template_id': meme_id,
                'text0': top_text,
                'text1': bottom_text
            }

            response = requests.request('POST', url, params=params).json()  # Creates the meme
            if response:
                img_url = response['data']['url']

                # Again, the image is sent in an embed because discord doesn't always show previews for links, but does always for embeds
                embed = discord.Embed(title="Meme :)", url=img_url)
                embed.set_image(url=img_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Sorry, page not found")

    @commands.command()
    async def bug(self, ctx, *, text):
        """Creates a cool bug fact. This isn't in the top 100 memes so I had to add it manually"""
        # TODO: look into making something that could get the template id for any meme based on a search

        imgflip_username = self.config["imgflip_username"]
        imgflip_password = self.config["imgflip_password"]


        url = 'https://api.imgflip.com/caption_image'
        params = {
            'username': imgflip_username,
            'password': imgflip_password,
            'template_id': "230178883",
            'text0': text,

        }
        with ctx.typing():
            response = requests.request('POST', url, params=params).json()  # Creates the meme
            print(response)
            if response:
                try:
                    img_url = response['data']['url']

                    # Again, the image is sent in an embed because discord doesn't always show previews for links, but does always for embeds
                    embed = discord.Embed(title="Bug", url=img_url)
                    embed.set_image(url=img_url)
                    await ctx.send(embed=embed)
                except KeyError as e:
                    await ctx.send("Something went wrong, sorry")
            else:
                await ctx.send("Sorry, page not found")


def setup(client):
    client.add_cog(MemeCommands(client))
