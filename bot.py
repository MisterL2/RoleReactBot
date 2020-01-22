from discord.ext.commands import *

TOKEN = open(
    "C:\\Users\\tramp\\Documents\\Programming\\Python Projekte\\Discord bots\\ReactionRolesv2\\token.txt").read()

# MessageID : Emoji : RoleID
# Persist in db using h2

# Fallback for reaction adds / removes when Bot is offline:
# 1. For every combination of {messageID + Emoji} that appears in the database, save all userIDs that reacted to it in the database
# 2. When the bot starts up, check all the reactions on all of these messages and determine differences, then add / remove roles accordingly


# Clean up no-longer-existant messages
# Clean up no-longer-existant guilds
# Clean up no-longer-existant roles

# Maybe clean up reactions for users that are no longer on the server?

bot = Bot(command_prefix='!', description="MisterL's utility bot")

bot.load_extension("bot_events")
bot.load_extension("bot_commands")


bot.run(TOKEN)
