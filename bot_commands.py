from discord import Role, NotFound
from discord.ext import commands
from discord.ext.commands import *

from bot_database import save_role_to_db, delete_role_from_db


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
        for channel in ctx.guild.text_channels:
            try:
                maybe_message = await channel.fetch_message(message_id)
                print(maybe_message)
                break
            except NotFound:
                pass
        else:  # If the message was not found
            await ctx.send(f"There is no message with id `{message_id}` on this server!")
            return

        # If the message exists, add the info to the db
        await save_role_to_db(message_id, emoji, role.id)
        await ctx.send(f'Added Role `{role.name}` with emoji `{emoji}`')

    # Usage: !removeRole [MessageID] [Emoji] [RoleID]
    @commands.command(name="removeRole")
    @has_permissions(administrator=True)
    async def remove_role(self, ctx: Context, message_id: int, emoji):

        role_id = await delete_role_from_db(message_id, emoji)
        # If there was no such entry to begin with
        if role_id is None:
            await ctx.send(f"There is no entry for a message with id `{message_id}` in combination with `emoji`!")
            return

        role = await RoleConverter().convert(ctx, role_id)

        await ctx.send(f'Removed Role `{role.name}` with emoji `{emoji}`')
