from discord.ext.commands import CommandError


class CommandNullException(CommandError):
    def __init__(self, object_id: int, object_type: str):
        self.object_id, self.object_type = object_id, object_type


# When an error does not need to be responded to at all. For example, this may be raised when a user uses a different reaction that shouldn't interact with this bot
class UselessError(CommandError):
    pass
