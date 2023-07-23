import pymongo
from decouple import config
from APIs.twitch_api import TwitchAPI

client = pymongo.MongoClient(f"mongodb+srv://shiro_47:{config('MONGODB_PASSWORD')}@gs-discord.y06kt.mongodb.net/?retryWrites=true&w=majority")

class TwitchDB:
    def __init__(self, server_id: str):
        self.server = client[server_id]
        self.collection = self.server["TWITCH_DB"]
        
    def check_existence(self, streamer: str) -> bool:
        return self.collection.find_one({"streamer_name": streamer}) is not None
    
    def add_streamer(self, streamers: list) -> bool:
        existing_streamers = [streamer for streamer in streamers if self.check_existence(streamer)]
        new_streamers = [streamer.lower() for streamer in streamers if not self.check_existence(streamer)]
        
        if new_streamers:
            self.collection.insert_many([{"streamer_name": streamer} for streamer in new_streamers])
        
        return not bool(existing_streamers)

    
    def remove_streamer(self, streamer: str) -> bool:
        if self.check_existence(streamer):
            self.collection.delete_one({"streamer_name": streamer})
            return True
        return False
        
    def get_all_streamers(self) -> list:
        return list(self.collection.find())

    def get_all_existing_streamers(self) -> list:
        streamers = self.get_all_streamers()
        active_streamers = [streamer for streamer in streamers if TwitchAPI().check_streamer_existence(streamer["streamer_name"])]
        return active_streamers