#!/usr/bin/env python

import os, stat, time, sys, platform
from subprocess import *
from PIL import Image
from PIL.ExifTags import TAGS
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
import locale, datetime
import exifread
import tempfile, Df, traceback

def ImageToPreview(fn):
    try:
        im = Image.open(fn)
    except:
        return None
    exif = {}
    try:
        info = im._getexif()
    except:
        info = None
    if info:
        for tag, value in list(info.items()):
            decoded = TAGS.get(tag, tag)
            exif[decoded] = value
    date = ''
    if 'DateTimeOriginal' in exif:
        # Date example: 2011:02:26 16:29:49
        try:
            date2 = exif['DateTimeOriginal']
            t = time.strptime(date2,"%Y:%m:%d %H:%M:%S")
            date = 'Photo taken at: '+ time2str(t) + '  '
        except:
            pass
    if 'Orientation' in exif:
        if exif['Orientation'] == 6:
            im = im.rotate(-90,expand=1)
        elif exif['Orientation'] == 3:
            im = im.rotate(180,expand=1)
        elif exif['Orientation'] == 8:
            im = im.rotate(90,expand=1)
    data = im.convert('RGBA').tobytes('raw', 'BGRA')
    image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    w,h = im.size
    size = str(w) + 'x' + str(h)
    return ((data, QtGui.QPixmap(image)), date + 'Size: ' + size + '  (%.1f Mpixels)' % ((w*h)/1.0e6))

def JpegThumbToIcon(fn):
    # print(fn)
    file=open(fn, 'rb')
    exif = exifread.process_file(file)
    file.close()
    date = ''
    dateSecs = 0
    thumb = None
    # print(exif)
    if 'EXIF DateTimeOriginal' in exif:
        # Date example: 2011:02:26 16:29:49
        date = str(exif['EXIF DateTimeOriginal'])
        try:
            t = time.strptime(date,"%Y:%m:%d %H:%M:%S")
            dateSecs = time.mktime(t)
            date = time2str(t)
        except:
            date = ''
    if 'JPEGThumbnail' in exif:
        f = Df.d.tempfile
        f.truncate(0)
        f.seek(0)
        f.write(exif['JPEGThumbnail'])
        f.seek(0)
        im = Image.open(f)
        if 'Image Orientation' in exif:
            o = str(exif['Image Orientation'])
            # print(o)
            if o == '6' or o == "Rotated 90 CW":
                im = im.rotate(-90,expand=1)
            elif o == '3':
                im = im.rotate(180,expand=1)
            elif o == '8' or o == "Rotated 90 CCW":
                im = im.rotate(90,expand=1)
        w,h = im.size
        if w > h:
            s = w
            b = (0,int((w-h)/2))
        else:
            s = h
            b = (int((h-w)/2),0)
        c = 128
        im2 = Image.new('RGBA', (s,s), (c,c,c,255))
        #print(im.size,b)
        im2.paste(im, b)
        im=im2
        data = im.convert('RGBA').tobytes('raw', 'BGRA')
        image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
        thumb = (data, QtGui.QIcon(QtGui.QPixmap(image)))
    return (thumb, date, dateSecs)

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


if platform.system() == 'Windows':
    def mode2str(stats):
        mode, attrib = stats
        s = ''
        if win32con.FILE_ATTRIBUTE_HIDDEN & attrib:
            s += 'H'
        if win32con.FILE_ATTRIBUTE_SYSTEM & attrib:
            s += 'S'
        if win32con.FILE_ATTRIBUTE_READONLY & attrib:
            s += 'R'
        if win32con.FILE_ATTRIBUTE_ARCHIVE & attrib:
            s += 'A'
        return s
else:
    def mode2str(stats):
        st, attrib = stats
        mode = int(st.st_mode)
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
        return "%.2f kB" % (size/kb)
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
    return time.strftime(Df.d.config.formatTimeDate, t)

#if platform.system() == 'Windows':
#    def time2str(t):
#        #return time.strftime(locale.nl_langinfo(locale.D_T_FMT), t)
#        de = win32api.GetDateFormat(0, 0, t)
#        tm = win32api.GetTimeFormat(0, 0, t)
#        return de+' '+tm
#else:
#    def time2str(t):
#        return time.strftime(locale.nl_langinfo(locale.D_T_FMT), t)
#        #return time.strftime("%y-%m-%d %H:%M:%S", t)

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



def crash():
    print(("Crash dumping now", Df.d.logfile))
    traceback.print_exc()
    try:
        f=open(Df.d.logfile,"w")
        traceback.print_exc(file=f)
    except:
        pass
    os._exit(1)

