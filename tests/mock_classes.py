class MockMember:
    def __init__(self, display_name: str | None, display_avatar: str | None) -> None:
        self.display_name = display_name
        self.display_avatar = display_avatar


class MockCommand:
    def __init__(self, name: str | None, help: str | None) -> None:
        self.name = name
        self.help = help
