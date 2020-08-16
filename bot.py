import os
import json

import discord
from discord.ext.commands import Bot

with open("config.json", "r") as config_file:
    config = json.load(config_file)

client = Bot(
    command_prefix=config["prefix"],
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
    status=discord.Status.online,
    activity=discord.Game("Vibing | .help")
)
client.config = config

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.run(config["bot_token"])
