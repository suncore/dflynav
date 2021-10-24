# Dragonfly Navigator
A simple and efficient file manager for Linux/KDE.

![Screen shot](images/screenshot.png)

Dragonfly Navigator has:

- Fast folder navigation
- Predictable file and folder operations without relying on fiddly drag-n-drop
- Asynchronous file operations with job control and a log of performed operations
- Quick preview (Alt key + mouse hover) for text and images
- AVIF, HEIF, JPG etc. image preview and icons

## Installing and running on Ubuntu / Debian
Download .deb file from the [github release page](https://github.com/suncore/dflynav/releases). Then install like this:
```
$ sudo dpkg -i dragonfly_xxx.deb
$ sudo apt install -f (this may not be necessary)
```
Run:
```
$ dragonfly 
```
Dragonfly Navigator should now also be possible to find in the desktop application menu.

## Installing and running on other distributions than Ubuntu / Debian
Download the .tar.gz package from the [github release page](https://github.com/suncore/dflynav/releases). Then install like this:

```
$ tar xzf dragonfly_xxx.tar.gz
$ cd dragonfly
$ ./setup 
```

Run:
```
$ dragonfly 
```
If dragonfly can not be found you may need to log out and in again, otherwise add ~/.local/bin to your path. Dragonfly Navigator should now also be possible to find in the desktop application menu.

If you have problems, contact me at henrik@harmsen.se. Dragonfly Navigator has only been tested on kubuntu 21.04, 21.10, latest Manjaro KDE and Debian Sid.


## Building and running from sources 
These instructions are for ubuntu.
1. Clone from github
```
$ git clone https://github.com/suncore/dflynav.git
```
2. Install prerequisites
```
$ sudo apt install pyqt5-dev-tools qtcreator libkf5-dev libkdeframeworks5-dev libkf5widgetsaddons-dev libkf5xmlgui-dev libkf5textwidgets-dev libkf5kio-dev build-essential libkf5config-dev libkdecorations2-dev libqt5x11extras5-dev qtdeclarative5-dev extra-cmake-modules libkf5guiaddons-dev libkf5configwidgets-dev libkf5windowsystem-dev libkf5coreaddons-dev gettext
```
3. Building:
```
$ cd dragonfly/src
$ ./build
```
4. Run:
```
$ ./dragonfly
```

Use qtcreator to edit the GUI .ui files.

