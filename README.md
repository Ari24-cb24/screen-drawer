# Screen Drawer
Apples Drawing and Zoom feature in a nutshell

## Installation

If you haven't installed Python 3.7+ yet, install it here: https://www.python.org/downloads/release/python-3710/  
After that, follow these steps

1. Download the zip-archiv containing ScreenDrawer: https://github.com/Ari24-cb24/screen-drawer/archive/refs/tags/1.1.zip   
2. Extract the zip-archiv
3. Install pygame 1.9.6+ if you haven't already installed it
4. **Run Main.pyw**  
5. (Optional Step) Make a linkage from the Startup folder to Main.pyw  

<br />
If you have problems installing pygame, install the binary from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame instead.  

Run  

```bash
pip install wheel
pip install pygame_binary_filename.whl
```

To install pygame via the binary.

## Features

The programs runs in the background.  
If you press Left CTRL/STRG and the Left Windows button, a pygame window will appear with a screenshot of your screen.  
  
You can then draw anything on that screen:
- **Left Mouseclick (LMB)** to draw something
- **SHIFT + Left Mouseclick (LMB)** to draw a straight line
- **ALT + r** to reset the drawing
- **CTRL/STRG + r** to reset everything
- **ALT + Mousewheel** to change stroke size  
- **CTRL/STRG + Mousewheel** to Zoom into the image  
- **CTRL/STRG + Spacebar** to move the image around

## Changelog

> v**1.1**
> * *Added ALT + r Keybind for resetting the drawing*
> * *Improved code readability*
> * *Pep8'ed the code but in a good way*
> * *Improved README.md*
> * *Added logging for more debugging*

## License stuff

Free to use
