class MockMember:
    """Mock class for :code:`hikari.Member`."""

    def __init__(self, display_name: str | None, display_avatar_url: str | None) -> None:
        self.display_name = display_name
        self.display_avatar_url = display_avatar_url


class MockPrefixCommand:
    """Mock class for :code:`lightbulb.PrefixCommand`."""

    def __init__(self, name: str | None, help: str | None) -> None:
        self.name = name
        self._help = help

    def get_help(self, ctx) -> str:
        return self._help
