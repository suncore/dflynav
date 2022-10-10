# Dragonfly Navigator
A simple and efficient dual pane file manager for Linux.

![Screen shot](images/screenshot.png)

Notable features:

- Fast folder navigation
- Predictable file and folder operations without relying on drag-n-drop or copy/paste.
- Asynchronous file operations with queue management
- Quick preview (Alt key + mouse hover) for text and images
- AVIF, HEIF, JPG etc. image preview and icons

## Installing and running on Ubuntu / Debian
Download .deb file from the [github release page](https://github.com/suncore/dflynav/releases). Then install like this:
```
$ sudo dpkg -i dragonfly_xxx.deb
$ sudo apt install -f
```
Run:
```
$ dragonfly 
```
Dragonfly Navigator should now also be possible to find in the desktop application menu.

## Installing and running on other distributions than Ubuntu / Debian
Download the .tar.gz package from the [github release page](https://github.com/suncore/dflynav/releases). Then install like this:

```
Install the following dependencies: python3-pil adwaita-qt python3-pyqt5
$ tar xzf dragonfly_xxx.tar.gz
$ cd dragonfly
$ ./setup 
```

Run:
```
$ dragonfly 
```
If dragonfly can not be found you may need to log out and in again, otherwise add ~/.local/bin to your path. Dragonfly Navigator should now also be possible to find in the desktop application menu.

If you have problems, contact me at henrik@harmsen.se. 


## Building and running from sources 
These instructions are for ubuntu.
1. Clone from github
```
$ git clone https://github.com/suncore/dflynav.git
```
2. Install prerequisites
```
$ sudo apt install pyqt5-dev-tools qtcreator libkf5-dev libkdeframeworks5-dev libkf5widgetsaddons-dev libkf5xmlgui-dev libkf5textwidgets-dev libkf5kio-dev build-essential libkf5config-dev libkdecorations2-dev libqt5x11extras5-dev qtdeclarative5-dev extra-cmake-modules libkf5guiaddons-dev libkf5configwidgets-dev libkf5windowsystem-dev libkf5coreaddons-dev gettext libgtkmm-3.0-dev python3-pil adwaita-qt python3-pyqt5
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

