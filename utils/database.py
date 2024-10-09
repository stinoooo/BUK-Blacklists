from pymongo import MongoClient
import datetime

client = MongoClient('your_mongodb_uri')
db = client['blacklistdb']
blacklist_col = db['blacklist']

def blacklist_user(user_id, reason, blacklisted_by, banned_servers):
    blacklist_col.insert_one({
        "user_id": user_id,
        "reason": reason,
        "blacklisted_by": blacklisted_by,
        "banned_servers": banned_servers,
        "date_blacklisted": datetime.datetime.utcnow()
    })

def unblacklist_user(user_id):
    blacklist_col.delete_one({"user_id": user_id})

def fetch_blacklist_status(user_id):
    return blacklist_col.find_one({"user_id": user_id})
