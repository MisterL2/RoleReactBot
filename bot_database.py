import os
import sqlite3

cur = None


def initialise_db():
    db = "data\\database.db"
    database_exists = os.path.isfile(db)
    conn = sqlite3.connect(db, isolation_level=None)

    global cur
    cur = conn.cursor()

    if database_exists:
        print("Database exists")
    else:
        cur.execute("CREATE TABLE messages ("
                    "guildID TEXT,"  # Actually a huge int (snowflake). GuildID is only saved to detect missing guilds, the messageID itself is already globally unique.
                    "messageID TEXT,"  # Actually a huge int (snowflake)
                    "emoji TEXT,"
                    "roleID TEXT NOT NULL,"  # Actually a huge int (snowflake)
                    "PRIMARY KEY (messageID, emoji)"
                    ");")
        print("Database created!")


async def save_entry_to_db(guild_id: int, message_id: int, emoji: str, role_id: int):  # message_ID is globally unique
    cur.execute("INSERT INTO messages VALUES (?,?,?,?)", (int(guild_id), int(message_id), emoji, int(role_id)))  # Explicit casts to int, in case they were previously somehow malformed
    # print("DEBUG: Saved role to db...")


async def delete_entry_from_db(message_id: int, emoji: str):  # message_ID is globally unique
    role_id = await get_role_id(message_id, emoji)
    if role_id is not None:
        cur.execute("DELETE FROM messages WHERE messageID = ? AND emoji = ?", (int(message_id), emoji))  # Explicit casts to int, in case they were previously somehow malformed
        # print("DEBUG: Removed role from db...")
    return role_id  # Might be None


# Get the role_ID determined by a combination of message_ID and an emoji from the database
async def get_role_id(message_id: int, emoji_name: str):
    # print(f"DEBUG: Getting role for id: {message_id} and emoji {emoji_name}")
    cur.execute("SELECT roleID FROM messages WHERE messageID = ? AND emoji = ?", (int(message_id), emoji_name))  # Explicit casts to int, in case they were previously somehow malformed
    rows = cur.fetchall()

    if len(rows) == 1:
        return int(rows[0][0])  # Return the roleID
    elif len(rows) > 1:
        print("CRITICAL: Multiple roleIDs returned for one messageID-emoji combination!")
    # If len(rows) != 1, None is returned


async def get_all_saved_messages():
    cur.execute("SELECT * FROM messages")
    return cur.fetchall()


async def delete_entries(outdated_entries: [[]]):
    print("Deleting outdated entries...")
    print(outdated_entries)
    cur.executemany("DELETE FROM messages WHERE guildID = ? AND messageID = ? AND emoji = ? AND roleID = ?", outdated_entries)

# Delete all mentions to a role from the database
async def delete_role(role_id: int):
    cur.execute("DELETE FROM messages WHERE roleID = ?", (int(role_id),))
