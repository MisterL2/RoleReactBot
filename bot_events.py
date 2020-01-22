from discord import RawReactionActionEvent
from discord.ext.commands import Cog, CommandError, MissingPermissions
from bot_database import get_roleID

def setup(bot):
    bot.add_cog(Bot_Listeners(bot))


class Bot_Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        # Check if globally unique message_id & emoji are in db
        await get_roleID(payload.message_id, payload.emoji)
        print("Reaction was added")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print("Reaction was removed")

    @Cog.listener()
    async def on_command_error(self, ctx, error: CommandError):
        if isinstance(error, MissingPermissions):
            await ctx.send("You do not have the permissions to use this command!")
        print("Some error occurred!")
