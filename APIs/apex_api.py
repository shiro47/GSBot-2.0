import time
import json
import requests
from decouple import config

class Apex_API():
    def __init__(self) -> None:
        self.token=config('APEX_TOKEN')
        self.errors = {400: "Try again in a few minutes.",
                       405: "External API error.",
                       429: "Rate limit reached.",
                       500: "Internal error."}
        self.fatal_errors = {403: "Unauthorized / Unknown API key.",
                             404: "The player could not be found.",
                             410: "Unknown platform provided.",
                             }

    def pred_threshold(self):
        www2=requests.get(f'https://api.mozambiquehe.re/predator?auth={self.token}')
        if www2.status_code!=200:
            print(f'{self.errors[www2.status_code]} Fixing error {www2.status_code}...')
            time.sleep(5)
            return self.pred_threshold()
        if www2.status_code==200:
            try:
                parsed_json = (json.dumps(www2.json()))
                BR_info = (json.loads(parsed_json)["RP"]["PC"])
            except KeyError:
                time.sleep(5)
                return self.pred_threshold()
            return BR_info['val'], BR_info['totalMastersAndPreds']

    def get_rankScore(self,platform,player):
        www2=requests.get(f'https://api.mozambiquehe.re/bridge?auth={self.token}&player={player}&platform={platform}')
        if www2.status_code in self.fatal_errors:
            print(f"{www2.status_code}: {self.fatal_errors[www2.status_code]} ({platform}, {player})")
            return None
        if www2.status_code!=200:
            print(f'{self.errors[www2.status_code]} Fixing error {www2.status_code}...')
            time.sleep(5)
            return self.get_rankScore(platform,player)
        if www2.status_code==200:
            try:
                parsed_json=(json.dumps(www2.json()))
                player_rank_info=(json.loads(parsed_json)["global"]["rank"])
            except KeyError:
                time.sleep(5)
                return self.get_rankScore(platform,player)
            return player_rank_info['rankName'], player_rank_info['rankScore'], player_rank_info['rankDiv']


    def map_rotation_data(self):
        www2=requests.get(f'https://api.mozambiquehe.re/maprotation?auth={self.token}&version=2')
        if www2.status_code!=200:
            print(f'{self.errors[www2.status_code]} Fixing error {www2.status_code}...')
            time.sleep(5)
            return self.map_rotation_data()
        if www2.status_code==200:
            try:
                parsed_json=(json.dumps(www2.json()))
                current_map_info=(json.loads(parsed_json)["battle_royale"]["current"])
                next_map_info=(json.loads(parsed_json)["battle_royale"]["next"])
                ranked_current_map_info=(json.loads(parsed_json)["ranked"]["current"])
                ranked_next_map_info=(json.loads(parsed_json)["ranked"]["next"])
            except KeyError:
                time.sleep(5)
                return self.map_rotation_data()
            return {"pubs":[current_map_info['map'], current_map_info['remainingTimer'], next_map_info['map'], next_map_info['readableDate_start'], next_map_info['readableDate_end'],current_map_info['asset']],
                    "ranked":[ranked_current_map_info['map'], ranked_current_map_info['remainingTimer'], ranked_next_map_info['map'], ranked_next_map_info['readableDate_start'], ranked_next_map_info['readableDate_end'],ranked_current_map_info['asset']]}
        