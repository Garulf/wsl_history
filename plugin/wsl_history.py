from subprocess import call, Popen, PIPE, DETACHED_PROCESS
import os


from flox import Flox

BASH_EXE = r"C:\WINDOWS\system32\bash.exe"
PSHELL = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
APPDATA = os.environ.get("APPDATA").replace("Roaming", "Local")
WT = os.path.join(APPDATA, "Microsoft\\WindowsApps\\wt.exe")
CMD = "C:\\Windows\\System32\\cmd.exe"
DETACHED_PROCESS = 0x00000008

class WslHistory(Flox):

    def run(self, cmd):
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

        out, err = process.communicate()
        errcode = process.returncode
        process.wait()
        return out, err

    def history(self):
        cmd = [BASH_EXE, "-c", "cat ~/.bash_history"]
        stdout, stderr = self.run(cmd)
        return str(stdout).split("\\n")

    def query(self, query):
        self.logger.debug(WT)
        history = self.history()
        for idx, item in enumerate(history):
            if query in item:
                self.add_item(
                    title=str(item),
                    subtitle=str(idx),
                    method='run_cmd',
                    parameters=[item]
                )

    def context(self, data):
        pass

    def run_cmd(self, cmd):
        
        if os.path.exists(WT):
            Popen([CMD, "/c", f"wt.exe bash -i -l -c \"{cmd}\; bash -i -l\""], shell=False, stdin=None, stdout=None, stderr=None,
                close_fds=True, creationflags=DETACHED_PROCESS)
        else:
            cmd = f"{cmd};exec $SHELL"
            Popen([CMD, "/K", BASH_EXE, "-c", cmd], shell=False, stdin=None, stdout=None, stderr=None,
                close_fds=True, creationflags=DETACHED_PROCESS)

if __name__ == "__main__":
    WslHistory()