# bot.py
import os
import discord
import operator
import re
import math
import LoLConsts as Consts

# delete these
import random

from heapq import nlargest
from dotenv import load_dotenv
from discord.ext import commands

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
        gameId_dict = {}                                                                                        # this will store the matchId and the champion that was player
        champ_occurrences = {}                                                                                  # this will store the amount of times that a champion was played
        matchlist_ranked = MatchAPI.get_matchlist_ranked(account_id, 420, 13, end_index, begin_index)           # this gets all the ranked matches 
        
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
            output = ''
            while begin_index < matchlist_ranked['totalGames']:
                matches = MatchAPI.get_matchlist_ranked(account_id, 420, 13, end_index, begin_index)
                print(str(begin_index), str(end_index))
                for games in matches['matches']:
                    gameId_dict[games['gameId']] = games['champion']
                    if games['champion'] in champ_occurrences:
                        champ_occurrences[games['champion']] += 1
                    else:
                        champ_occurrences[games['champion']] = 1
                end_index += 100
                begin_index += 100
    
            three_highest = nlargest(5, champ_occurrences, key = champ_occurrences.get)
            output = "**Most Played Champion in Ranked**" + "\n"
            #await message.channel.send("**Most Played Champion in Ranked**")
            for val in three_highest:
                output += '   - **' + re.sub(r"(\w)([A-Z])", r"\1 \2", ChampMasteryAPI.get_champion(str(val))) + "** : " + str(champ_occurrences.get(val)) + " games\n"
            await message.channel.send(output)
            

client.run(TOKEN)






