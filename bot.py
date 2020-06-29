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
        type(message)

        command = message.content[message.content.find(' ')+1:]
        summoner_name = command[command.find(' ')+1:]                             # get the summoner name
        summoner = SummonerAPI.get_summoner_by_name(summoner_name)       # access the SummonerAPI based off of summoner_name

        

        summoner_id = summoner['id']
        account_id = summoner['accountId']

        league = LeagueAPI.rank_of_summoner(summoner_id)
        #matchlist = MatchAPI.get_matchlist(account_id)

        end_index = 100
        begin_index = 0
        #gameId_dict = {}                                                                                        # this will store the matchId and the champion that was player
        #champ_occurrences = {}                                                                                  # this will store the amount of times that a champion was played
        #matchlist_ranked = MatchAPI.get_matchlist_ranked(account_id, 420, 13, end_index, begin_index)           # this gets all the ranked matches 
        
        # find the rank of the summoner
        if message.content.startswith('-lol rank '):
            # test if it works
            count = 0
            for i in league:
                if i['queueType'] == 'RANKED_SOLO_5x5':
                    await message.channel.send(str(summoner['name']) + " is " + league[count]['tier']+ " " +league[count]['rank'])
                count += 1
            

        # find the 5 most played champs
        if message.content.startswith('-lol champs '):
            output = '**Most Played Champs in Ranked for ' + summoner_name + "**\n"

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
        if message.content.startswith('-lol stats '):
            output = '**Stats for ' + summoner_name + "**\n"
            await message.channel.send(output)
            
            

client.run(TOKEN)






