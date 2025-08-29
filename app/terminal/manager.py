import os, pty, tty, select, fcntl, termios, signal, threading, subprocess

class PTYSession:
    def __init__(self, shell="/bin/bash"):
        self.shell = shell
        self.pid = None
        self.fd = None
        self.alive = False
        self.lock = threading.Lock()

    def start(self):
        pid, fd = pty.fork()
        if pid == 0:
            # Child: interactive shell
            os.execvp(self.shell, [self.shell, "-l"])
        else:
            self.pid = pid
            self.fd = fd
            self.alive = True
            # non-blocking
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def read(self, timeout=0.05) -> bytes:
        if not self.alive:
            return b""
        r, _, _ = select.select([self.fd], [], [], timeout)
        if r:
            try:
                return os.read(self.fd, 8192)
            except OSError:
                self.alive = False
        return b""

    def write(self, data: bytes):
        if not self.alive:
            return
        with self.lock:
            os.write(self.fd, data)

    def signal(self, sig=signal.SIGINT):
        if self.pid and self.alive:
            try:
                os.kill(self.pid, sig)
            except ProcessLookupError:
                self.alive = False

    def close(self):
        if self.alive:
            try:
                os.kill(self.pid, signal.SIGHUP)
            except ProcessLookupError:
                pass
        self.alive = False

# One-shot exec
def run_cmd(cmd: str, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
