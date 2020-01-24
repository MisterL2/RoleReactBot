from discord import RawReactionActionEvent, Embed
from discord.ext.commands import Cog, CommandError, MissingPermissions

import bot_database
import bot_helpers
from bot_database import get_role_id
from bot_errors import MissingObjectException, ProcessAborted


def setup(bot):
    bot.add_cog(BotListeners(bot))


class BotListeners(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        print('Logged in as {0.user}'.format(self.bot))
        await self.clean_guilds()

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        # Ignore own reactions
        if payload.user_id == self.bot.user.id:
            return

        member, role = await self.reaction_role_change(payload)

        # Add role
        await member.add_roles(role, reason="Removed by MisterL's UtilityBot")

        # Inform user
        guild = self.bot.get_guild(payload.guild_id)
        await member.send(embed=Embed(title=f"Role `{role.name}` assigned in `{guild.name}`", description="Thanks for using Utility Bot!"))

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Ignore own reactions
        if payload.user_id == self.bot.user.id:
            return

        member, role = await self.reaction_role_change(payload)

        # Remove role
        await member.remove_roles(role, reason="Removed by MisterL's UtilityBot")

        # Inform user
        guild = self.bot.get_guild(payload.guild_id)
        await member.send(embed=Embed(title=f"Role `{role.name}` removed in `{guild.name}`", description="Thanks for using Utility Bot!"))

    @Cog.listener()
    async def on_command_error(self, ctx, error: CommandError):
        if isinstance(error, MissingPermissions):
            await ctx.send("You do not have the permissions to use this command!")

        print("Some error occurred!")
        print(f"Error: {error}")

    async def reaction_role_change(self, payload: RawReactionActionEvent):  # Returns either a (Member, Role) Tuple, or raises an exception which is handled in on_command_error
        # If not on a server
        if payload.guild_id is None:
            raise ProcessAborted

        guild = self.bot.get_guild(payload.guild_id)

        if guild is None:
            raise MissingObjectException(payload.guild_id, "guild_id")

        member = guild.get_member(payload.user_id)

        if member is None:
            raise ProcessAborted

        # Check if globally unique message_id & emoji are in db
        role_id = await get_role_id(payload.message_id, payload.emoji.name)

        if role_id is None:  # Other emoji or other message (or both) than in the db
            raise ProcessAborted

        role = guild.get_role(role_id)

        if role is None:
            raise MissingObjectException(role_id, "role_id")

        return member, role

    async def clean_guilds(self):
        print("Checking for outdated entries...")
        guild_list = {guild.id: guild for guild in self.bot.guilds}

        entries = await bot_database.get_all_saved_messages()
        outdated_entries = []
        for entry in entries:
            # Clean up no-longer-existent guilds
            keys = guild_list.keys()
            if int(entry[0]) not in guild_list.keys():
                outdated_entries.append(entry)
                continue

            # Clean up no-longer-existent roles
            guild = guild_list.get(int(entry[0]))  # Get the guild by its ID. The guild exists as checked by previous if-statement
            if guild.get_role(int(entry[3])) is None:  # If the role no longer exists
                outdated_entries.append(entry)
                continue

            # Clean up no-longer-existent messages
            message = await bot_helpers.find_message(guild, int(entry[1]))
            if message is None:
                outdated_entries.append(entry)
                continue

        if outdated_entries:
            await bot_database.delete_entries(outdated_entries)

        print("All entries up to date!")
