import discord
import pytest

from bot.embeds import create_help_embed
from bot.constants import WHITE
from tests.mock_classes import MockCommand


def test_normal():
    """Tests normal behavior."""

    command = MockCommand("Test", "Test help")
    embed = create_help_embed(command)

    assert embed.title == command.name
    assert embed.description == command.help
    assert embed.color == discord.Color(WHITE)


def test_no_description():
    """Tests behavior when no description is provided."""

    command = MockCommand("Test", None)
    embed = create_help_embed(command)

    assert embed.title == command.name
    assert embed.description == ""
    assert embed.color == discord.Color(WHITE)


def test_no_name():
    """Tests behavior when no name is provided."""

    command = MockCommand(None, "")

    with pytest.raises(ValueError) as exc:
        create_help_embed(command)

    assert str(exc.value) == "Command does not have a name."
