async def save_role_to_db(message_ID: int, emoji, role_ID: int):  # message_ID is globally unique
    print("Saving role to db...")
    print(message_ID)
    print(emoji)
    print(role_ID)


async def delete_role_from_db(message_ID: int, emoji, role_ID: int):  # message_ID is globally unique
    print("Removing role from db...")
    print(message_ID)
    print(emoji)
    print(role_ID)


# Get the role_ID determined by a combination of message_ID and an emoji from the database
async def get_roleID(message_ID: int, emoji):
    print("Getting roleID from database!")
    print(emoji.name)
    print(message_ID)
    role_ID = 669633862183157779
    return role_ID
