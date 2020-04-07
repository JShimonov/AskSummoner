import LoLConsts as Consts
import requests

class LeagueAPI():

    def __init__(self, api_key, region = Consts.REGIONS['north_america']):
        self.api_key = api_key  
        self.region = region    # this gives me the proxy
    
    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.get(
            Consts.LEAGUE_URL['base'].format(
                proxy = self.region,
                url = api_url
            )
        )
        params = args
        #print(response.url)
        return response.json()
    
    def rank_of_summoner(self, id):
        api_url = Consts.LEAGUE_URL['entries_by_summoner'].format(
            version = Consts.API_VERSIONS['league_version'],
            summoner_id = id,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)