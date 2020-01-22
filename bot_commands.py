from discord import Message, Role
from discord.ext import commands
from discord.ext.commands import *

from bot_database import save_role_to_db, delete_role_from_db


def setup(bot):
    bot.add_cog(BotCommands(bot))


class BotCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Usage: !addRole [MessageID] [Emoji] [RoleID]
    @commands.command(name="addRole")
    @has_permissions(administrator=True)
    async def add_role(self, ctx, message: Message, emoji, role: Role):
        await save_role_to_db(message.id, emoji, role.id)
        await ctx.send(f'Added Role "{role.name}" with emoji "{emoji}"')

    # Usage: !removeRole [MessageID] [Emoji] [RoleID]
    @commands.command(name="removeRole")
    @has_permissions(administrator=True)
    async def remove_role(self, ctx, message: Message, emoji, role: Role):
        await delete_role_from_db(message.id, emoji, role.id)
        await ctx.send(f'Removed Role "{role.name}" with emoji "{emoji}"')