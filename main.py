from SummonerAPI import SummonerAPI as Summoner
from LeagueAPI import LeagueAPI as League
from ChampMasteryAPI import ChampMasteryAPI as ChampMastery
from MatchAPI import MatchAPI as Match
from ClashAPI import ClashAPI as Clash

from heapq import nlargest

import LoLConsts as Consts
import operator
import re
import math

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def main():
    SummonerAPI = Summoner(Consts.KEY['api_key'])               # SummonerAPI Test
    LeagueAPI = League(Consts.KEY['api_key'])                   # LeagueAPI Test
    ChampMasteryAPI = ChampMastery(Consts.KEY['api_key'])       # MasteryAPI Test
    MatchAPI = Match(Consts.KEY['api_key'])                     # MatchAPI Test
    ClashAPI = Clash(Consts.KEY['api_key'])                     # ClashAPI Test

   

    summoner = input("Enter your summoner name: ")
    
    summoner = SummonerAPI.get_summoner_by_name(summoner)       # summoner is vital - never delete this
    print(str(summoner['name']) + " is level " + str(summoner['summonerLevel']))
    #print("")
    #print(summoner)
    #print("")
    summoner_id = summoner['id']                                # keep summoner_id
    account_id = summoner['accountId']                          # keep the accountID

    league = LeagueAPI.rank_of_summoner(summoner_id)

    # check for rank in solo/duo queue
    count = 0
    #print(league)
    for i in league:
        if i['queueType'] == 'RANKED_SOLO_5x5':
            print(str(summoner['name']) + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked solo/duo queue") 
        elif i['queueType'] == 'RANKED_FLEX_SR':
            print(str(summoner['name']) + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked flex queue")   
        count = count+1 
    #print(len(league))

    # Get the highest mastery of all the champions that the Summoner plays here
    mastery = ChampMasteryAPI.get_all_masteries(summoner_id)                # gets all the masteries for that summoneer
    champ_id = []                                                           # making a list to store all the champions
    for i in range(5):                                                      # iterate thru masteries, and append all champId's into the list
        champ_id.append(ChampMasteryAPI.get_champion(str(mastery[i]['championId'])) + " - " + str(mastery[i]['championPoints']) + " mastery points")
    print(champ_id)

    # This accesses the matches of the Summoner
    matchlist = MatchAPI.get_matchlist(account_id)

    end_index = 100
    begin_index = 0
    gameId_dict = {}                                                                                        # this will store the matchId and the champion that was player
    champ_occurrences = {}                                                                                  # this will store the amount of times that a champion was played
    matchlist_ranked = MatchAPI.get_matchlist_ranked(account_id, 420, 13, end_index, begin_index)           # this gets all the ranked matches 
    print("this is the total amount of games", matchlist_ranked['totalGames'])

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
    
    three_highest = nlargest(3, champ_occurrences, key = champ_occurrences.get)
    print("Champion : Amount of times played")
    for val in three_highest:
        print(re.sub(r"(\w)([A-Z])", r"\1 \2", ChampMasteryAPI.get_champion(str(val))), ":", champ_occurrences.get(val))
    


    matchId = matchlist['matches'][0]['gameId']                   # vital for get_match information
    #print(matchId)
    #champion_in_match = matchlist['matches'][0]['champion']       # vital for get_match information
    
    # Access the most recent match
    match = MatchAPI.get_match(matchId)
    print("\nHere are the stats of your previous game:")
    #stats = 0
    player_counter = 0
    kda_dict = {}
    for i in match['participants']:
        kda = str(i['stats']['kills']) + "/" + str(i['stats']['deaths']) + "/" + str(i['stats']['assists'])
        kda_dict[player_counter] = kda
        # if (i['teamId'] == 100):
        #     print("team 1: " + kda) 
        # elif (i['teamId'] == 200):
        #     print("team 2: " + kda)
        player_counter = player_counter+1

    player_counter = 0
    print("\nHere is your latest match and the ranks of the players in your game:")
    for i in match['participantIdentities']:
        if (i['participantId'] < 6):
            print("team 1 : " + i['player']['summonerName'] + ". Their KDA was: " + kda_dict[player_counter])
        else:
            print("team 2 : " + i['player']['summonerName'] + ". Their KDA was: " + kda_dict[player_counter])
        sumId = i['player']['summonerId']
        league = LeagueAPI.rank_of_summoner(sumId)
        count = 0
        for j in league:
            if j['queueType'] == 'RANKED_SOLO_5x5':
                print(i['player']['summonerName'] + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked solo/duo queue") 
            elif j['queueType'] == 'RANKED_FLEX_SR':
                print(i['player']['summonerName'] + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked flex queue")   
            count = count+1
        player_counter = player_counter+1
        print("")

    clash_summoner = ClashAPI.get_team_from_summoner(summoner_id)               # this gives access to the team_id
    if (len(clash_summoner) > 0):
        teamId = clash_summoner[0]['teamId']                                    # this stores the team_id into teamId

        # Now that we have the team_id, we can find all the members of the team and the role that they play
        # to do this, we are going to use summoners_from_team from the ClashAPI
        team = ClashAPI.get_summoners_from_team(teamId)
        print("This is the clash lineup for " + team['name'] + ":")
        for i in team['players']:
            sumId = i['summonerId']                                             # This is the raw summonerId -> convert to IGN
            name = SummonerAPI.get_summoner_by_summoner_id(sumId)['name']       # This gives their IGN
            print(""+ name + " -> " + i['position'])

    
    





if __name__ == "__main__":
    main()