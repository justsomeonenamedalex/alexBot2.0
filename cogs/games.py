import discord
from discord.ext import commands
import asyncio
import random

rps_moves = ["🧱", "📰", "✂"]


def rps_check_winner(player_move: str, ai_move: str) -> str:
    print(player_move, ai_move)
    if not (player_move in rps_moves and ai_move in rps_moves):
        raise Exception("Invalid move")

    result = None

    if player_move == ai_move:
        result = "Draw"
    else:
        if player_move == "🧱" and ai_move == "✂":
            result = "Player wins"
        elif player_move == "✂" and ai_move == ":📰:":
            result = "Player wins"
        elif player_move == "📰" and ai_move == "🧱":
            result = "Player wins"
        else:
            result = "Ai wins"
    return result


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command(aliases=["rps"])
    async def rock_paper_scissors(self, ctx):
        ai_score = 0
        player_score = 0
        game_round = 1

        embed = discord.Embed(title="Rock paper scissors! First to 3 wins.",
                              description="Click the reaction to make "
                                          "your move!")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Player score", value=str(player_score), inline=False)
        embed.add_field(name="Ai score", value=str(ai_score), inline=False)
        main_message = await ctx.send(embed=embed)

        for i in rps_moves:
            await main_message.add_reaction(i)

        while True:
            await main_message.edit(embed=embed)

            if player_score == 3:
                embed.add_field(name="Result", value=f"{ctx.author.display_name} wins!", inline=False)
                await main_message.edit(embed=embed)
                await main_message.clear_reactions()
                break
            elif ai_score == 3:
                embed.add_field(name="Result", value="Ai wins!", inline=False)
                await main_message.edit(embed=embed)
                await main_message.clear_reactions()
                break

            def check(reaction, user):
                return user == ctx.author and str(reaction) in rps_moves

            try:
                response_reaction, user = await self.client.wait_for("reaction_add", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond!")
                return None

            player_move = str(response_reaction)
            await main_message.remove_reaction(player_move, ctx.author)

            ai_move = random.choice(rps_moves)
            result = rps_check_winner(player_move, ai_move)

            if result == "Player wins":
                player_score += 1
            elif result == "Ai wins":
                ai_score += 1
            else:
                pass

            embed.set_field_at(0, name="Player score", value=str(player_score), inline=False)
            embed.set_field_at(1, name="Ai score", value=str(ai_score), inline=False)
            embed.add_field(name=f"Round {game_round}", value=f"{ctx.author.display_name} played: {player_move}\nThe "
                                                              f"ai played: {ai_move}\n{result}", inline=True)

            game_round += 1


def setup(client):
    client.add_cog(Games(client))
