from asyncio.windows_events import NULL
import random
import enum
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
import json
from cassiopeia.data import Rank
import discord
from discord.ext import commands
import cassiopeia as cass

#Key needs to be reset daily
cass.set_riot_api_key("RGAPI-d18ead5b-a161-4334-b304-b6936cc8b2a2")  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")

#Enum used in the abilities command, makes the titles of abilities easier
class Key(enum.Enum):
    Passive = "skill skill_innate"
    Q = "skill skill_q"
    W = "skill skill_w"
    E = "skill skill_e"
    R = "skill skill_r"


class League(commands.Cog, description="Commands related to the game League of Legends:\n\
    Should Eventually be able to display information on specific players, including rank and other information\n\
    It Will also include commands for displaying information on items and champions, scraped from the wiki\n\
    I am also working on a match making system for custom games, but that's a while off"):

    def __init__(self, bot):
        self.bot = bot
    

    # THIS SECTION COVERS THE ACCOUNT/SUMMONER SPECIFIC COMMANDS

#     @commands.command(name='mastery7', help='prints a list of champions that the input summoner has mastery 7 on')
#     async def mastery7(self, ctx, *, summoner_name):
        
#         summoner = cass.get_summoner(name=summoner_name)
#         good_with = summoner.champion_masteries.filter(lambda cm: cm.level ==7)

#         mastery7 = []
        
#         for cm in good_with:
#             mastery7.append(cm.champion.name)
        
#         await ctx.send(f'{summoner.name} has mastery 7 with these champions: {mastery7}')


#     @commands.command(name='rank', help='Displays the rank of the input summoner in both solo/duo and flex queue')
#     async def rank(self, ctx, *, summoner_name):

#         summoner = cass.get_summoner(name=summoner_name)
#         rank_dict = summoner.ranks

#         for queue, rank in rank_dict.items():

#             if queue == cass.Queue.ranked_solo_fives:
                
#                 await ctx.send(f'{summoner.name} is {rank} in solo-q')
                
#                 if rank.tier == cass.data.Tier.gold:
#                     await ctx.send(f'cmon {summoner_name}, you can do better than that')
#             else:
#                 await ctx.send(f'{summoner.name} is {rank} in flex')










#     # THIS SECTION COVERS THE CHAMPION SPECIFIC COMMANDS

#     @commands.command(name='stats', help='Displays the stats of the given champion')
#     async def stats(self, ctx, *, champion_name):

#         champion = cass.get_champion(f'{champion_name}')
#         stats = champion.stats

#         emb = discord.Embed(title = f"{champion.name}", description=f"Displaying {champion.name}'s base stats")
#         # Weird formatting because of multiline string, dont worry about it
#         response = f"""
# armor: {stats.armor}
# armor per level: {stats.armor_per_level}
# attack_damage: {stats.attack_damage}
# attack_damage_per_level: {stats.attack_damage_per_level}
# attack_range: {stats.attack_range}
# attack_speed: {stats.attack_speed}
# percent_attack_speed_per_level: {stats.percent_attack_speed_per_level}
# critical_strike_chance: {stats.critical_strike_chance}
# critical_strike_chance_per_level: {stats.critical_strike_chance_per_level}
# health: {stats.health}
# health_per_level: {stats.health_per_level}
# health_regen: {stats.health_regen}
# health_regen_per_level: {stats.health_regen_per_level}
# magic_resist: {stats.magic_resist}
# magic_resist_per_level: {stats.magic_resist_per_level}
# mana: {stats.mana}
# mana_per_level: {stats.mana_per_level}
# mana_regen: {stats.mana_regen}
# mana_regen_per_level: {stats.mana_regen_per_level}
# movespeed: {stats.movespeed}"""
        
#         emb.add_field(name="Stats", value=response, inline=True)
#         skins = champion.skins
#         emb.set_thumbnail(url=skins['default'].loading_image_url)
#         await ctx.send(embed=emb)

#     @commands.command(name='abilities', help='Displays the abilities of the given champion')
#     async def abilities(self, ctx, *, champion_name):

#         champion = cass.get_champion(f'{champion_name}')
        
#         emb = discord.Embed(title = f"{champion.name}", description=f"Displaying {champion.name}'s abilities")

#         passive = champion.passive
#         emb.add_field(name=f"Passive: {passive.name}", value=passive.description, inline=False)

#         spells = champion.spells
#         for spell in spells:
#             emb.add_field(name=f"{spell.keyboard_key}: {spell.name}", value=spell.description, inline=False)
#             emb.add_field(name=f"{spell.keyboard_key} tooltip:",value=f"{spell.tooltip}", inline=False)
#             emb.add_field(name=f"{spell.keyboard_key} effects:",value=f"{spell.effects}", inline=False)
#             print(spell.effects_by_level)

#         skins = champion.skins
#         emb.set_thumbnail(url=skins['default'].loading_image_url)
        
        
#         await ctx.send(embed=emb)






















# # This section uses the ddragon json file downloaded to the computer, will work on improving this over time
# # Otherwise just use the cass api for ease of functionality
#     @commands.command(name='ddragonstats', help='prints the stats of the given champion')
#     async def ddragonstats(self, ctx, *, champion):
#         with open(f"C:/Baka-Bot/11.11.1/data/en_US/champion/{champion}.json") as access_json:
#             file_access = json.load(access_json)
        
#         data_access = file_access['data']

#         access_json.close() #Close the file so bad things dont happen

#         champion_access = data_access[f'{champion}']
        
#         stats_access = champion_access['stats']
        
#         await ctx.send(stats_access)

#     @commands.command(name='ddragonabilities', help='prints the abilities of the given champion')
#     async def ddragonabilities(self, ctx, *, champion):
#         with open(f"C:/Baka-Bot/11.11.1/data/en_US/champion/{champion}.json") as access_json:
#             file_access = json.load(access_json)
        
#         data_access = file_access['data']

#         access_json.close() #Close the file so bad things dont happen

#         champion_access = data_access[f'{champion}']
        
#         abilities_access = champion_access['spells']
        
#         print(abilities_access)

#         for abilities in abilities_access:
#             await ctx.send(abilities)




























    # #THIS SECTION IS FOR SCRAPING FROM THE WIKI BECAUSE RIOT IS A SMALL INDIE COMPANY

    @commands.command(name='wikiinfo', help='Gets information about the input champion from the League wikia')
    async def wikiinfo(self, ctx, *, champion_name):

        #FIX CHAMPION NAME INPUT
        if " " in champion_name: #Deal with champs that have spaces in their names
            champion_list = champion_name.split(" ")
            champion = f"{champion_list[0].capitalize()}{champion_list[1].capitalize()}"
            champion_url = f"{champion_list[0].capitalize()}_{champion_list[1].capitalize()}"
        else: #If they dont have a space, just capitalize the name
            champion = champion_name.capitalize()
            champion_url = champion
      
        # get URL
        page = requests.get(f"https://leagueoflegends.fandom.com/wiki/{champion_url}/LoL")
  
        # display status code
        print(page.status_code)
        # If the response was successful, no Exception will be raised
        try:
            page.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
    
        #Should make this a lis rather than dict, put flat and per level in same embed
        stats_list = [
            f"Health_{champion}",
            f"HealthRegen_{champion}",
            f"ResourceBar_{champion}",
            f"ResourceRegen_{champion}",
            f"Armor_{champion}",
            f"AttackDamage_{champion}",
            f"AttackSpeed_{champion}",
            f"MagicResist_{champion}",
            f"MovementSpeed_{champion}",
            f"AttackRange_{champion}"
        ]

        # scrape webpage
        soup = BeautifulSoup(page.content, 'html.parser')

        # Determine what resource the champ uses
        resources = soup.find_all(class_="pi-faux-label")
        resource = resources[1]
        resource_table = resource.find_all('a')
        resource_name = resource_table[1].get("title")

        # Determine what regen happens/ or secondary resource
        secondary_resource = resources[3]
        secondary_resource_name = secondary_resource.get_text().strip()
        
        emb = discord.Embed(description=f"Displaying {champion}'s info")

        for stat in stats_list:
            
            try:
                value = soup.find(id=f"{stat}").string
            except:
                value = "N/A"
            try:
                value_lvl = soup.find(id=f"{stat}_lvl").string
            except:
                value_lvl = ""

            #For resource field, use the specific search for the correct type done above
            if stat == f"ResourceBar_{champion}":
                emb.add_field(name=f"`   {resource_name}   `", value=f"**{value} {value_lvl}**", inline=False)
            # If the resource is found to be "Manaless" do this
            elif stat == f"ResourceRegen_{champion}" and resource_name == "Manaless":
                # Check if they are a fury champion, if so act accordingly
                if soup.find(attrs={"data-tip": "Fury"}).get_text().strip() == "Fury":
                    value = 'Fury (100)'
                # If not, do the standard manaless action
                else:
                    value = soup.find(title="Manaless").string
                # Add a field to the embed with the appropriate values
                emb.add_field(name=f"`   {secondary_resource_name}   `", value=f"**{value} {value_lvl}**", inline=False)
            # If they are an energy champion, do this. uses the energy value finder from above
            elif stat == f"ResourceRegen_{champion}" and resource_name == "Energy":
                # value = soup.find(title="Energy").string
                value = soup.find(attrs={"data-source": "resource regen"}).get_text().strip().replace(f"{secondary_resource_name}", "")
                emb.add_field(name=f"`   {secondary_resource_name}   `", value=f"**{value} {value_lvl}**", inline=False)
            
            # Attack speed is formatted differently, so its separate process goes here
            elif stat == f"AttackSpeed_{champion}":
                value = soup.find(attrs={"data-source": "attack speed"}).get_text().replace("Base AS", "")
                # attackspeed_title = "Base AS" #get the name of the stat, in this case: Base AS
                value_lvl = soup.find(id=f"AttackSpeedBonus_{champion}_lvl").string #Grab the per level increase, different format from the rest
                emb.add_field(name=f"`   {stat.split('_')[0]}   `", value=f"**{value} {value_lvl}%**", inline=False)
            
            else:
                emb.add_field(name=f"`   {stat.split('_')[0]}   `", value=f"**{value} {value_lvl}**", inline=False)



        #get the splash art for the desired champ to use as a thumbnail
        image_div = soup.find(class_='FullWidthImage')
        image_url = image_div.find('a')['href']

        emb.set_thumbnail(url=f'{image_url}')
        emb.set_author(name=f'{champion}')
        
        await ctx.send(embed=emb)


#TEST COMMAND TO GET ABILITIES

    @commands.command(name='abilities', help='Gets the ability information of the input champion from the League wikia')
    async def abilities(self, ctx, *, champion_name):
        #FIX CHAMPION NAME INPUT
        if " " in champion_name: #Deal with champs that have spaces in their names
            champion_list = champion_name.split(" ")
            champion = f"{champion_list[0].capitalize()}{champion_list[1].capitalize()}"
            champion_url = f"{champion_list[0].capitalize()}_{champion_list[1].capitalize()}"
        else: #If they dont have a space, just capitalize the name
            champion = champion_name.capitalize()
            champion_url = champion
      
        # get URL
        page = requests.get(f"https://leagueoflegends.fandom.com/wiki/{champion_url}/LoL")
  
        # display status code
        print(page.status_code)
        # If the response was successful, no Exception will be raised
        try:
            page.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

        # scrape webpage
        soup = BeautifulSoup(page.content, 'html.parser')

        #get the splash art for the desired champ to use as a thumbnail
        image_div = soup.find(class_='FullWidthImage')
        image_url = image_div.find('a')['href']

        # List of ability identifiers
        abilities_list = [
            'skill skill_innate',
            'skill skill_q',
            'skill skill_w',
            'skill skill_e',
            'skill skill_r'
        ]

        #Get the div for each ability
        for ability in abilities_list:
            ability_title = []

            #Get the div for each ability
            ability_div = soup.find(class_=f"{ability}")
            ability_emb = discord.Embed()

            #Get all of the ability headers, the divs for each ability block
            ability_sections = ability_div.find_all(class_="ability-info-container") #,style=lambda value: value and "padding-bottom:1em;")

            for section in ability_sections:
                # For each section get the header, contains the name, title and other attributes
                ability_header = section.find(class_="champion-ability__header")
                ability_name = ability_header.find(class_="mw-headline").get_text()
                ability_title.append(ability_name)
                
                # Get all of the text paragraphs in the section
                ability_paragraphs = section.find_all('p')

                # For each paragraph in the list
                last_type = "" #Holder var
                last_text = "" #Holder var
                for index, paragraph in enumerate(ability_paragraphs):
                    # print(paragraph)
                    
                    try:
                        #Try to find the ability type, ie active vs innate
                        ability_type = paragraph.find(class_="template_sbc").get_text()
                    except:
                        pass

                    # Get the text for each paragraph
                    ability_text = paragraph.get_text()

                    # If the combined paragraph length is greater than the embed field limit, or
                    # if the ability type is not the same as the last type make an embed with the last_text and set
                    # the current text to be the new last_text
                    if ((len(last_text) + len(ability_text)) > 1024 or ability_type != last_type) and last_text != "":
                        ability_emb.add_field(name=highlight(f"{ability_name}: {last_type}"), value=f'{last_text.replace(f"{last_type}", "")}')
                        last_text = ability_text
                        last_type = ability_type
                        # If we are on the last index, make this embed field too
                        # Needs to be here as well if the last index is a different type or too long
                        if index is (len(ability_paragraphs) - 1):
                            ability_emb.add_field(name=highlight(f"{ability_name}: {ability_type}"), value=f'{ability_text.replace(f"{ability_type}", "")}')
                    # If we are on the last index, make this an embed field too
                    elif index is (len(ability_paragraphs) - 1):
                        last_text = last_text + f" {ability_text}"
                        ability_emb.add_field(name=highlight(f"{ability_name}: {last_type}"), value=f'{last_text.replace(f"{last_type}", "")}')
                    # Otherwise, add the current text to the old text to make a larger combined embed value
                    else:
                        last_text = last_text + ability_text
                        last_type = ability_type

                    # ability_emb.add_field(name=highlight(f'{ability_name}: {ability_type}'), value=f'{ability_text.replace(f"{ability_type}", "")}')
                    
            #Get the image for each ability section and add it to the embed
            ability_image = ability_div.find(class_="pi-item pi-image").find('a')['href']
            # Put together the combined title for the ability and set the author to it as a header
            title = "/".join(ability_title)
            ability_emb.set_author(name=f"{Key(ability).name}: {title}", icon_url=f"{ability_image}")

            # Put the thumbnail only on the passive embed
            if Key(ability) is Key.Passive:
                ability_emb.set_thumbnail(url=f'{image_url}')

            await ctx.send(embed=ability_emb)


    @commands.command(name='rank', help='returns the rank of the input summoner from u.gg')
    async def rank(self, ctx, *, summoner_name):
        #FIX CHAMPION NAME INPUT
        summoner_url = summoner_name.replace(" ", "%20")
      
        url = f"https://u.gg/lol/profile/na1/{summoner_url}/overview"

        # Use Selenium to interact with the webpage

        # Use chrome
        driver = webdriver.Chrome(r"F:/chromedriver_win32/chromedriver.exe")

        # Open the website
        driver.get(url)

        # Get the update button and click it
        update_button = driver.find_element_by_class_name("update-button")
        update_button.click()

        # get URL
        page = requests.get(url)
  
        # display status code
        print(page.status_code)
        # If the response was successful, no Exception will be raised
        try:
            page.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

        # scrape webpage
        soup = BeautifulSoup(page.content, 'html.parser')

        rank_divs = soup.find_all(class_="rank-tile")

        rank_emb = discord.Embed()

        for queue in rank_divs:

            queue_type = queue.find(class_="queue-type").get_text()

            rank = queue.find(class_="rank-text").get_text()
            cleaned_rank = rank.replace("/", ": ") # Replaces the '/' with a space

            if queue_type == "Ranked Solo":
                # Get the png used for the rank icon
                # Hosting images using ibb
                if "Iron" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/K58NXGD/iron.png"
                elif "Bronze" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/xjCFxWV/bronze.png"
                elif "Silver" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/3R6ZbL3/silver.png"
                elif "Gold" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/Mn18y7c/gold.png"
                elif "Platinum" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/FXhrdYt/platinum.png"
                elif "Diamond" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/HBQ5S7H/diamond.png"
                elif "Master" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/Z2dx21f/master.png"
                elif "Grandmaster" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/PxV2yGC/grandmaster.png"
                elif "Challenger" in cleaned_rank:
                    rank_icon_url ="https://i.ibb.co/C2x1vV4/challenger.png"

            rank_emb.add_field(name=f"{highlight(queue_type)}", value=cleaned_rank)        

        rank_emb.set_author(name=f"{summoner_name}'s Rank", icon_url=f"{rank_icon_url}")

        await ctx.send(embed=rank_emb)

        driver.quit() # Close the window
            
            

# Helper functions for discord specific text formatting
def highlight(string):
    return string.replace(f'{string}',f'`   {string}   `')
def bold(string):
    return string.replace(f'{string}',f'**{string}**')



