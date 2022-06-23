from datetime import datetime

import discord
from discord.ext import commands

from .constants import WHITE


def create_poll_embed(text: str, author: discord.Member) -> discord.Embed:
    """Creates an embed out of poll text and author."""

    if not text or text.isspace():
        raise ValueError("Invalid text.")

    if not author.display_name or not author.display_avatar:
        raise ValueError(
            "Author does not have properties display_name and/or display_avatar."
        )

    embed = discord.Embed(
        title=text,
        color=WHITE,
        timestamp=datetime.now(),
    )

    embed.set_author(name=author.display_name, icon_url=author.display_avatar)

    return embed


def create_help_embed(command: commands.Command) -> discord.Embed:
    """Creates an embed out of a command."""

    if not command.name or command.name.isspace():
        raise ValueError("Command does not have a name.")

    embed = discord.Embed(
        title=command.name,
        color=WHITE,
        description=command.help or "",
    )

    return embed
