import discord
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def ping(self, ctx):
        """Returns the response time of the bot in ms"""
        await ctx.send(f"Pong! `{round(self.client.latency * 1000)}ms`")


def setup(client):
    client.add_cog(Utility(client))
