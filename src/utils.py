#!/usr/bin/env python

import os, stat, time, sys, platform
from subprocess import *
from PIL import Image
from PIL.ExifTags import TAGS
from PySide.QtCore import *
from PySide import QtGui


def JpegToPixmap(fn):
    im = Image.open(fn)
    exif = Exif(im)
    if 'Orientation' in exif:
        if exif['Orientation'] == 6:
            im = im.rotate(-90)
        elif exif['Orientation'] == 3:
            im = im.rotate(180)
        elif exif['Orientation'] == 8:
            im = im.rotate(90)
    data = im.convert('RGBA').tostring('raw', 'BGRA')
    image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    return (data, QtGui.QPixmap(image))

def Exif(i):
    ret = {}
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret        

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


def seq2str(seq):
    s = ''
    for i in seq:
        s = s + ' ' + str(i)
    return s[1:]

def time2str(t):
    return time.strftime("%y-%m-%d %H:%M:%S", t)

def timenow():
    return time.localtime(time.time())

def fsPathExt(path):
        p = path.lower()
        p = p.split('.')
        if len(p) <= 1:
            return ''
        if len(p) >= 3 and p[-2] == 'tar':
            if p[-1] == 'gz':
                return 'tar.gz'
            if p[-1] == 'bz2':
                return 'tar.bz2'
        ext = p[-1]
        if len(ext) > 4:
            ext = ''
        return ext

def genericPathToWindows(p):
    p = '\\'.join(p.split('/'))
    return p

def windowsPathToGeneric(p):
    p = '/'.join(p.split('\\'))
    return p
