

Cloned from: https://github.com/timgott/gtk-open-with


# gtk-open-with

This is a very simple tool similar to scripts like `xdg-open`, but instead of running the default application it shows you a GTK app chooser (the same as the "Open with Application" function in Nautilus).

## Usage

```
gtk-open-with [files]
```

## Building

```
mkdir build
cd build
cmake ..
make
```

## Dependencies
```
libgtkmm-3.0-dev
```
