from discord.ext.commands import *

TOKEN = open(
    "C:\\Users\\tramp\\Documents\\Programming\\Python Projekte\\Discord bots\\ReactionRolesv2\\token.txt").read()

# Accept commands only from those with administrator permissions
# ServerID : ChannelID : MessageID : Emoji : RoleID
# Persist in db using h2

# Add new role react
# Remove role react


bot = Bot(command_prefix='!', description="MisterL's utility bot")

bot.load_extension("bot_events")
bot.load_extension("bot_commands")








bot.run(TOKEN)
