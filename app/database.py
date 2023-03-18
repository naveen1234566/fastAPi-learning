"""DATABASE
MongoDB database initialization
"""

# # Installed # #
from pymongo import MongoClient
from pymongo.collection import Collection

# # Package # #
from .core.settings import mongo_settings as settings

__all__ = ("client", "collection")

client = MongoClient(settings.uri)

users: Collection = client[settings.database]["users"]
ethernet: Collection = client[settings.database]["ethernet"]
templete: Collection = client[settings.database]["templete"]
notification: Collection = client[settings.database]["notification"]
iReach: Collection = client[settings.database]["iReach"]
