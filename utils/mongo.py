from motor.motor_asyncio import AsyncIOMotorClient

class PreferencesManager:
    def __init__(self, mongo_uri: str, db_name: str = "scipnet", collection_name: str = "guilds"):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    # --------------------------
    # Save/Update Preference
    # --------------------------
    async def set_pref(self, guild_id: int, key: str, value):
        await self.collection.update_one(
            {"_id": guild_id},
            {"$set": {key: value}},
            upsert=True
        )

    # --------------------------
    # Get a Single Preference
    # --------------------------
    async def get_pref(self, user_id: int, key: str):
        doc = await self.collection.find_one({"_id": user_id})
        if doc:
            return doc.get(key)
        return None

    # --------------------------
    # Get All Preferences
    # --------------------------
    async def get_all_prefs(self, user_id: int):
        doc = await self.collection.find_one({"_id": user_id})
        return doc or {}

    # --------------------------
    # Delete a Preference
    # --------------------------
    async def delete_pref(self, user_id: int, key: str):
        await self.collection.update_one(
            {"_id": user_id},
            {"$unset": {key: ""}}
        )

    # --------------------------
    # Delete ALL user prefs
    # --------------------------
    async def delete_user(self, user_id: int):
        await self.collection.delete_one({"_id": user_id})