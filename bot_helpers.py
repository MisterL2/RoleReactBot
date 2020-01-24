from discord import Guild, Message, NotFound


async def find_message(guild: Guild, message_id: int) -> Message:  # Returns the message, or None if there is no message
    for channel in guild.text_channels:
        try:
            return await channel.fetch_message(message_id)  # Returns only if there is a message (otherwise NotFound exception is raised)
        except NotFound:
            pass
