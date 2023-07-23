import pymongo
from decouple import config

client = pymongo.MongoClient(f"mongodb+srv://shiro_47:{config('MONGODB_PASSWORD')}@gs-discord.y06kt.mongodb.net/?retryWrites=true&w=majority")


class ConfigDB:
    
    def __init__(self, server_id: str):
        self.server = client[server_id]
        self.collection = self.server["CONFIG"]

    def create_ids_for_map_rotation(self, channel_id: int, message_id: int, message_id_ranked: int):
        data = {
            "Name": "Map_rotation",
            "channel_id": channel_id, 
            "message_id": message_id,
            "message_id_ranked": message_id_ranked
        }
        self.collection.replace_one({"Name": "Map_rotation"}, data, upsert=True)
            
    def create_ids_for_pred(self, channel_id: int, message_id: int):
        data = {
            "Name": "Predator_embed",
            "channel_id": channel_id, 
            "message_id": message_id
        }
        self.collection.replace_one({"Name": "Predator_embed"}, data, upsert=True)
        
    def create_ids_for_apex_leaderboard(self, channel_id: int, IDs: list):
        data = {
            "Name": "Leaderbord_IDs",
            "channel_id": channel_id,
            "message_ids": IDs
        }
        self.collection.replace_one({"Name": "Leaderbord_IDs"}, data, upsert=True)
            
    def create_ids_for_streams_list(self, channel_id: int):
        data = {
            "Name": "Streams_list",
            "channel_id": channel_id
        }
        self.collection.replace_one({"Name": "Streams_list"}, data, upsert=True)
            
    def check_ids_for_map_rotation(self):
        return self.collection.find_one({"Name": "Map_rotation"})
    
    def check_ids_for_pred(self):
        return self.collection.find_one({"Name": "Predator_embed"})
    
    def check_ids_for_apex_leaderboard(self):
        return self.collection.find_one({"Name": "Leaderbord_IDs"})
    
    def check_ids_for_streams_list(self):
        return self.collection.find_one({"Name": "Streams_list"})
