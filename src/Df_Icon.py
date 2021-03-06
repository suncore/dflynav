

from PyQt5.QtCore import *
from PyQt5 import QtGui, QtWidgets
from utils import *
from PIL import Image, ImageDraw
import hashlib, random
import colorsys

if platform.system() == 'Windows':
    import win32ui
    import win32gui
    import win32con
    import win32api
    import io
    import Image
    from winreg import  *

def ImageToIcon(im):
    data = im.convert('RGBA').tobytes('raw', 'BGRA')
    image = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    return (data, QtGui.QIcon(QtGui.QPixmap(image)))

class IconFactory(object):
    def __init__(self):
        self.radius = 0
        self.size = (64,64)
        #import os
        #print os.getcwd()
        #self.bgim = Image.open('/a/proj/dragonfly/ws3/src/icons/Background1.png')
        #self.bgim = Image.open('src/icons/Background1.png')
        self.allLettersIm = Image.open('icons/Letters.png')
        #im = colorize(im,0)
        #self.bgims = []
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
            h += .05
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

        #im = Image.open('src/icons/Folder.png')
        im = self.drawRectangle(self.size, (255,241,19), (255,204,1))

        self.folderImageData, self.folderIcon = ImageToIcon(im)
        #im = Image.open('src/icons/File.png')
        #im = drawRectangle(self.size, self.radius, (70,180,255), (25,161,255), True)
        im = self.drawRectangle(self.size, self.bgimcols[-1][0], self.bgimcols[-1][1])
        self.bgimnum -= 1
        self.fileImageData, self.fileIcon = ImageToIcon(im)

        self.icons = {}
#        for i in range(1,self.bgimnum+1):
#            self.bgims.append(Image.open('src/icons/b' + str(i) + '.png'))
        if platform.system() == 'Windows':
            self.tempDirectory = os.getenv("temp")
            self.ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            self.ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
            self.aReg = ConnectRegistry(None, HKEY_CLASSES_ROOT)

    def WindowsIconFromFilename(self, path, index=0):
        try:
            large, small = win32gui.ExtractIconEx(path,index)
        except:
            large = small = []
        if len(small) > 0 and len(large) > 0:
            win32gui.DestroyIcon(large[0])
            hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, self.ico_x, self.ico_y)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject( hbmp )
            hdc.FillSolidRect( (0,0, self.ico_x, self.ico_y), 0xffffff ) #TODO should use current background
            hdc.DrawIcon( (0,0), small[0] )
            #hdc.DeleteDC()
            win32gui.DestroyIcon(small[0])
            hbmp.SaveBitmapFile( hdc, self.tempDirectory + "\dfIcontemp.bmp")
            im = Image.open(self.tempDirectory + "\dfIcontemp.bmp")
            return ImageToIcon(im)
        return None

    def WindowsGetIconFilenameFromExt(self, ext):
        default = os.getenv("systemroot") + "\\system32\\imageres.dll", -2
        if ext == '':
            return default
        ext = '.' + str(ext)
        try:
            for mode in ( KEY_WOW64_64KEY, KEY_WOW64_32KEY ):
                aKey = OpenKey(self.aReg, ext, 0, KEY_READ | mode)
                val = QueryValue(aKey, None)
                try:
                    aKey2 = OpenKey(self.aReg, val+'\\CurVer', 0, KEY_READ | mode)
                    val2 = QueryValue(aKey2, None)
                    val = val2
                except:
                    pass
                aKey = OpenKey(self.aReg, val+'\\DefaultIcon', 0, KEY_READ | mode)
                val,type = QueryValueEx(aKey, "")
                t = val.split(',')
                fname = t[0]
                if len(t) < 2:
                    index = 0
                else:
                    index = int(t[1])
                if fname[0:12] == "%SystemRoot%":
                    return os.getenv("systemroot") + fname[12:], index
                if fname == "%1" or fname == '"%1"':
                    return default
                if fname[1] != ":":
                    return os.getenv("systemroot") + "\\system32\\" + fname, index
                return fname, index
        except:
            return default

    def getFolderIcon(self):
        return self.folderIcon
    
    def getFileIcon(self, path):
        ext = fsPathExt(path)
        if platform.system() == 'Windows' and Df.d.config.showIcons:
            r = self.WindowsIconFromFilename(path)
            if r:
                data, icon = r
                return icon
            r = self.WindowsGetIconFilenameFromExt(ext)
            if r:
                fname, index = r
                r = self.WindowsIconFromFilename(fname, index)
                if r:
                    data, icon = r
                    return icon
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
        im = im.resize((letterSize, letterSize))
        h = hashlib.md5(ext.encode()).hexdigest()
        h = int(h[28:32], 16)
        coff = h/65536.0
        #bgim = colorize(self.bgim, coff*360.0)
        idx = int(coff*(self.bgimnum-0.0001))
        #bgim = self.bgims[int(coff*(self.bgimnum-0.0001))].copy()
        #bgim = colorize(bgim, 0)

        bgim = self.drawRectangle(self.size, self.bgimcols[idx][0], self.bgimcols[idx][1])
        
        offs = int((self.size[0]-letterSize)/2)
        bgim.paste(im, (offs,offs), im)
        #im = Image.composite(im, bgim, im)

        (data, icon) = ImageToIcon(bgim)
        self.icons[ext] = (data, icon)
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


