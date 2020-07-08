from discord import Guild, Message, NotFound
from discord.ext.commands import EmojiConverter
import re

async def find_message(guild: Guild, message_id: int) -> Message:  # Returns the message, or None if there is no message
    for channel in guild.text_channels:
        try:
            return await channel.fetch_message(message_id)  # Returns only if there is a message (otherwise NotFound exception is raised)
        except NotFound:
            pass

def get_emoji_identifier(emoji):
    if re.match(r"<:\w+:\d+>", str(emoji)):
        emoji_id = str(emoji).split(":")[2][:-1]
        return emoji_id
    else:
        return str(emoji)