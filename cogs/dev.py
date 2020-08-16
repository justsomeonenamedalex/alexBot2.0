import discord
from discord.ext import commands


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.is_owner()
    @commands.command(hidden=True)
    async def load(self, ctx, extension: str):
        """Loads a cog"""
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded.")

        except commands.NoEntryPointError as e:
            # Runs if the cog has no entry point
            # Not sure if I need this but I might as well cover everything
            await ctx.send(f"Extension {e.name} has no entry point.")

        except commands.ExtensionFailed as e:
            # Runs if there is an error in the code
            await ctx.send(f"Failed to load extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionAlreadyLoaded as e:
            await ctx.send(f"Extension {e.name} is already loaded.")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload(self, ctx, extension: str):
        """Unloads a cog"""
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded.")

        except commands.ExtensionFailed as e:
            # Runs if there is an error in the code
            await ctx.send(f"Failed to unload extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionNotLoaded as e:
            await ctx.send(f"Extension {e.name} is not loaded")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def reload(self, ctx, extension: str):
        """Unloads, then loads a cog"""
        # Unload the cog
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded.")

        except commands.ExtensionFailed as e:
            await ctx.send(f"Failed to unload extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionNotLoaded as e:
            await ctx.send(f"Extension {e.name} is not loaded")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

        # Load the cog
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded.")

        except commands.NoEntryPointError as e:
            # Not sure if I need this but I might as well cover everything
            await ctx.send(f"Extension {e.name} has no entry point.")

        except commands.ExtensionFailed as e:
            await ctx.send(f"Failed to load extension {e.name}, due to a code error:\n`{e.original}`")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def activity(self, ctx, *, text):
        """Sets the activity of the bot manually"""
        await self.client.change_presence(activity=discord.Game(text))
        await ctx.send(f"Activity set to {text}")

    @commands.is_owner()
    @commands.command(aliases=["shutdown", "off"], hidden=True)
    async def goodnight(self, ctx):
        """Safely shuts down the bot"""
        await ctx.send("Bot shutting down")

        await self.client.change_presence(status=discord.Status.offline)
        await self.client.logout()

    @commands.is_owner()
    @commands.command(aliases=["inv"], hidden=True)
    async def invite(self, ctx):
        """Sends the link used to add the bot to servers"""
        await ctx.send(self.config["invite"])

    @commands.is_owner()
    @commands.command(aliases=["eval"], hidden=True)
    async def _eval(self, ctx, *, text):
        """Evaluates a statement"""
        try:
            out = eval(text)
            await ctx.send(out)
            print(out)
        except Exception as e:
            await ctx.send(f"Statement had error:\n```\n{e}\n```")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def mimic(self, ctx, *, text):
        """Pretend to be the bot"""
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(hidden=True)
    async def server(self, ctx):
        """Gets info on the server"""
        guild = ctx.guild
        e = discord.Embed(title="Server Info", description=guild.description, color=discord.Color.blue())
        e.set_author(name=guild.name, icon_url=guild.icon_url_as(format="png"))
        e.add_field(name="Owner", value=guild.owner.mention, inline=False)
        e.add_field(name="Members", value=len(guild.members), inline=False)
        e.add_field(name="Created at", value=guild.created_at, inline=False)
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    async def whois(self, ctx, member: discord.Member = None):
        """Gets info on a particular user"""
        if member is None:
            member = ctx.author

        e = discord.Embed(title="Member info", color=member.color)
        e.set_author(name=member.display_name, icon_url=member.avatar_url_as(format="png"))
        e.add_field(name="Joined at", value=member.joined_at, inline=False)
        e.add_field(name="Created at", value=member.created_at, inline=False)
        e.add_field(name="ID", value=member.id, inline=False)
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    async def server_icon(self, ctx):
        embed = discord.Embed(title=f"Server icon for {ctx.guild.name}")
        embed.set_image(url=ctx.guild.icon_url_as(format="png"))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Dev(client))
