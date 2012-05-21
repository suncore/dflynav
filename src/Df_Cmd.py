
import os, stat, time, sys, platform


class Cmd(object):
    def __init__(self, cmd, dst):
        if platform.system() == 'Windows':
            if cmd[0][0] == '/':
                cmd2 = 'c:/cygwin' + cmd[0]
            else:
                cmd2 = 'c:/cygwin/bin/' + cmd[0]
            cmd = (cmd2,) + cmd[1:]
        self.pob = Popen(cmd, bufsize=1, stdout=PIPE, stderr=STDOUT, universal_newlines=True, cwd=dst)

    def readline(self):
        return self.pob.stdout.readline()

    def finish(self):
        self.pob.wait()
        return self.pob.returncode
