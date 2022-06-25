from datetime import datetime

import hikari
import lightbulb

from .constants import WHITE


def create_help_embed(command: lightbulb.PrefixCommand) -> hikari.Embed:
    """Creates a help embed for the given command."""

    return hikari.Embed(
        title=command.name,
        description=command.get_help(None),
        timestamp=datetime.now().astimezone(),
        color=WHITE,
    )


def create_poll_embed(text: str, author: hikari.Member) -> hikari.Embed:
    """Creates a poll embed based on the text and author."""

    return hikari.Embed(
        title=text,
        description="React with the appropriate emoji to vote!",
        timestamp=datetime.now().astimezone(),
        color=WHITE,
    ).set_author(
        name=author.display_name,
        icon=author.display_avatar_url,
    )
