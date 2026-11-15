import os
import subprocess

DETACHED_PROCESS = 0x00000008


class Shell:
    """The process and filesystem calls the plugin makes on Windows."""

    def output(self, args: list) -> bytes:
        process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        return stdout

    def spawn(self, args: list) -> None:
        subprocess.Popen(
            args,
            shell=False,
            stdin=None,
            stdout=None,
            stderr=None,
            close_fds=True,
            creationflags=DETACHED_PROCESS,
        )

    def exists(self, path: str) -> bool:
        return os.path.exists(path)
