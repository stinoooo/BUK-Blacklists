from pymongo import MongoClient
import datetime

client = MongoClient('your_mongodb_uri')
db = client['blacklistdb']
blacklist_col = db['blacklist']

def blacklist_user(user_id, reason, blacklisted_by, banned_servers, case_id):
    """Insert a new blacklist entry into the database."""
    blacklist_col.insert_one({
        "user_id": user_id,
        "reason": reason,
        "blacklisted_by": blacklisted_by,
        "banned_servers": banned_servers,
        "date_blacklisted": datetime.datetime.utcnow(),  # Store the date of blacklisting
        "case_id": case_id  # Store the case ID
    })

def unblacklist_user(user_id):
    """Remove a user from the blacklist in the database and log the unblacklist date."""
    blacklist_col.update_one({"user_id": user_id}, {"$set": {"date_unblacklisted": datetime.datetime.utcnow()}})  # Log unblacklist date
    blacklist_col.delete_one({"user_id": user_id})  # Optionally, you can delete the entry or retain it

def fetch_blacklist_status(user_id):
    """Fetch the blacklist status of a user."""
    return blacklist_col.find_one({"user_id": user_id})

def edit_blacklist_reason(case_id, new_reason):
    """Edit the reason for a specific blacklist case."""
    result = blacklist_col.update_one({"case_id": case_id}, {"$set": {"reason": new_reason}})
    return result.modified_count > 0  # Return True if the reason was updated