#!/usr/bin/env python

import os, time, io
from subprocess import *
from PIL import Image
from PIL.ExifTags import TAGS
from PyQt6.QtCore import *
from PyQt6 import QtGui, QtWidgets
import exifread
import Df, traceback


def TextToPreview(fn):
    try:
        file=open(fn, 'r')
        data = file.read(1024*10)
        file.close()
        return 'text', data
    except:
        return 'text', "No preview available"

def ImageToPreview(fn):
    #print("ImageToPreview",fn)
    try:
        im = Image.open(fn)
    except:
        im = None
    if not im:
        return None
    file=open(fn, 'rb')
    exif = exifread.process_file(file)
    file.close()
    date = ''
    #print("ImageToPreview2",fn)
    if 'EXIF DateTimeOriginal' in exif:
        # Date example: 2011:02:26 16:29:49
        date = str(exif['EXIF DateTimeOriginal'])
        try:
            t = time.strptime(date,"%Y:%m:%d %H:%M:%S")
            dateSecs = time.mktime(t)
            date = time2str(t)
        except:
            date = ''
    if 'Image Orientation' in exif:
        o = str(exif['Image Orientation'])
        if o == '6' or o == "Rotated 90 CW":
            im = im.rotate(-90,expand=1)
        elif o == '3':
            im = im.rotate(180,expand=1)
        elif o == '8' or o == "Rotated 90 CCW":
            im = im.rotate(90,expand=1)
    try:
        data = im.convert('RGBA').tobytes('raw', 'BGRA')
    except:
        return None
    image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format.Format_ARGB32)
    w,h = im.size
    size = str(w) + 'x' + str(h)
    return 'image', (data, QtGui.QPixmap(image), date + '  Size: ' + size + '  (%.1f Mpixels)' % ((w*h)/1.0e6))

def ImageToIcon(fn):
    file=open(fn, 'rb')
    exif = exifread.process_file(file)
    file.close()
    date = ''
    dateSecs = 0
    thumb = None

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
        c = 0
        im2 = Image.new('RGBA', (s,s), (c,c,c,1))
        im2.paste(im, b)
        im=im2
        data = im.convert('RGBA').tobytes('raw', 'BGRA')
        image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format.Format_ARGB32)
        thumb = (data, QtGui.QIcon(QtGui.QPixmap(image)))
    else:
        try:
            im = Image.open(fn)
        except:
            im = None
        if im:
            if True:
                im.thumbnail((128,128), Image.LANCZOS)
                w,h = im.size
                if w > h:
                    s = w
                    b = (0,int((w-h)/2))
                else:
                    s = h
                    b = (int((h-w)/2),0)
                c = 0
                im2 = Image.new('RGBA', (s,s), (c,c,c,1))
                im2.paste(im, b)
                im=im2
                data = im.convert('RGBA').tobytes('raw', 'BGRA')
            #except:
            #    return (None, date, dateSecs)
            image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format.Format_ARGB32)
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
        if len(ext) > 8:
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

