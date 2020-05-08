import LoLConsts as Consts
import requests

class ClashAPI():

    def __init__(self, api_key, region = Consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
            Consts.CLASH_URL['base'].format(
                proxy = self.region,
                url = api_url
            )
        )
        params = args
        return response.json()

    def get_team_from_summoner(self, id):
        api_url = Consts.CLASH_URL['players_by_summoner'].format(
            version = Consts.API_VERSIONS['clash_version'],
            summoner_id = id,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)

    def get_summoners_from_team(self, teamId):
        api_url = Consts.CLASH_URL['teams_by_id'].format(
            version = Consts.API_VERSIONS['clash_version'],
            team_id = teamId,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)