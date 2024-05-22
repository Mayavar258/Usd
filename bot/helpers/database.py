from bot import MONGO_DB
from motor import motor_asyncio


class MONGODB:
    def __init__(self) -> None:
        self.client = motor_asyncio.AsyncIOMotorClient(MONGO_DB)
        self.db = self.client["spamBanBot"]
        self.mutes = self.db["mutes"]
        self.bans = self.db["bans"]
    
    def new_chats(self, old_chats, new_chats):
        if not old_chats:
            return new_chats
        if isinstance(new_chats, int):
            new_chats = [new_chats]
        return list(set(old_chats + new_chats))
    
    async def add_gmute(self, user_id: int, chat_ids):
        if is_exist := await self.mutes.find_one({"user_id": user_id}):
            chat_ids = self.new_chats(is_exist.get("chat_ids"), chat_ids)
            await self.mutes.update_one({"user_id": user_id}, {"$set": {"chat_ids": chat_ids}})
        else:
            await self.mutes.insert_one({"user_id": user_id, "chat_ids": chat_ids})
    
    async def add_gban(self, user_id: int, chat_ids):
        if is_exist := await self.bans.find_one({"user_id": user_id}):
            chat_ids = self.new_chats(is_exist.get("chat_ids"), chat_ids)
            await self.bans.update_one({"user_id": user_id}, {"$set": {"chat_ids": chat_ids}})
        else:
            await self.bans.insert_one({"user_id": user_id, "chat_ids": chat_ids})

    async def is_gmuted(self, user_id: int):
        return await self.mutes.find_one({"user_id": user_id})
    
    async def is_gbanned(self, user_id: int):
        return await self.bans.find_one({"user_id": user_id})
    
    async def remove_gmute(self, user_id):
        await self.mutes.delete_one({"user_id": user_id})
    
    async def remove_gban(self, user_id):
        await self.bans.delete_one({"user_id": user_id})

db = MONGODB()