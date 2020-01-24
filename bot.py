import sys
import traceback

from discord.ext.commands import *
import bot_database
import bot_errors
import bot_helpers

TOKEN = open("data\\token.txt").read()


# Fallback for reaction adds / removes when Bot is offline:
# 1. For every combination of {messageID + Emoji} that appears in the database, save all userIDs that reacted to it in the database
# 2. When the bot starts up, check all the reactions on all of these messages and determine differences, then add / remove roles accordingly


bot_database.initialise_db()

bot = Bot(command_prefix='!', description="MisterL's utility bot")

bot.load_extension("bot_events")
bot.load_extension("bot_commands")


@bot.event
async def on_error(event, *args, **kwargs):
    exc_type, exc_value, exc_traceback = sys.exc_info()

    # Ignore ProcessAborted
    if exc_type == bot_errors.ProcessAborted:
        return

    trace = exc_value.__traceback__
    verbosity = 4
    lines = traceback.format_exception(exc_type, exc_value, trace, verbosity)
    traceback_text = ''.join(lines)
    print(traceback_text, file=sys.stderr)


print("Logging in...")
bot.run(TOKEN)


