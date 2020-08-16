import discord
from discord.ext import commands
import time
from PIL import Image, ImageOps, ImageFilter
from io import BytesIO
import requests


# Stuff using pillow
# TODO: Look into improving this, its a bit messy


async def get_pfp(member: discord.Member):
    """Gets the pfp of the user as a png"""
    img = member.avatar_url_as(format="png")
    img = await img.read()
    return img


async def send_image(image, ctx, filename="image.png"):
    """Converts the pfp into a byte stream? I think? I know it turns it into something PIL can use"""
    # This code was stolen from a friend
    image_b = BytesIO()
    image.save(image_b, format="png")
    image_b.seek(0)
    await ctx.send(file=discord.File(image_b, filename=filename))


class profilePictures(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def pfp(self, ctx, user: discord.Member = None):
        """Gets the pfp of the user, or a specified user"""
        if user is None:
            user = ctx.author

        # Send the image as an embed because links don't always expand
        embed = discord.Embed(title=f"Profile picture of {user}")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def pfp_roll(self, ctx, angle=180, user=None):
        """Rotates the profile picture of the user"""
        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        out = image.rotate(int(angle))
        await send_image(out, ctx)

    @commands.command()
    async def pfp_blur(self, ctx, user: discord.Member = None):
        """Blurs the profile picture of the user"""
        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        out = image.filter(ImageFilter.BLUR)
        await send_image(out, ctx)

    @commands.command()
    async def pfp_greyscale(self, ctx, user: discord.Member = None):
        """Creates a greyscale version of the user's pfp"""
        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        out = image.convert('L')
        await send_image(out, ctx)

    @commands.command()
    async def pfp_filter(self, ctx, a_filter="blur", user: discord.Member = None):
        """"Applies a filter to the user's pfp, defaults to blur"""
        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        a_filter = a_filter.upper()

        filters = {
            "BLUR": ImageFilter.BLUR,
            "CONTOUR": ImageFilter.CONTOUR,
            "DETAIL": ImageFilter.DETAIL,
            "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
            "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
            "EMBOSS": ImageFilter.EMBOSS,
            "FIND_EDGES": ImageFilter.FIND_EDGES,
            "SMOOTH": ImageFilter.SMOOTH,
            "SMOOTH_MORE": ImageFilter.SMOOTH_MORE,
            "SHARPEN": ImageFilter.SHARPEN
        }

        out = image.filter(filters[a_filter])
        await send_image(out, ctx)

    @commands.command()
    async def pfp_invert(self, ctx, user: discord.Member = None):
        """Invert's the colours of the user's pfp"""
        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        image = image.convert('RGB')

        out = ImageOps.invert(image)
        await send_image(out, ctx)

    @commands.command()
    async def pfp_blur_edges(self, ctx, user: discord.Member = None):
        """Blurs the edges of the pfp"""
        # Stolen from a tutorial

        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        # blur radius and diameter
        radius, diameter = 20, 40
        # open an image
        img = image
        # Paste image on white background
        background_size = (img.size[0] + diameter, img.size[1] + diameter)
        background = Image.new('RGB', background_size, (255, 255, 255))
        background.paste(img, (radius, radius))
        # create new images with white and black
        mask_size = (img.size[0] + diameter, img.size[1] + diameter)
        mask = Image.new('L', mask_size, 255)
        black_size = (img.size[0] - diameter, img.size[1] - diameter)
        black = Image.new('L', black_size, 0)
        # create blur mask
        mask.paste(black, (diameter, diameter))
        # Blur image and paste blurred edge according to mask
        blur = background.filter(ImageFilter.GaussianBlur(radius / 2))
        background.paste(blur, mask=mask)

        out = background
        await send_image(out, ctx)


def setup(client):
    client.add_cog(profilePictures(client))
