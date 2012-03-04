#!/usr/bin/env python

import os, stat, time, sys, platform
from subprocess import *

def iff(test_, then_, else_):
    if test_:
        return then_
    else:
        return else_

def mode2strp(mode):
    R_MSK, W_MSK, X_MSK, Z_MSK = 4,   2,   1,   0
    R_STR, W_STR, X_STR, Z_STR = 'r', 'w', 'x', '-'
    r, w, x = mode & R_MSK, mode & W_MSK, mode & X_MSK
    return iff(r, R_STR, Z_STR) + iff(w, W_STR, Z_STR) + iff(x, X_STR, Z_STR) + ' '

def mode2str(mode):
    u, g, o = mode >> 6 & 0x7, mode >> 3 & 0x7, mode & 0x7
    return mode2strp(u) + mode2strp(g) + mode2strp(o)

def size2str(size):
    kb = 1024.0
    mb = 1024 * kb
    gb = 1024 * mb
    if size >= gb:
        return "%.2f GB" % (size/gb)
    if size >= mb:
        return "%.2f MB" % (size/mb)
    if size >= kb:
        return "%.2f KB" % (size/kb)
    else:
        return "%d B" % (size)

def toutf8(name):
    try:
        return name.encode('utf-8')
    except:
        for i in range(0,len(name)):
            if ord(name[i]) >= 128:
                name = name[0:i] + '?' + name[i+1:]
        return name

def bf_exec(cmd):
    pid = os.fork()
    if pid == 0:
        try:
            os.execvp(cmd[0], cmd)
        finally:
            print('Could not exec ', cmd)
            os._exit(1)


class Df_Cmd():
    def __init__(self, cmd):
        if platform.system() == 'Windows':
            if cmd[0][0] == '/':
                cmd[0] = 'c:/cygwin' + cmd[0]
            else:
                cmd[0] = 'c:/cygwin/bin/' + cmd[0]
        self.pob = Popen(cmd, bufsize=1, stdout=PIPE, stderr=STDOUT, universal_newlines=True)

    def readline(self):
        return self.pob.stdout.readline()

    def finish(self):
        self.pob.poll()
        return self.pob.returncode;

def bf_popen(cmd, bufsize=-1):
    p2cread, p2cwrite = os.pipe()
    c2pread, c2pwrite = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.dup2(p2cread, 0)
        os.dup2(c2pwrite, 1)
        os.dup2(c2pwrite, 2)
        try:
            os.execvp(cmd[0], cmd)
        finally:
            print('Could not exec ', cmd)
            os._exit(1)
    os.close(p2cread)
    os.close(p2cwrite)
    os.close(c2pwrite)
    fromchild = os.fdopen(c2pread, 'r', bufsize)
    return fromchild, pid

def seq2str(seq):
    s = ''
    for i in seq:
        s = s + ' ' + str(i)
    return s[1:]

def time2str(t):
    return time.strftime("%y-%m-%d %H:%M:%S", t)

def timenow():
    return time.localtime(time.time())
