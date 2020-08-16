import discord
from discord.ext import commands
from PyDictionary import PyDictionary


class DictionaryCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.py_dict = PyDictionary()
        self.config = client.config

    @commands.group(aliases=["dict"], invoke_without_command=True)
    async def dictionary(self, ctx, *, term):
        default_command: commands.Command = self.dictionary.get_command("meaning")
        await ctx.invoke(default_command, term=term)

    @dictionary.command(aliases=["define"])
    async def meaning(self, ctx, term):
        word_meanings = self.py_dict.meaning(term)

        if word_meanings is None:
            await ctx.send("Sorry, no meanings were found")
            return None

        e = discord.Embed(title=f"Meanings for {term}")
        for thingy, definition in word_meanings.items():
            definition = "\n".join(definition)
            e.add_field(name=thingy, value=definition, inline=False)

        await ctx.send(embed=e)

    @dictionary.command()
    async def synonym(self, ctx, term):
        word_synonym = self.py_dict.synonym(term)

        if word_synonym is None:
            await ctx.send("Sorry, no synonyms were found")
            return None

        e = discord.Embed(title=f"Synonyms for {term}", description="\n".join(word_synonym))

        await ctx.send(embed=e)

    @dictionary.command()
    async def antonym(self, ctx, term):
        word_antonym = self.py_dict.antonym(term)

        if word_antonym is None:
            await ctx.send("Sorry, no antonym were found")
            return None

        e = discord.Embed(title=f"Antonyms for {term}", description="\n".join(word_antonym))

        await ctx.send(embed=e)


def setup(client):
    client.add_cog(DictionaryCommands(client))
