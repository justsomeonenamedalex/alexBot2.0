import discord
from discord.ext import commands
import requests
import random
import reverse_geocoder as rg
import time
import math
import json


class Nasa(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config
        self.api_key = self.config["nasa_key"]

    @commands.command()
    async def apod(self, ctx):
        """Gets the astronomy picture of the day from nasa"""
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}"
        r = requests.get(url)
        if r:
            r_url = r.json()['url']
            await ctx.send(r_url)
        else:
            await ctx.send("Page not found")

    @commands.command()
    async def mars(self, ctx):
        """Gets a random picture of mars"""
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={self.api_key}"
        page = requests.get(url)
        if page:
            photos = page.json()["photos"]
            photo = random.choice(photos)["img_src"]
            await ctx.send(photo)
        else:
            await ctx.send("Page not found")

    @commands.command()
    async def iss(self, ctx):
        """Gets the current latitude and longitude of the iss, as well as its location"""
        page = requests.get("http://api.open-notify.org/iss-now.json")
        if page:
            response = page.json()
            latitude = response["iss_position"]["latitude"]
            longitude = response["iss_position"]["longitude"]

            coords = (float(latitude), float(longitude))
            # Use reverse geocoder to get the location of the iss from the latitude and longitude
            # I don't know how this works, it's magic afaik
            try:
                results = rg.search(coords, mode=1)[0]
                name = results["name"]
                area = results["admin2"]
                country = results["admin1"]
                locations = [i for i in [name, area, country] if i]
                location = ", ".join(locations)
                location_text = f", above {location}"
            except:
                # I have no idea what errors this could throw because the library doesnt have much documentation
                location_text = "."

            text = f"The ISS is currently at {latitude}, {longitude}" + location_text
            await ctx.send(text)
        else:
            await ctx.send("Page not found")

    # TODO get this working maybe?
    # @commands.command()
    # async def neo(self, ctx):
    #     url = "https://api.nasa.gov/neo/rest/v1/feed"
    #     params = {
    #         'api_key': self.api_key,
    #         'start_date': str(date.today()),
    #         'end_date': str(date.today())
    #     }
    #     response = requests.get(url, params=params).json()
    #     f = open("neo.txt", "w")
    #     f.write(str(response))
    #     f.close()
    #     neo = response["near_earth_objects"]

    @commands.command(aliases=["moonphase", "moon_phase"])
    async def moon(self, ctx):
        """Gets current data on the moon"""
        # This api is the most random thing i've found for this bot, so I wouldn't be surprised if it goes down
        # TODO: read up on how the api works and recreate it in python
        # https://github.com/FarmSense/Astro-Widget/blob/master/astro_widget.js
        date = math.floor(time.time())
        url = f"http://api.farmsense.net/v1/moonphases/?d={date}&callback=window.randName.f.moonPhase.parseRequest"
        page = requests.get(url)
        # TODO: do this with regex, even if it hurts my soul to do so
        page_split_one = page.text.split("(")[1]
        page_split_two = page_split_one.split(")")[0]
        page = page_split_two[1:-1]
        if page:
            data = json.loads(page)
            e = discord.Embed(title="The Moon", description="Y'know, that thing", color=discord.Color.purple())
            e.add_field(name="Full moon name:", value="\n".join(data["Moon"]), inline=False)
            e.add_field(name="Phase of moon:", value=data["Phase"], inline=False)
            await ctx.send(embed=e)
        else:
            await ctx.send("Page could not be found")


def setup(client):
    client.add_cog(Nasa(client))
