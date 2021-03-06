# Screen Drawer
Apples Drawing and Zoom feature in a nutshell

## Installation

If you haven't installed Python 3.7+ yet, install it here: https://www.python.org/downloads/release/python-3710/  
After that, follow these steps

1. Download the zip-archiv containing ScreenDrawer: https://github.com/Ari24-cb24/screen-drawer/archive/refs/tags/1.2a.zip   
2. Extract the zip-archiv
3. Install the following packages if you haven't already installed it
   - pygame 1.9.6+ (pip install pygame)
   - desktopmagic (pip install desktopmagic)
   - pyautogui (pip install pyautogui)
    
4. **Run Main.pyw**  
5. (Optional Step) Make a linkage from the Startup folder to Main.pyw  

<br />
If you have problems installing pygame, install the binary from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame instead.  

**Run**  

```bash
pip install wheel
pip install pygame_binary_filename.whl
```

To install pygame via the binary.

## Features

The programs runs in the background.  
If you press Left CTRL/STRG, and the Left Windows button, a pygame window will appear with a screenshot of your screen.  
ScreenDrawer will take a screenshot of the screen where you're mouse cursor currently is.
  
You can then draw anything on that screen:
- **Left Mouseclick (LMB)** to draw something
- **SHIFT + Left Mouseclick (LMB)** to draw a straight line
- **ALT + r** to reset the drawing
- **CTRL/STRG + r** to reset everything
- **ALT + Mousewheel** to change stroke size  
- **CTRL/STRG + Mousewheel** to Zoom into the image  
- **CTRL/STRG + Spacebar** to move the image around
- **CTRL/STRG + c** to copy the current image. Also applies the zoom, move and drawing

## Currently known bugs

- If you draw something, while you're zoomed in, and you zoom out, the drawing will vanish
- Screenshots are incorrectly cropped on high-DPI displays. Windows returns display geometry data scaled for the DPI, while the actual screenshots are unscaled. Workaround: Right-click on python.exe, Properties, Compatibility tab, check 'Disable display scaling on high DPI settings'. Repeat for pythonw.exe.

## Changelog

> v**1.2a**
> Fixed bug where window is permanently topmost
> Pygame Window title set

> v**1.2**
> * *Added multiple screen support. You can now screenshot your 2nd monitor as well!*
> * *Fixed issue where ScreenDrawer is not the topmost window*
> * *Missing packages are now automatically downloaded if missing*
> * *ScreenDrawer now uses desktopmagic instead of pyautogui and screeninfo for taking screenshots*
> * *Some more warnings are now implemented*
> * *Main.py is now Main.pyw*

> v**1.1a**
> * *Added functionality to add multiple keybinds*
> * *Fixed Readme bugs*
> * *Debug mode is now on default false*
> * *Improved code readability*

<br />

> v**1.1**
> * *Added ALT + r Keybind for resetting the drawing*
> * *Improved code readability*
> * *Pep8'ed the code but in a good way*
> * *Improved README.md*
> * *Added logging for more debugging*
> * *Added Keybind CTRL + c to copy the current image. Also applies the zoom, move and the drawing*

## License stuff

Free to use
