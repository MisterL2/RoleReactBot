from discord import Message, Role
from discord.ext import commands
from discord.ext.commands import *

from bot_database import save_role_to_db


def setup(bot):
    bot.add_cog(Bot_Commands(bot))


class Bot_Commands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Usage: !addRole [MessageID] [Emoji] [RoleID]
    @commands.command(name="addRole")
    @has_permissions(administrator=True)
    async def add_role(self, ctx, message: Message, emoji, role: Role):
        await save_role_to_db(message.id, emoji, role.id)
        await ctx.send(f'Role "{role.name}" added with emoji {emoji}')

    # Usage: TBD
    @commands.command(name="removeRole")
    @has_permissions(administrator=True)
    async def remove_role(self, ctx):
        await ctx.send('Removed a role.')