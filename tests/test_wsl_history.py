import asyncio

import pytest
from conftest import APPDATA, WINDOWS_TERMINAL, FakeShell

import wsl_history
from wsl_history import BASH_EXE, CMD, WslHistory


def run_method(method, *params):
    return asyncio.run(wsl_history.plugin._event_handler.trigger_event(method, *params))


def titles(response):
    return [result["Title"] for result in response["Result"]]


def test_history_is_read_with_bash(wsl, shell):
    wsl.history()
    assert shell.calls == [[BASH_EXE, "-c", "cat ~/.bash_history"]]


def test_query_filters_history_by_substring(wsl):
    response = run_method("query", "git")
    assert titles(response) == ["git status"]


def test_result_runs_the_command(wsl):
    (result,) = run_method("query", "make")["Result"]
    assert result["SubTitle"] == "3"
    assert result["IcoPath"] == wsl_history.ICON
    assert result["JsonRPCAction"]["Method"] == "run_cmd"
    assert result["JsonRPCAction"]["Parameters"] == ["make test"]


def test_run_uses_windows_terminal_when_installed(shell):
    shell.files.add(WINDOWS_TERMINAL)
    WslHistory(shell, {"APPDATA": APPDATA}).run("git status")
    assert shell.spawned == [[CMD, "/c", 'wt.exe bash -i -l -c "git status\\; bash -i -l"']]


def test_run_falls_back_to_cmd(shell):
    WslHistory(shell, {"APPDATA": APPDATA}).run("git status")
    assert shell.spawned == [[CMD, "/K", BASH_EXE, "-c", "git status;exec $SHELL"]]


@pytest.mark.parametrize("environ", [{}, {"APPDATA": ""}])
def test_run_without_appdata_falls_back_to_cmd(environ):
    shell = FakeShell(files=[WINDOWS_TERMINAL])
    WslHistory(shell, environ).run("ls")
    assert shell.spawned == [[CMD, "/K", BASH_EXE, "-c", "ls;exec $SHELL"]]


def test_run_cmd_action(wsl, shell):
    run_method("run_cmd", "ls -la")
    assert shell.spawned == [[CMD, "/K", BASH_EXE, "-c", "ls -la;exec $SHELL"]]
