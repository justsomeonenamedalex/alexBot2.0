import discord
from discord.ext import commands
import asyncio
import random
import math

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

    @commands.command(aliases=["ms"])
    async def minesweeper(self, ctx, x: int = 5, y: int = 5):
        grid = [[0 for n in range(x)] for i in range(y)]  # Creates a grid using embeded lists
        num_boms = math.ceil((x*y)//5)  # About 20% of the cells will be bombs

        # Place the bombs
        for n in range(num_boms):
            while True:
                bomb_x = random.randint(0, x - 1)
                bomb_y = random.randint(0, y - 1)
                bomb_space = grid[bomb_y][bomb_x]
                if bomb_space == 0:
                    # "*" represents a bomb
                    grid[bomb_y][bomb_x] = "*"
                    break
                else:
                    pass

        # Update the empty spaces to show many bombs are adjacent
        # The easiest thing to do is to find each bomb and add one to each adjacent cell
        for row_num, row in enumerate(grid):
            for column_num, item in enumerate(row):
                # If the cell contains a bomb
                if item == "*":

                    # This loops over every adjacent cell
                    for a in [-1, 0, 1]:
                        for b in [-1, 0, 1]:
                            try:
                                coords = (row_num+a, column_num+b)
                                target_item = grid[coords[0]][coords[1]]  # Get the contents of the cell

                                # This cehcks that the cell doesn't contain a bomb, and that the coords aren't negative
                                # Python does negative indexes which i forgot the first time i wrote this bit
                                if target_item != "*" and coords[0] >= 0 and coords[1] >= 0:
                                    grid[coords[0]][coords[1]] += 1
                            except IndexError:
                                # If the cell being looked at doesn't exist this runs
                                # This is somewhat lazy but it works
                                pass

        # This is easier to do than finding the weird unicode characters like i did for the poll command
        emoji_replacements = {
            0: ":zero:",
            1: ":one:",
            2: ":two:",
            3: ":three:",
            4: ":four:",
            5: ":five:",
            6: ":six:",
            7: ":seven:",
            8: ":eight:",
            9: ":nine:",
            "*": ":boom:"
        }

        for row_num, row in enumerate(grid):
            for column_num, item in enumerate(row):
                # Replace everything in the list with the corresponding emoji markdown
                grid[row_num][column_num] = emoji_replacements[item]

        out_grid = []
        for row in grid:
            # Spoiler tag each cell
            out_grid.append("".join([f"||{i}||" for i in row]))
        out_string = "\n".join(out_grid) + f"\nThere are {num_boms} bombs in this grid!"

        try:
            await ctx.send(out_string)
        except discord.HTTPException:
            # This runs if the message is too long
            await ctx.send("That grid is too big!")


def setup(client):
    client.add_cog(Games(client))
