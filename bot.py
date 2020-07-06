# bot.py
import os
import discord
import operator
import re
import math
import LoLConsts as Consts
import requests

# delete these
import random

from heapq import nlargest
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup

from SummonerAPI import SummonerAPI as Summoner
from LeagueAPI import LeagueAPI as League
from ChampMasteryAPI import ChampMasteryAPI as ChampMastery
from MatchAPI import MatchAPI as Match
from ClashAPI import ClashAPI as Clash

SummonerAPI = Summoner(Consts.KEY['api_key'])               # SummonerAPI Test
LeagueAPI = League(Consts.KEY['api_key'])                   # LeagueAPI Test
ChampMasteryAPI = ChampMastery(Consts.KEY['api_key'])       # MasteryAPI Test
MatchAPI = Match(Consts.KEY['api_key'])                     # MatchAPI Test
ClashAPI = Clash(Consts.KEY['api_key'])                     # ClashAPI Test

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# bot = commands.Bot(command_prefix='-lol ')

# @bot.command(name='rank', help='Displays player rank')
# async def getRank(ctx):
#     # response = random.choice(brooklyn_99_quotes)

#     await ctx.send()

# @bot.command(name='champs', help='Displays most played champs in ranked')
# async def getChamps(ctx):
#     await ctx.send("champs 5")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # rather than putting all of the vital lines of code in each if statement
    # we can just put them all in the on_message method
    # and then put all the specific code inside of the future if statements

    # the summoner name isn't always going to be in the same index
    # but the summoner name will always be after the second white space
    # we have to find the second white space in message
    # that will be the start of summoner
    if message.content.startswith('-lol'):
        
        # help menu
        # if message.content == '-lol help':

        command = message.content[message.content.find(' ')+1:]                     # finds command that user input
        summoner_name = command[command.find(' ')+1:]                               # get the summoner name
        summoner = SummonerAPI.get_summoner_by_name(summoner_name)                  # access the SummonerAPI based off of summoner_name
        #print(summoner)

        name = summoner['name']
        
        summoner_id = summoner['id']
        account_id = summoner['accountId']

        league = LeagueAPI.rank_of_summoner(summoner_id)
        #matchlist = MatchAPI.get_matchlist(account_id)

        #gameId_dict = {}                                                                                        # this will store the matchId and the champion that was player
        #champ_occurrences = {}                                                                                  # this will store the amount of times that a champion was played
        #matchlist_ranked = MatchAPI.get_matchlist_ranked(account_id, 420, 13, end_index, begin_index)           # this gets all the ranked matches 
        
        # find the rank of the summoner
        if command == "rank " + name:
            # test if it works
            count = 0
            for i in league:
                if i['queueType'] == 'RANKED_SOLO_5x5':
                    await message.channel.send(str(summoner['name']) + " is " + league[count]['tier']+ " " +league[count]['rank'])
                count += 1
            

        # find the 5 most played champs
        if command == "champs " + summoner_name:
            print(name)
            output = '**Most Played Champs in Ranked for ' + name + "**\n"

            # Web Scraper
            URL = 'https://na.op.gg/summoner/userName=' + summoner_name
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Summoner may not exist causing for an exception
            try:
                results = soup.find(class_='MostChampionContent')

                champs = results.find_all('div', class_='ChampionBox Ranked')

                for i in range(5):
                    champ = champs[i]
                    champion = champ.find('div', class_='ChampionName').text.strip()
                    kda = champ.find('span', class_='KDA').text.strip()

                    played = champ.find('div', class_='Played')
                    winRatio = played.find('div', title='Win Ratio').text.strip()
                    totalPlayed = played.find('div', class_='Title').text.strip()

                    output += "- **" + champion + "**\n"
                    output += "   - **KDA** : " + kda + "\n"
                    output += "   - **Win Ratio** : " + winRatio + "\n"
                    output += "   - **Total Played** : " + totalPlayed + "\n\n"
                await message.channel.send(output)
            except:
                await message.channel.send("Summoner Does Not Exist")
        


        # Here we determine the difference in win rate in the last 10 games
        # as opposed to the total amount of games that the person has played
        # The champions that we are selecting to compare are those found in the web scraper
        # those champions will be queued into the Match API to show the diff in win rate
        # Precondition: First we check the amount of games that op.gg shows for champ
            # if totalPlayed < 11 don't do anything
        if command == "stats " + summoner_name:
            output = '**Stats for ' + name + "**\n"

            # Web Scraper
            URL = 'https://na.op.gg/summoner/userName=' + summoner_name
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')

            results = soup.find(class_='MostChampionContent')

            champs = results.find_all('div', class_='ChampionBox Ranked')

            for i in range(5):
                champ = champs[i]
                champion = champ.find('div', class_='ChampionName').text.strip()
                kda = champ.find('span', class_='KDA').text.strip()

                played = champ.find('div', class_='Played')
                winRatio = played.find('div', title='Win Ratio').text.strip()
                totalPlayed = played.find('div', class_='Title').text.strip()

                totalPlayed_value = int(totalPlayed[:totalPlayed.find(' ')])

                output += "- **" + champion + "**\n"
                output += "   - **Total games played**: " + str(totalPlayed_value) + "\n"

                if totalPlayed_value < 6:
                    output += "   - **Average KDA**: " + kda + "\n\n"
                else:
                    output += "   - **Total KDA**: " + kda + "\n"

                    # this part will analyze the past 10 games for the champion
                    val = ChampMasteryAPI.get_championId(champion)
                    champion_matchlist = MatchAPI.get_matchlist_ranked(account_id, val, 420)
                    gameIds = []                                                                    # store the last 10 games in here
                    counter = 0
                    for match in champion_matchlist['matches']:
                        if counter == 6:                                                            # the amount of games it calculates per champ
                            break
                        gameIds.append(match['gameId'])
                        counter += 1
                    
                    # keep track of the kda
                    kills = 0
                    deaths = 1
                    assists = 0
                    
                    # Great! now we iterate through the gameId list we made
                    for game in gameIds:
                        match = MatchAPI.get_match(game)                                            # gives access to the match details
                        
                        # iterate through the match participants
                        for participant in match['participants']:
                            # print(str(participant['championId']) + " : " + str(val))
                            if str(participant['championId']) == str(val):
                                print(participant['stats']['kills'])
                                kills += participant['stats']['kills']
                                assists += participant['stats']['assists']
                                deaths += participant['stats']['deaths']
                                break

                    # Now all the games have been iterated thru for that champ
                    # Calculate the kda for that champ
                    # print(kills)
                    # print(assists)
                    # print(deaths)
                    ten_game_kda = (kills+assists)/deaths
                    rounded_kda = round(ten_game_kda*100)/100

                    output += "   - **5 Most recent games KDA**: " + str(rounded_kda) + ":1\n"

                    # Let's evaluate the difference of kda's
                    # First get the value of the total kda before the colon
                    kda_value = float(kda[:kda.find(':')])
                    
                    if rounded_kda > kda_value+1:
                        output += "   - " + summoner_name + " will carry\n\n"
                    elif rounded_kda > kda_value:
                        output += "   - " + summoner_name + " is good and could potentially help carry\n\n"
                    elif rounded_kda == kda_value:
                        output += "   - " + summoner_name + " somehow managed to get his kda to equal his 5 day kda\n\n"
                    elif rounded_kda < kda_value-1 or rounded_kda < 1.0:
                        output += "   - **SHIT PLAYER!!! DO NOT LET THEM PLAY THIS CHAMPION, **\n\n"
                    else:
                        output += "   - " + summoner_name + " not that bad, probably had a couple of bad games, but be aware\n\n"

            await message.channel.send(output)
            # except:
            #     await message.channel.send("Summoner Does Not Exist")
            
            

client.run(TOKEN)






