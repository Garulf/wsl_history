import ntpath
import os
from pathlib import Path
from typing import List, Mapping, Optional

from pyflowlauncher import Plugin, Result

from shell import Shell

BASH_EXE = r"C:\WINDOWS\system32\bash.exe"
CMD = "C:\\Windows\\System32\\cmd.exe"
ICON = str(Path(__file__).resolve().parent.parent / "icon.png")


class WslHistory:
    def __init__(self, shell: Shell, environ: Mapping[str, str]) -> None:
        self._shell = shell
        self._environ = environ

    def windows_terminal(self) -> Optional[str]:
        appdata = self._environ.get("APPDATA")
        if not appdata:
            return None
        return ntpath.join(appdata.replace("Roaming", "Local"), "Microsoft\\WindowsApps\\wt.exe")

    def history(self) -> List[str]:
        stdout = self._shell.output([BASH_EXE, "-c", "cat ~/.bash_history"])
        return str(stdout).split("\\n")

    def run(self, command: str) -> None:
        terminal = self.windows_terminal()
        if terminal and self._shell.exists(terminal):
            self._shell.spawn([CMD, "/c", f'wt.exe bash -i -l -c "{command}\\; bash -i -l"'])
        else:
            self._shell.spawn([CMD, "/K", BASH_EXE, "-c", f"{command};exec $SHELL"])


plugin = Plugin()
wsl = WslHistory(Shell(), os.environ)


@plugin.on_method
def run_cmd(command: str) -> None:
    wsl.run(command)


@plugin.on_method
def query(query: str):
    for index, command in enumerate(wsl.history()):
        if query in command:
            yield Result(title=command, subtitle=str(index), icon=ICON).add_action(run_cmd, parameters=[command])
