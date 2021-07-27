import json
import time
import discord
from discord.ext import commands


class Utility(commands.Cog, description="Utility commands related to bot functionality"):

    def __init__(self, bot):
        self.bot = bot


    # prints to the console anything the bot is dm'd
    # also stores it in the requests.json file under the dms list
    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.bot.user:
            print(f"{message.author} sent: {message.content}")
            # File where the requests are stored 
            file_name = 'requests.json'
            
            #Open the file and grab the json data
            with open(f"C:/Baka-Bot/{file_name}") as access_json:
                file_access = json.load(access_json)

            #Get the dms list from the json file
            dms = file_access['dms']

            # time_gmt stores current gmtime
            time_gmt = time.gmtime()
            # time_asctime stores the timestamp in a good format
            time_asctime = time.asctime(time_gmt)
            
            # Format for the request dict to be stored
            dm = {
                "author" : f"{message.author}",
                "message" : f"{message.content}",
                "time_sent" : f"{time_asctime}"
            }

            # Append the request to the requests list
            dms.append(dm)

            # Write the requests back into the json file
            with open('requests.json', 'w', encoding='utf-8') as access_json:
                json.dump(file_access, access_json, ensure_ascii=True, indent=4)    

    @commands.command(name='request', help='Sends a message to the developer. Please use this to send suggestions for new features, \
report bugs and generally communicate with the developer.')
    async def request(self, ctx, *, message):
        print(message)

        # File where the requests are stored 
        file_name = 'requests.json'
        
        #Open the file and grab the json data
        with open(f"C:/Baka-Bot/{file_name}") as access_json:
            file_access = json.load(access_json)

        #Get the requests list from the json file
        requests = file_access['requests']

        # gmt stores current gmtime
        time_gmt = time.gmtime()
        time_asctime = time.asctime(time_gmt)
        
        # Format for the request dict to be stored
        request = {
            "author" : f"{ctx.author}",
            "message" : f"{message}",
            "time_sent" : f"{time_asctime}"
        }

        # Append the request to the requests list
        requests.append(request)

        # Write the requests back into the json file
        with open('requests.json', 'w', encoding='utf-8') as access_json:
            json.dump(file_access, access_json, ensure_ascii=True, indent=4)

        await ctx.send(f"Thanks for your request {ctx.author.display_name}!")

    # Error handling for the request command
    @request.error
    async def request_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('A description of your request seems to be missing, try using `!request <description of your request>`')
        elif isinstance(error, IOError):
            await ctx.send("Something went wrong while opening the request file, please send a dm to either myself or my developer\
and we'll get right on it!")


    @commands.command(name='addbot', help='Displays the link used to add me to a server')
    async def addbot(self, ctx):
        bot_link = "https://discord.com/api/oauth2/authorize?client_id=812441406018420777&permissions=2184707152&scope=bot"
        emb = discord.Embed()
        emb.set_author(name="Bot URL", icon_url=self.bot.user.avatar_url)
        emb.add_field(name=highlight('URL'), value=bot_link)
        await ctx.send(embed=emb)

# Helper functions for discord specific text formatting
def highlight(string):
    return string.replace(f'{string}',f'`   {string}   `')
def bold(string):
    return string.replace(f'{string}',f'**{string}**')