

from PySide.QtCore import *
from PySide import QtGui
from utils import *
from PIL import Image, ImageDraw
import hashlib, random

if platform.system() == 'Windows':
    import win32ui
    import win32gui
    import win32con
    import win32api
    import cStringIO
    import Image
            



def ImageToIcon(im):
    data = im.convert('RGBA').tostring('raw', 'BGRA')
    image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    return (data, QtGui.QIcon(QtGui.QPixmap(image)))

class IconFactory(object):
    def __init__(self):
        self.radius = 0
        self.size = (70,70)
        #import os
        #print os.getcwd()
        #self.bgim = Image.open('/a/proj/dragonfly/ws3/src/icons/Background1.png')
        self.bgim = Image.open('src/icons/Background1.png')
        self.allLettersIm = Image.open('src/icons/Letters.png')
        #im = Image.open('src/icons/Folder.png')
        im = round_rectangle(self.size, self.radius, (255,241,19), (255,204,1), True)

        self.folderImageData, self.folderIcon = ImageToIcon(im)
        #im = Image.open('src/icons/File.png')
        im = round_rectangle(self.size, self.radius, (70,180,255), (25,161,255), True)
        #im = colorize(im,0)
        self.fileImageData, self.fileIcon = ImageToIcon(im)
        self.bgims = []
        self.bgimnum = 7
        self.bgimcols = [((255,157,29),(255,109,11)),
                         ((241,33,121),(203,39,128)),
                         ((251,49,34),(197,16,34)),
                         ((238,19,252),(175,1,225)),
                         ((19,117,250),(1,20,145)),
                         ((0,210,0),(0,154,0)),
                         ((126,126,249),(82,97,176))]
        l1 = 0.5
        u1 = 1.0
        l2 = 0.1
        u2 = 0.3
        for i in range(self.bgimnum):
            r1 = int(255*random.uniform(l1,u1))
            g1 = int(255*random.uniform(l1,u1))
            b1 = int(255*random.uniform(l1,u1))
            r2 = int(255*random.uniform(l2,u2))
            g2 = int(255*random.uniform(l2,u2))
            b2 = int(255*random.uniform(l2,u2))
            self.bgimcols[i] = ((r1,g1,b1),(r2,g2,b2))
        self.icons = {}
        for i in range(1,self.bgimnum+1):
            self.bgims.append(Image.open('src/icons/b' + str(i) + '.png'))
        if platform.system() == 'Windows':
            self.tempDirectory = os.getenv("temp")
            self.ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            self.ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

    def getFolderIcon(self):
        return self.folderIcon
    
    def getFileIcon(self, path):
        if platform.system() == 'Windows' and Df.d.config.showIcons:
            try:
                large, small = win32gui.ExtractIconEx(path,0)
            except:
                large = small = []
            if len(small) > 0 and len(large) > 0:
                win32gui.DestroyIcon(small[0])
                hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap(hdc, self.ico_x, self.ico_y)
                hdc = hdc.CreateCompatibleDC()
                hdc.SelectObject( hbmp )
                hdc.FillSolidRect( (0,0, self.ico_x, self.ico_y), 0xffffff ) #TODO should use current background
                hdc.DrawIcon( (0,0), large[0] )
                #hdc.DeleteDC()
                win32gui.DestroyIcon(large[0])
                hbmp.SaveBitmapFile( hdc, self.tempDirectory + "\dfIcontemp.bmp")
                im = Image.open(self.tempDirectory + "\dfIcontemp.bmp")
                (data, icon) = ImageToIcon(im)
                #self.icons[path] = (data, icon)
                return icon
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
        idx = int(coff*(self.bgimnum-0.0001))
        #bgim = self.bgims[int(coff*(self.bgimnum-0.0001))].copy()
        #bgim = colorize(bgim, 0)

        bgim = round_rectangle(self.size, self.radius, self.bgimcols[idx][0], self.bgimcols[idx][1], True)
        
        offs = (self.bgim.size[0]-letterSize)/2
        bgim.paste(im, (offs,offs), im)
        #im = Image.composite(im, bgim, im)

        (data, icon) = ImageToIcon(bgim)
        self.icons[ext] = (data, icon)
        return icon



def channel(i, c, size, startFill, stopFill):
    """calculate the value of a single color channel for a single pixel"""
    return startFill[c] + int((i * 1.0 / size) * (stopFill[c] - startFill[c]))

def color(i, size, startFill, stopFill):
    """calculate the RGB value of a single pixel"""
    return tuple([channel(i, c, size, startFill, stopFill) for c in range(3)])

def round_corner(radius):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill="blue")
    return corner

def apply_grad_to_corner(corner, gradient, backwards = False, topBottom = False):
    width, height = corner.size
    widthIter = range(width)

    if backwards:
        widthIter.reverse()

    for i in xrange(height):
        gradPos = 0
    for j in widthIter:
        if topBottom:
            pos = (i,j)
        else:
            pos = (j,i)
        pix = corner.getpixel(pos)
        gradPos+=1
        if pix[3] != 0:
            corner.putpixel(pos,gradient[gradPos])

    return corner

def round_rectangle(size, radius, startFill, stopFill, runTopBottom = False):
    """Draw a rounded rectangle"""
    width, height = size
    rectangle = Image.new('RGBA', size)

    if runTopBottom:
      si = height
    else:
      si = width

    gradient = [ color(i, width, startFill, stopFill) for i in xrange(si) ]

    if runTopBottom:
        modGrad = []
        for i in xrange(height):
           modGrad += [gradient[i]] * width
        rectangle.putdata(modGrad)
    else:
        rectangle.putdata(gradient*height)

    origCorner = round_corner(radius)

    # upper left
    corner = origCorner
    apply_grad_to_corner(corner,gradient,False,runTopBottom)
    rectangle.paste(corner, (0, 0))

    # lower left
    if runTopBottom: 
        gradient.reverse()
        backwards = True
    else:
        backwards = False


    corner = origCorner.rotate(90)
    apply_grad_to_corner(corner,gradient,backwards,runTopBottom)
    rectangle.paste(corner, (0, height - radius))

    # lower right
    if not runTopBottom: 
        gradient.reverse()

    corner = origCorner.rotate(180)
    apply_grad_to_corner(corner,gradient,True,runTopBottom)
    rectangle.paste(corner, (width - radius, height - radius))

    # upper right
    if runTopBottom: 
        gradient.reverse()
        backwards = False
    else:
        backwards = True

    corner = origCorner.rotate(270)
    apply_grad_to_corner(corner,gradient,backwards,runTopBottom)
    rectangle.paste(corner, (width - radius, 0))

    return rectangle

#img = round_rectangle((200, 200), 70, (255,0,0), (0,255,0), True)
#img.save("test.png", 'PNG')






#import numpy as np
#import colorsys
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

