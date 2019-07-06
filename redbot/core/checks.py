import warnings
from typing import Awaitable, TYPE_CHECKING, Dict

import discord

from .commands import (
    bot_has_permissions,
    has_permissions,
    is_owner,
    guildowner,
    guildowner_or_permissions,
    admin,
    admin_or_permissions,
    mod,
    mod_or_permissions,
    check as _check_decorator,
)
from .utils.mod import (
    is_mod_or_superior as _is_mod_or_superior,
    is_admin_or_superior as _is_admin_or_superior,
    check_permissions as _check_permissions,
)

if TYPE_CHECKING:
    from .bot import Red
    from .commands import Context

__all__ = [
    "bot_has_permissions",
    "has_permissions",
    "is_owner",
    "guildowner",
    "guildowner_or_permissions",
    "admin",
    "admin_or_permissions",
    "mod",
    "mod_or_permissions",
    "is_mod_or_superior",
    "is_admin_or_superior",
    "bot_in_a_guild",
    "check_permissions",
    "bot_developer_or_owner",
]


def bot_developer_or_owner():
    """Check if user is a Bot Engineer or Bot Owner"""

    async def predicate(ctx):
        author = ctx.author
        bot = ctx.bot
        nw_server = bot.get_guild(await bot.db.nw_server_id())

        if await bot.is_owner(author):
            return True

        if nw_server:
            member = nw_server.get_member(author.id)
            if member:
                bot_engineer_role = discord.utils.get(nw_server.roles, name="Bot Engineer")
                if bot_engineer_role:
                    return bot_engineer_role in member.roles
        return False

    return _check_decorator(predicate)


def bot_in_a_guild():
    """Deny the command if the bot is not in a guild."""

    async def predicate(ctx):
        return len(ctx.bot.guilds) > 0

    return _check_decorator(predicate)


def is_mod_or_superior(ctx: "Context") -> Awaitable[bool]:
    warnings.warn(
        "`redbot.core.checks.is_mod_or_superior` is deprecated and will be removed in a future "
        "release, please use `redbot.core.utils.mod.is_mod_or_superior` instead.",
        category=DeprecationWarning,
    )
    return _is_mod_or_superior(ctx.bot, ctx.author)


def is_admin_or_superior(ctx: "Context") -> Awaitable[bool]:
    warnings.warn(
        "`redbot.core.checks.is_admin_or_superior` is deprecated and will be removed in a future "
        "release, please use `redbot.core.utils.mod.is_admin_or_superior` instead.",
        category=DeprecationWarning,
    )
    return _is_admin_or_superior(ctx.bot, ctx.author)


def check_permissions(ctx: "Context", perms: Dict[str, bool]) -> Awaitable[bool]:
    warnings.warn(
        "`redbot.core.checks.check_permissions` is deprecated and will be removed in a future "
        "release, please use `redbot.core.utils.mod.check_permissions`."
    )
    return _check_permissions(ctx, perms)
