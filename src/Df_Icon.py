
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
from utils import *
from PIL import Image, ImageDraw
import hashlib, random
import colorsys

def PILImageToIcon(im):
    data = im.convert('RGBA').tobytes('raw', 'BGRA')
    image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    return (data, QtGui.QIcon(QtGui.QPixmap(image)))

class IconFactory(object):
    def __init__(self, scalepx):
        # self.radius = 0
        #print("iconfactory scalepx", scalepx)
        self.size = (64,64)
        self.allLettersIm = Image.open('icons/Letters.png')
        self.bgimnum = 25
        self.bgimcols = [((255,157,29),(255,109,11)),
                         ((241,33,121),(203,39,128)),
                         ((251,49,34),(197,16,34)),
                         ((238,19,252),(175,1,225)),
                         ((19,117,250),(1,20,145)),
                         ((0,210,0),(0,154,0)),
                         ((126,126,249),(82,97,176))]
        self.bgimcols = []
        for i in range(self.bgimnum):
            h = i/float(self.bgimnum-1) # random.uniform(0,1)
            r1,g1,b1 = colorsys.hsv_to_rgb(h,.95,0.8)
            h += .07
            if h > 1:
                h -= 1
            r2,g2,b2 = colorsys.hsv_to_rgb(h,1,0.5)
            r1 = int(255*r1)
            g1 = int(255*g1)
            b1 = int(255*b1)
            r2 = int(255*r2)
            g2 = int(255*g2)
            b2 = int(255*b2)
            self.bgimcols.append(((r1,g1,b1),(r2,g2,b2)))

        # 720,660 coordinates to / in letters.png
        x = 752
        y = 698
        hs = 42 # hs = half of the total crop size
        letterSize = int((76*self.size[0])/100)
        im = self.allLettersIm.crop((x-hs,y-hs,x+hs,y+hs))
        im = im.resize((letterSize, letterSize), Image.BICUBIC)
        bgim = self.drawRectangle(self.size, (255,241,19), (255,204,1))
        offs = int((self.size[0]-letterSize)/2)
        bgim.paste(im, (offs,offs), im)
        self.folderImageData, self.folderIcon = PILImageToIcon(bgim)

        arrow = Image.open('icons/arrow.png')
        scale = 0.55
        arrow = arrow.resize((int(scale*128*.8),int(scale*68)), Image.BICUBIC)
        bgim.paste(arrow, (10,33), arrow)
        self.folderLinkImageData, self.folderLinkIcon = PILImageToIcon(bgim)
        self.arrow = arrow

        im = self.drawRectangle(self.size, self.bgimcols[13][0], self.bgimcols[13][1])
        #self.bgimnum -= 1
        self.fileImageData, self.fileIcon = PILImageToIcon(im)
        im.paste(arrow, (10,33), arrow)
        self.fileImageDataLink, self.fileIconLink = PILImageToIcon(im)
        self.icons = {}
        self.iconsLink = {}

    def getFolderIcon(self, softlink=False):
        if softlink:
            return self.folderLinkIcon
        return self.folderIcon
    
    def getFileIcon(self, path, softlink=False):
        ext = fsPathExt(path)
        if ext == '':
            if softlink:
                return self.fileIconLink
            else:
                return self.fileIcon
        if softlink:
            if ext in self.iconsLink:
                (_, icon) = self.iconsLink[ext]
                return icon
        else:
            if ext in self.icons:
                (_, icon) = self.icons[ext]
                return icon
        e = ext[0]
        c1 = 'abcdefghijklmn'
        c2 = 'opqrstuvwxyz'
        if not e in c1+c2:
            if len(ext) >= 2:
                e = ext[1]
            else:
                return self.fileIcon
        # It's ok if e is not one of the letters now, it will just be a blank foreground
        cols = ((212, 151, c1),
                (532, 226, c2))
        hs = 42 # hs = half of the total crop size
        deltay = 92.6
        letterSize = int((76*self.size[0])/100)
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
        im = im.resize((letterSize, letterSize), Image.BICUBIC)
        h = hashlib.md5(ext.encode()).hexdigest()
        h = int(h[28:32], 16)
        coff = h/65536.0
        idx = int(coff*(self.bgimnum-0.0001))
        bgim = self.drawRectangle(self.size, self.bgimcols[idx][0], self.bgimcols[idx][1])
        offs = int((self.size[0]-letterSize)/2)
        bgim.paste(im, (offs,offs), im)
        (data, icon) = PILImageToIcon(bgim)
        self.icons[ext] = (data, icon)
        bgim.paste(self.arrow, (10,33), self.arrow)
        (data, icon) = PILImageToIcon(bgim)
        self.iconsLink[ext] = (data, icon)
        return icon

    def channel(self, i, c, size, startFill, stopFill):
        return startFill[c] + int((i * 1.0 / size) * (stopFill[c] - startFill[c]))
    
    def color(self, i, size, startFill, stopFill):
        return tuple([self.channel(i, c, size, startFill, stopFill) for c in range(3)])

    def drawRectangle(self, size, startFill, stopFill):
        width, height = size
        rectangle = Image.new('RGBA', size)
        gradient = [ self.color(i, width, startFill, stopFill) for i in range(height) ]
    
        modGrad = []
        for i in range(height):
            modGrad += [gradient[i]] * width
        rectangle.putdata(modGrad)
    
        return rectangle


