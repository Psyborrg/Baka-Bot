import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import giphy_client

#Import the Roll class created to roll dice
from Roll import Roll
from ddragon import League
from Music import Music
from Utility import Utility
from games import Games

# Helper functions for discord specific text formatting
def highlight(string):
    return string.replace(f'{string}',f'`   {string}   `')
def bold(string):
    return string.replace(f'{string}',f'**{string}**')

# Note to self: 
# Tokens dont keep {} around them in the file, just type the
# token verbatim
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GIPHY_KEY = os.getenv('GIPHY_KEY')

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# Constructor for the bot, all commands start with the prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Name of the text channel where bot notifications and other testing will take place
bot_channel = 'robot-stuff'

#prints into the terminal every member of the guild,
# the guild id, and the guild name, as well as the bot name
@bot.event
async def on_ready():

    print(f'{bot.user} is connected to the following guilds:')

    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        # Get the bot text channel if it exists, otherwise make it
        channel = discord.utils.get(guild.channels, name=f"{bot_channel}")
        if channel is None:
            channel = await guild.create_text_channel(f'{bot_channel}')
        # Send a message to show that the bot is online
        if guild.name == GUILD:
            await channel.send('Ohayo!')

# Sends a dm to any member who joins the guild
@bot.event
async def on_member_join(member):
    await member.create_dm()
    # If they are in the GUILD send a special message
    if member.guild.name == GUILD:
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to the tomb!'
        )
    # Otherwise send a default message
    else:
        await member.dm_channel.send(
            f'Hello {member.name}, welcome to the server!'
        )

# on_message event to process all of the commands, all other on_messages will be listeners
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    # Causes the commands to run, SUPER REQUIRED FOR A MIX OF COMMANDS AND EVENTS
    await bot.process_commands(message)

#ping pong
@bot.command(name='ping', help='Plays ping pong')
#ctx is the 'Context' surrounding the invoked command
#contains the channel and guild and other data that the
#   user called the command from
async def ping(ctx):
    await ctx.send('pong')

#extreme ping
@bot.command(name='PING', help='Plays extreme PING PONG')
#ctx is the 'Context' surrounding the invoked command
#contains the channel and guild and other data that the
#   user called the command from
async def ping(ctx):
    await ctx.send('PONG!')

#extreme ping
@bot.command()
async def pong(ctx):
    if ctx.author.display_name == "DroopyMantis230":
        await ctx.send(f"Only for you {ctx.author.display_name}, ping <3")
    else:
        await ctx.send(f"{ctx.author.display_name}, you know I don't know how to ping")

#zoe copypasta i guess, it was requested -_-
@bot.command()
async def zoe(ctx):
    
    api_instance = giphy_client.DefaultApi()
    api_response = api_instance.gifs_gif_id_get(GIPHY_KEY, gif_id='l04DWtTzSqI8b0bhwv')
    giff = api_response.data

    emb = discord.Embed(title = "Why did I make this?")
    #the link needs to be hardcoded but the id is based on the api search
    emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

    emb.add_field(name='Why?', value="Because I'm a people pleaser...", inline=False)
    emb.set_footer(text="I hope Zoe wins xD. I’m a Zoe main and she’s just so fun!! People get so trolled by the bubble, and her voice lines are so cute like when she \
sings about chocolate cake LOL! She’s super random but also smarter than she looks, just like me xD")

    await ctx.send(embed=emb)





#command to have baka-bot produce a gif of the queried term
@bot.command(name='gif', help='Displays a random gif related to the search term from giphy')
async def gif(ctx, *, query):

    api_instance = giphy_client.DefaultApi()

    api_response = api_instance.gifs_search_get(GIPHY_KEY, query, limit = 5, rating = 'g')
    lst = list(api_response.data)
    giff = random.choice(lst)

    emb = discord.Embed(title = query)
    #the link needs to be hardcoded but the id is based on the api search
    emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

    await ctx.send(embed=emb)

# #snip snip for funzies 
@bot.listen()
async def on_message(message):

    if message.author == bot.user:
        return

    if 'gwen' in message.content.lower():

        api_instance = giphy_client.DefaultApi()

        # The ids have to be hardcoded because search doesnt pull up accurate results (too many gwens)
        gwen_ids = ["wCab1EYb5ze222QR1V", "NSkCP9QbbKHbWXD9x9", "w0aV6SMqWwVGiMkWZs", "uDMW5KReX7MO64gHny", "7qMcBgCN4JC2R4quV9"]
        gwen_id = random.choice(gwen_ids)

        api_response = api_instance.gifs_gif_id_get(GIPHY_KEY, gif_id=gwen_id)
        giff = api_response.data


        emb = discord.Embed(title = "Snip-Snip!")
        #the link needs to be hardcoded but the id is based on the api search
        emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await message.channel.send(embed = emb)


#Tanjiro Kamado, text version 
@bot.listen()
async def on_message(message):
    if 'its tanjiro kamado' in message.content.lower():

        gif_id = '77XbECLoijixFkHheh'

        emb = discord.Embed()
        emb.set_footer(text="Alright gOnPaChIrO kAmAbOkO, I'm gonna bring you DOWN!!!!!!")
        emb.set_image(url=f"https://media.giphy.com/media/{gif_id}/giphy.gif")

        await message.channel.send(embed=emb)


# dms the target member 
@bot.command(name='bday', help='Sends the target member of the server a birthday message!')
async def bday(ctx, *, target):

    member = discord.utils.find(lambda m: m.display_name == f'{target}', ctx.guild.members)

    await member.create_dm()

    api_instance = giphy_client.DefaultApi()

    api_response = api_instance.gifs_search_get(GIPHY_KEY, 'Happy Birthday!', limit = 5, rating = 'g')
    lst = list(api_response.data)
    giff = random.choice(lst)

    emb = discord.Embed(title = "HAPPY BIRTHDAY!")
    #the link needs to be hardcoded but the id is based on the api search
    emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')

    await member.dm_channel.send(embed=emb)


#exit command to stop the bot
@bot.command(name='terminate', help='Turns off baka-bot. Admin command only')
@commands.has_any_role('Admin')
async def terminate(ctx):
    #If the bot is in a voice channel
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    #Send a terminate message to the current chat
    await ctx.send(f'{ctx.author.display_name} terminated me :(')
    #exit the process
    await exit()

#Portion of the code for the terminate command that runs on error    
@terminate.error
async def terminate_error(ctx, error):
    #If you dont have the correct role
    if isinstance(error, commands.CommandError):
        #List of terminate error messages
        msg_error = [
            'Well that\'s not nice', 'My apologies, you do not have permission to use that command',
            'No man born of woman can kill me...'
        ]
        #pick a random message and send it
        await ctx.send(msg_error[random.randint(0, len(msg_error) - 1)])


#rolls any number of any sided die, prints individual rolls
@bot.command(name='roll_dice', help='rolls any number of any sided dice, they must all be the same size. Format: !roll_dice num_dice num_sides')
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

#Rolls any number of any sided die, can be different sizes
#should print each roll and the total
@bot.command(name='roll', help='Rolls any number of any sided dice')
async def roll(ctx, *args):
    for arg in args:
        roll_arr, total = Roll.roll(arg)
        result = str(roll_arr)
        result += f' Total Roll: {total}'
        await ctx.send(result)  


bot.add_cog(League(bot))
bot.add_cog(Music(bot))
bot.add_cog(Utility(bot))
bot.add_cog(Games(bot))

bot.run(TOKEN)