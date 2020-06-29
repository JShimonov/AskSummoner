import LoLConsts as Consts
import requests

import urllib.request as url
import json
import urllib.parse
import ast

class ChampMasteryAPI():

    def __init__(self, api_key, region = Consts.REGIONS['north_america']):
        self.api_key = api_key  
        self.region = region    # this gives me the proxy

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.get(
            Consts.CHAMP_MASTERY_URL['base'].format(
                proxy = self.region,
                url = api_url
            )
        )
        params = args
        #print(response.url)
        return response.json()

    def get_all_masteries(self, id):
        api_url = Consts.CHAMP_MASTERY_URL['champion_masteries_by_summoner'].format(
            version = Consts.API_VERSIONS['champion_mastery_version'],
            summoner_id = id,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)
    
    # make a dictionary that assigns each champion_id to its own champion
    # use Consts.CHAMP_MASTERY_URL['all_champs'] to scrape all the champions and their keys
    def all_champions(self):
        request = url.Request(Consts.CHAMP_MASTERY_URL['all_champs'])
        data = url.urlopen(request).read()
        data = data.decode("utf-8")
        data = ast.literal_eval(data)
        data = json.dumps(data)
        array = json.loads(data)
        champ_dict = array['data']
        dict = {}                       # this will hold all the id's to champ_keys
        for key in champ_dict:
            dict[champ_dict[key]['key']] = key
        return dict
        
    def get_champion(self, championId):
        return self.all_champions().get(championId)

    def get_championId(self, championName):
        key_list = list(self.all_champions().keys())
        val_list = list(self.all_champions().values())
        return(key_list[val_list.index(championName)])

    
