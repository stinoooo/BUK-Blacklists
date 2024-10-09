from pymongo import MongoClient
import datetime

# Replace with your actual MongoDB URI
client = MongoClient('your_mongodb_uri')
db = client['blacklistdb']
blacklist_col = db['blacklist']

def blacklist_user(user_id, username, reason, blacklisted_by, banned_servers, case_id):
    """Store a new blacklist entry in the database."""
    blacklist_col.insert_one({
        "user_id": user_id,
        "username": username,
        "reason": reason,
        "blacklisted_by": blacklisted_by,
        "banned_servers": banned_servers,
        "case_id": case_id,
        "date_blacklisted": datetime.datetime.utcnow()  # Use utcnow for consistency
    })

def unblacklist_user(user_id):
    """Remove a user from the blacklist in the database and log the unblacklist date."""
    # Optionally log unblacklist date without deleting the entry
    blacklist_col.update_one({"user_id": user_id}, {"$set": {"date_unblacklisted": datetime.datetime.utcnow()}})
    # If you prefer to delete the entry instead of just marking it unblacklisted, uncomment the line below
    # blacklist_col.delete_one({"user_id": user_id})

def fetch_blacklist_status(identifier):
    """Fetch the blacklist status of a user by user ID or username."""
    # Check if identifier is a number (user ID) or a string (username)
    if isinstance(identifier, int):
        return blacklist_col.find_one({"user_id": identifier})
    else:
        return blacklist_col.find_one({"username": identifier})

def edit_blacklist_reason(case_id, new_reason):
    """Edit the reason for a specific blacklist case."""
    result = blacklist_col.update_one({"case_id": case_id}, {"$set": {"reason": new_reason}})
    return result.modified_count > 0  # Return True if the reason was updated