import pymongo
from decouple import config

client = pymongo.MongoClient(f"mongodb+srv://shiro_47:{config('MONGODB_PASSWORD')}@gs-discord.y06kt.mongodb.net/?retryWrites=true&w=majority")

class ApexDB():
    
    def __init__(self, server_id):
        self.server = client[server_id]
        self.collection = self.server["APEX_DB"]
    
    def check_existence(self, discordID):
        return self.collection.find_one({"DiscordID": discordID}) is not None
    
    def check_existence_by_name(self, playerName) -> bool:
        return self.collection.find_one({"ID": playerName}) is not None
            
    def add_player(self, platform, nickname, discordID):
        if not self.check_existence(discordID):
            self.collection.insert_one({'platform': platform, 'ID': nickname, 'DiscordID': discordID})
            return True
        return False

    def remove_player(self, discordID):
        if self.check_existence(discordID):
            self.collection.delete_one({"DiscordID": discordID})
            return True
        return False

    def remove_player_by_name(self, playerName) -> bool:
        if self.check_existence_by_name(playerName):
            self.collection.delete_one({"ID": playerName})
            return True
        return False
    
    def get_all_players(self):
        return list(self.collection.find())

    def get_player(self, discordID):
        if self.check_existence(discordID):
            return self.collection.find_one({"DiscordID": discordID})
        return False
