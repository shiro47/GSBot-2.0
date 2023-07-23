import pymongo
from decouple import config

client = pymongo.MongoClient(f"mongodb+srv://shiro_47:{config('MONGODB_PASSWORD')}@gs-discord.y06kt.mongodb.net/?retryWrites=true&w=majority")

class WhitelistDB:
    def __init__(self):
        self.server = client["GENERAL"]
        self.collection = self.server["WHITELIST"]
    
    def add_user(self, userName: str, userId: int, avatarUrl: str, serverId: int) -> bool:
        if not self.check_existence(userId):
            self.collection.insert_one({
                "userId": userId,
                "userName": userName,
                "avatarUrl": avatarUrl,
                "servers": [],
            })
            return self.add_server_to_user(userId, serverId)
        return self.add_server_to_user(userId, serverId)
    
    def check_existence(self, userId: int) -> bool:
        return self.collection.find_one({"userId": userId}) is not None
    
    def remove_user(self, userId: int) -> bool:
        if self.check_existence(userId):
            self.collection.delete_one({"userId": userId})
            return True
        return False
        
    def get_all_users(self) -> list:
        return list(self.collection.find())

    def add_server_to_user(self, userId: int, serverId: int) -> bool:
        if self.check_existence(userId):
            self.collection.update_one(
                {"userId": userId},
                {"$addToSet": {"servers": serverId}}
            )
            return True
        return False
    
    def get_all_user_servers(self, userId: int) -> list:
        user = self.collection.find_one({"userId": userId})
        if user:
            return user["servers"]
        return []
    
