import discord
from discord.ext import commands

tic_tac_toe_current_content = None
tic_tac_toe_player_o = None
tic_tac_toe_player_x = None
board = [[]]

class Games(commands.Cog, description="Simple games that can be played over discord"):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="tictactoe")
    async def tictactoe(self, ctx):

        #Setup for the initial Board,
        # :white_large_square: is an empty cell ":x:" is an X and ":o:" is an O
        global board
        board = [[":white_large_square:", ":white_large_square:", ":white_large_square:"],
                [":white_large_square:", ":white_large_square:", ":white_large_square:"],
                [":white_large_square:", ":white_large_square:", ":white_large_square:"]]

        # Send the board as an embed
        await embed_board(ctx, True)

    # BIG LISTENER FOR ALL REACTION CONTROLS, PROLLY A BAD IDEA
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        user = payload.member

        if user != self.bot.user:

            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)

            message = await channel.fetch_message(payload.message_id)

            if message.id == tic_tac_toe_current_content.id:

                member_name = guild.get_member(payload.user_id)
                
                if payload.emoji.name == "❌":
                    global tic_tac_toe_player_x
                    if tic_tac_toe_player_x is None:
                        tic_tac_toe_player_x = member_name
                        await channel.send(f"{member_name} is now playing X's")
                    else:
                        await channel.send("There is already a player for X")

                elif payload.emoji.name == "⭕":
                    global tic_tac_toe_player_o
                    if tic_tac_toe_player_o is None:
                        tic_tac_toe_player_o = member_name
                        await channel.send(f"{member_name} is now playing O's")
                    else: 
                        await channel.send("There is already a player for O")
                else:
                    await channel.send("Not a valid reaction")

                if tic_tac_toe_player_o is not None and tic_tac_toe_player_x is not None:
                    await channel.send(f"Game begining with {tic_tac_toe_player_x} as X and {tic_tac_toe_player_o} as O")
                    
                    await tic_tac_toe_next_turn()

def board_toString():
    board_string = ""

    for row in range(len(board)):
        for col in range(len(board[row])):
            board_string = " ".join([board_string, board[row][col]])

        board_string = " ".join([board_string, "\n"])
        
    return board_string

async def embed_board(ctx, doingSetup):
# add the board to the embed
    board_string = board_toString()
    
    emb = discord.Embed(name="board", description=board_string)

    board_embed = await ctx.send(embed=emb)

    # update the current content for tictactoe
    global tic_tac_toe_current_content
    tic_tac_toe_current_content = board_embed

    if doingSetup is True:
        
        team_reactions = {
        "X Player": "❌",
        "O Player" : "⭕"  
    }

        for player in team_reactions:
            await board_embed.add_reaction(team_reactions[player])
    else:
    
        input_reactions = {
        "X Player": "❌",
        "O Player" : "⭕"  
    }

        for input in input_reactions:
            await board_embed.add_reaction(input_reactions[input])

# Define the function that prints the next frame of the game
async def tic_tac_toe_next_turn():
    return