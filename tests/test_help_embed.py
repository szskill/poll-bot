import pytest

from bot.embeds import create_help_embed
from bot.constants import WHITE
from tests.mock_classes import MockPrefixCommand


def test_normal():
    """Tests normal behavior."""

    command = MockPrefixCommand("Test", "Test help")
    embed = create_help_embed(command)

    assert embed.title == command.name
    assert embed.description == command.get_help(None)
    assert embed.color == WHITE


def test_no_description():
    """Tests behavior when no description is provided."""

    command = MockPrefixCommand("Test", None)
    embed = create_help_embed(command)

    assert embed.title == command.name
    assert not embed.description
    assert embed.color == WHITE


def test_no_name():
    """Tests behavior when no name is provided."""

    command = MockPrefixCommand(None, "")

    with pytest.raises(ValueError) as exc:
        create_help_embed(command)

    assert str(exc.value) == "Command does not have a name."
