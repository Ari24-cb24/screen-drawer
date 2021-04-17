import logging
import os
from KeyListener import Listener

DEBUG = False

def setup_logger():
    log_level = logging.DEBUG if DEBUG else logging.ERROR
    logging.basicConfig(format="[%(levelname)s] %(message)s (%(module)s)", level=log_level)

def check_missing_packages():
    def error_missing_package(package_name):
        logging.exception("Package '{0}' is not installed! Please install it in order to use ScreenDrawer!".format(package_name))
        raise RuntimeError("Package '{0}' is not installed! Please install it in order to use ScreenDrawer!".format(package_name))

    try:
        import pip
    except ImportError:
        pip = None

    try:
        import desktopmagic
    except ImportError:
        if pip is not None:
            pip.main(["install", "desktopmagic"])
        else:
            error_missing_package("desktopmagic")

    try:
        import pygame
    except ImportError:
        if pip is not None:
            pip.main(["install", "pygame"])
        else:
            error_missing_package("pygame")

    try:
        import pyautogui
    except ImportError:
        if pip is not None:
            pip.main(["install", "pyautogui"])
        else:
            error_missing_package("pyautogui")

def check_os():
    if os.name != "nt":
        logging.warning("ScreenDrawer currently works only on windows. Linux has not been tested yet! Be careful.")


if __name__ == '__main__':
    check_missing_packages()
    check_os()
    setup_logger()

    listener = Listener()
    listener.listen()
