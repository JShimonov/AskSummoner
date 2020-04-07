import LoLConsts as Consts
import requests

class SummonerAPI():

    def __init__(self, api_key, region = Consts.REGIONS['north_america']):
        self.api_key = api_key  
        self.region = region    # this gives me the proxy
    
    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.get(
            Consts.SUMMONER_URL['base'].format(
                proxy = self.region,
                url = api_url
            ),
            Consts.LEAGUE_URL['base'].format(
                proxy = self.region,
                url = api_url
            )
        )
        params = args
        #print(params)
        # print(response.url)
        return response.json()

    def get_summoner_by_name(self, name) :
        api_url = Consts.SUMMONER_URL['summoner_by_name'].format(
            version = Consts.API_VERSIONS['summoner_version'],
            names = name,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)
