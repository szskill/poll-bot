import discord
import pytest

from bot.embeds import create_poll_embed
from bot.constants import WHITE
from .mock_classes import MockMember


def test_normal():
    """Tests normal behavior."""

    text = "Test"
    mock_author = MockMember("John123", "John123Avatar")

    embed = create_poll_embed(text, mock_author)

    assert embed.title == text
    assert embed.color == discord.Color(WHITE)

    assert embed.author.name == mock_author.display_name
    assert embed.author.icon_url == mock_author.display_avatar


def test_no_text():
    """Tests when whitespace is provided as the text argument."""

    with pytest.raises(ValueError) as exc:
        create_poll_embed(" ", MockMember("John123", "John123Avatar"))

    assert str(exc.value) == "Invalid text."


def test_invalid_author():
    """Tests when an invalid author (missing display_name and display_avatar)
    is provided.
    """

    with pytest.raises(ValueError) as exc:
        create_poll_embed("Test", MockMember(None, None))

    assert (
        str(exc.value)
        == "Author does not have properties display_name and/or display_avatar."
    )
