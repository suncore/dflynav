

from PySide.QtCore import *
from PySide import QtGui
from utils import *
from PIL import Image
#import numpy as np
#import colorsys
import hashlib

#rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
#hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)
#
#def shift_hue(arr, hout):
#    r, g, b, a = np.rollaxis(arr, axis=-1)
#    h, s, v = rgb_to_hsv(r, g, b)
#    #h = h + hout
#    r, g, b = hsv_to_rgb(h, s, v)
#    #g = g * 0.99
#    #r = r * 0.99
#    arr = np.dstack((r, g, b, a))
#    return arr
#
#def colorize(image, hue):
#    """
#    Colorize PIL image `original` with the given
#    `hue` (hue within 0-360); returns another PIL image.
#    """
#    img = image.convert('RGBA')
#    arr = np.array(np.asarray(img).astype('float'))
#    new_img = Image.fromarray(shift_hue(arr, hue/360.).astype('uint8'), 'RGBA')
#
#    return new_img

def ImageToIcon(im):
    data = im.convert('RGBA').tostring('raw', 'BGRA')
    image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    return (data, QtGui.QIcon(QtGui.QPixmap(image)))

class IconFactory(object):
    def __init__(self):
        #import os
        #print os.getcwd()
        #self.bgim = Image.open('/a/proj/dragonfly/ws3/src/icons/Background1.png')
        self.bgim = Image.open('src/icons/Background1.png')
        self.allLettersIm = Image.open('src/icons/Letters.png')
        im = Image.open('src/icons/Folder.png')
        self.folderImageData, self.folderIcon = ImageToIcon(im)
        im = Image.open('src/icons/File.png')
        #im = colorize(im,0)
        self.fileImageData, self.fileIcon = ImageToIcon(im)
        self.bgims = []
        self.bgimnum = 7
        self.icons = {}
        for i in range(1,self.bgimnum+1):
            self.bgims.append(Image.open('src/icons/b' + str(i) + '.png'))

    def getFolderIcon(self):
        return self.folderIcon
    
    def getFileIcon(self, path):
        ext = fsPathExt(path)
        if ext == '':
            return self.fileIcon
        e = ext[0]
        if ext in self.icons:
            (data, icon) = self.icons[ext]
            return icon
        cols = ((212, 151, 'abcdefghijklmn'),
                (532, 226, 'opqrstuvwxyz'))
        hs = 42 # hs = half of the total crop size
        deltay = 92.6
        letterSize = (76*self.bgim.size[0])/100
        if e <= 'n':
            col = cols[0]
            ix = ord(e)-ord('a')
        else:
            col = cols[1]
            ix = ord(e)-ord('o')
        x, y, chars = col
        y = ix*deltay+y
        yi = int(y)
        im = self.allLettersIm.crop((x-hs,yi-hs,x+hs,yi+hs))
        im = im.resize((letterSize, letterSize))
        h = hashlib.md5(ext).hexdigest()
        h = int(h[28:32], 16)
        coff = h/65536.0
        #bgim = colorize(self.bgim, coff*360.0)
        bgim = self.bgims[int(coff*(self.bgimnum-0.0001))].copy()
        #bgim = colorize(bgim, 0)
        offs = (self.bgim.size[0]-letterSize)/2
        bgim.paste(im, (offs,offs), im)
        #im = Image.composite(im, bgim, im)
        (data, icon) = ImageToIcon(bgim)
        self.icons[ext] = (data, icon)
        return icon

