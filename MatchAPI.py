import LoLConsts as Consts
import requests

# This is by far the coolest API, gives access to most parts of the player and the value of the player themselves
# -> shows if the Summoner is a carry, a team player, or just not good at the moment

class MatchAPI():

    def __init__(self, api_key, region = Consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
            Consts.MATCH_URL['base'].format(
                proxy = self.region,
                url = api_url
            )
        )
        params = args
        return response.json()

    def get_matchlist(self, acct_id):
        api_url = Consts.MATCH_URL['matchlists_by_account'].format(
            version = Consts.API_VERSIONS['match_version'],
            account_id = acct_id,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)
    
    def get_matchlist_ranked(self, acct_id, champ, que):
        api_url = Consts.MATCH_URL['matchlists_by_account_ranked'].format(
            version = Consts.API_VERSIONS['match_version'],
            account_id = acct_id,
            champion = champ,
            queue = que,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)

    def get_match(self, match_id):
        api_url = Consts.MATCH_URL['matches'].format(
            version = Consts.API_VERSIONS['match_version'],
            matchId = match_id,
            api_key = Consts.KEY['api_key']
        )
        return self._request(api_url)