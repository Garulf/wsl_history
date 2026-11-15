import pytest

import wsl_history
from wsl_history import WslHistory

HISTORY = b"ls -la\ncd projects\ngit status\nmake test\n"
APPDATA = "C:\\Users\\user\\AppData\\Roaming"
WINDOWS_TERMINAL = "C:\\Users\\user\\AppData\\Local\\Microsoft\\WindowsApps\\wt.exe"


class FakeShell:
    def __init__(self, history=HISTORY, files=()):
        self.history = history
        self.files = set(files)
        self.calls = []
        self.spawned = []

    def output(self, args):
        self.calls.append(args)
        return self.history

    def spawn(self, args):
        self.spawned.append(args)

    def exists(self, path):
        return path in self.files


@pytest.fixture
def shell():
    return FakeShell()


@pytest.fixture
def wsl(shell, monkeypatch):
    history = WslHistory(shell, {"APPDATA": APPDATA})
    monkeypatch.setattr(wsl_history, "wsl", history)
    return history
