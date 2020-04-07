KEY = {
    'api_key': 'RGAPI-9a268ce4-defe-40d4-874a-2fcb3a4ba90c'
}

SUMMONER_URL = {
    'base': 'https://{proxy}.api.riotgames.com/lol/summoner/{url}',
    'summoner_by_name': 'v{version}/summoners/by-name/{names}?api_key={api_key}'
}

LEAGUE_URL = {
    'base': 'https://{proxy}.api.riotgames.com/lol/league/{url}',
    'entries_by_summoner': 'v{version}/entries/by-summoner/{summoner_id}?api_key={api_key}'
}

CHAMP_MASTERY_URL = {
    'base': 'https://{proxy}.api.riotgames.com/lol/champion-mastery/{url}',
    'champion_masteries_by_summoner': 'v{version}/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}',
    'all_champs': 'http://ddragon.leagueoflegends.com/cdn/10.7.1/data/en_US/champion.json'
}

API_VERSIONS = {
    'summoner_version': '4',
    'league_version': '4',
    'champion_mastery_version': '4'
}

# DO NOT TOUCH THIS DICTIONARY
REGIONS = {
    'brazil': 'br1',
    'europe_nordic_and_east': 'eun1',
    'europe_west': 'euw1',
    'japan': 'jp1',
    'korea': 'kr1',
    'latin_america_north': 'la1',
    'latin_america_south': 'la2',
    'north_america': 'na1',
    'oceana': 'oc1',
    'russia': 'ru',
    'turkey': 'tr1'
}