from SummonerAPI import SummonerAPI
from LeagueAPI import LeagueAPI
from ChampMasteryAPI import ChampMasteryAPI
from MatchAPI import MatchAPI

import LoLConsts as Consts

def main():
    api = SummonerAPI(Consts.KEY['api_key'])            # SummonerAPI Test
    api2 = LeagueAPI(Consts.KEY['api_key'])             # LeagueAPI Test
    api3 = ChampMasteryAPI(Consts.KEY['api_key'])       # MasteryAPI Test
    api4 = MatchAPI(Consts.KEY['api_key'])              # MatchAPI Test

    summoner = input("Enter your summoner name: ")
    
    summoner = api.get_summoner_by_name(summoner)       # summoner is vital - never delete this
    print(str(summoner['name']) + " is level " + str(summoner['summonerLevel']))
    #print("")
    #print(summoner)
    #print("")
    summoner_id = summoner['id']                        # keep summoner_id
    account_id = summoner['accountId']                  # keep the accountID

    league = api2.rank_of_summoner(summoner_id)

    # check for rank in solo/duo queue
    count = 0
    for i in league:
        if i['queueType'] == 'RANKED_SOLO_5x5':
            print(str(summoner['name']) + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked solo/duo queue") 
        elif i['queueType'] == 'RANKED_FLEX_SR':
            print(str(summoner['name']) + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked flex queue")   
        count = count+1 
    #print(len(league))

    mastery = api3.get_all_masteries(summoner_id)               # gets all the masteries for that summoneer
    champ_id = []                                               # making a list to store all the champions
    for i in range(5):                                          # iterate thru masteries, and append all champId's into the list
        champ_id.append(api3.get_champion(str(mastery[i]['championId'])) + " - " + str(mastery[i]['championPoints']) + " mastery points")
    print(champ_id)

    matchlist = api4.get_matchlist(account_id)
    matchId = matchlist['matches'][0]['gameId']                   # vital for get_match information
    champion_in_match = matchlist['matches'][0]['champion']       # vital for get_match information
    
    match = api4.get_match(matchId)
    print("")
    for i in match['participantIdentities']:
        if (i['participantId'] < 6):
            print("team 1 " + i['player']['summonerName'])
        else:
            print("team 2 " + i['player']['summonerName'])
        sumId = i['player']['summonerId']
        league = api2.rank_of_summoner(sumId)
        count = 0
        for j in league:
            if j['queueType'] == 'RANKED_SOLO_5x5':
                print(i['player']['summonerName'] + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked solo/duo queue") 
            elif j['queueType'] == 'RANKED_FLEX_SR':
                print(i['player']['summonerName'] + " is " + league[count]['tier']+ " " +league[count]['rank'] + " with " + str(league[count]['leaguePoints']) + "LP" + " in ranked flex queue")   
            count = count+1
        print("")

if __name__ == "__main__":
    main()