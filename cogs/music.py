import discord
from discord.ext import commands
import time
import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
import re

from util import spotify as spotify_util


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config
        self.genius = lyricsgenius.Genius(self.config["lyricsgenius_key"])
        self.spotify = spotify_util.Spotify(client_id=self.config["spotify_id"], client_secret=self.config["spotify_secret"])
        self.spotipy_client = self.spotify.sp

    @commands.command()
    async def lyrics(self, ctx, *, song):
        """Gets the lyrics of a specified song"""
        search = self.genius.search_song(song)
        try:
            parts = search.lyrics.split("\n\n")  # Otherwise the lyrics are far too long to put in one message
            for part in parts:
                await ctx.send(part)
        except AttributeError:
            await ctx.send("Song not found, try again or search something else.")

    @commands.command()
    async def song(self, ctx, *, text):
        """Gets the open spotify link for the first result of the given search"""
        links = self.sp.search_songs(text)

        if links is None:
            await ctx.send("Something went wrong, sorry")

        if links:
            await ctx.send(links[0])
        else:
            await ctx.send("Sorry, the song wasn't found")

    @commands.command()
    async def album(self, ctx, *, text):
        """Gets the open spotify link for the first result of the given search"""
        links = self.sp.search_albums(text)

        if links is None:
            await ctx.send("Something went wrong, sorry")

        if links:
            await ctx.send(links[0])
        else:
            await ctx.send("Sorry, the album wasn't found")

    @commands.command()
    async def artist(self, ctx, *, text):
        """Gets the open spotify link for the first result of the given search"""
        links = self.sp.search_artists(text)

        if links is None:
            await ctx.send("Something went wrong, sorry")

        if links:
            await ctx.send(links[0])
        else:
            await ctx.send("Sorry, the artist wasn't found")