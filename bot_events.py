from discord import RawReactionActionEvent
from discord.ext.commands import Cog, CommandError, MissingPermissions
from bot_database import get_roleID
from bot_errors import CommandNullException, UselessError


def setup(bot):
    bot.add_cog(BotListeners(bot))


class BotListeners(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        member, role = await self.reaction_role_change(payload)
        await member.add_roles(role, reason="Removed by MisterL's UtilityBot")

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member, role = await self.reaction_role_change(payload)
        await member.remove_roles(role, reason="Removed by MisterL's UtilityBot")

    @Cog.listener()
    async def on_command_error(self, ctx, error: CommandError):
        if isinstance(error, MissingPermissions):
            await ctx.send("You do not have the permissions to use this command!")
        elif isinstance(error, CommandNullException):
            print("Something was deleted:", end="")
            print(error.object_id, end=" | ")
            print(error.object_type)
        print("Some error occurred!")
        print(f"Error: {error}")

    async def reaction_role_change(self, payload: RawReactionActionEvent):  # Returns either a (Member, Role) Tuple, or raises an exception which is handled in on_command_error
        # If not on a server:
        if payload.guild_id is None:
            raise UselessError

        guild = self.bot.get_guild(payload.guild_id)

        if guild is None:
            raise CommandNullException(payload.guild_id, "guild")

        member = guild.get_member(payload.user_id)

        if member is None:
            raise UselessError

        # Check if globally unique message_id & emoji are in db
        role_id = await get_roleID(payload.message_id, payload.emoji)

        if role_id is None:  # Other emoji or other message (or both) than in the db
            raise UselessError

        role = guild.get_role(role_id)

        return member, role
