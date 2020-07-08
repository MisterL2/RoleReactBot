from discord import Role
from discord.ext import commands
from discord.ext.commands import *
import bot_helpers

from bot_database import save_entry_to_db, delete_entry_from_db


def setup(bot):
    bot.add_cog(BotCommands(bot))


class BotCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._last_member = None

    # Usage: !addRole [MessageID] [Emoji] [RoleID]
    @commands.command(name="addRole")
    @has_permissions(administrator=True)
    async def add_role(self, ctx: Context, message_id: int, emoji, role: Role):

        # Check that message really exists
        message = await bot_helpers.find_message(ctx.guild, message_id)
        if message is None:
            await ctx.send(f"There is no message with id `{message_id}` on this server!")
            return

        # Add the info to the db
        await save_entry_to_db(ctx.guild.id, message_id, emoji, role.id)
        await ctx.send(f'Added Role `{role.name}` with emoji `{emoji}`')
        print(f'Added Role `{role.name}` with emoji `{emoji}`')

        # Add a reaction to the message
        await message.add_reaction(emoji)

    # Usage: !removeRole [MessageID] [Emoji] [RoleID]
    @commands.command(name="removeRole")
    @has_permissions(administrator=True)
    async def remove_role(self, ctx: Context, message_id: int, emoji):

        role_id = await delete_entry_from_db(message_id, emoji)
        # If there was no such entry to begin with
        if role_id is None:
            await ctx.send(f"There is no entry for a message with id `{message_id}` in combination with `emoji`!")
            return

        role = ctx.guild.get_role(role_id)
        await ctx.send(f'Removed Role `{role.name}` with emoji `{emoji}`')
        print(f'Removed Role `{role.name}` with emoji `{emoji}`')
        
        message = await bot_helpers.find_message(ctx.guild, message_id)
        if message is not None:
            await message.remove_reaction(emoji, self.bot.user)  # Remove the Bot's reaction




