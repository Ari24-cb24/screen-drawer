from PIL import Image
from ctypes import windll
import pyautogui
import sys
import tempfile
import os
import subprocess

import pygame
from desktopmagic.screengrab_win32 import getDisplayRects

class Monitor:
    def __init__(self, bbox):
        self.bbox = bbox
        self.x = bbox[0]
        self.y = bbox[1]
        self.width = bbox[2] - bbox[0]
        self.height = bbox[3] - bbox[1]

def surf_to_img(surf):
    return Image.frombytes("RGBA", surf.get_size(), pygame.image.tostring(surf, "RGBA", False))


def img_to_surf(img):
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)


def calc_direction(x1, y1, x2, y2):
    direction_x_ = x2 - x1
    direction_x = -1 if direction_x_ < 0 else 1

    direction_y_ = y2 - y1
    direction_y = -1 if direction_y_ < 0 else 1

    return direction_x, direction_y, direction_x_, direction_y_

def screenshot(bbox=None, include_layered_windows=False, all_screens=False):
    if sys.platform == "darwin":
        fh, filepath = tempfile.mkstemp(".png")
        os.close(fh)
        subprocess.call(["screencapture", "-x", filepath])
        im = Image.open(filepath)
        im.load()
        os.unlink(filepath)
        if bbox:
            im = im.crop(bbox)
    else:
        offset, size, data = Image.core.grabscreen(include_layered_windows, all_screens)
        im = Image.frombytes(
            "RGB",
            size,
            data,
            # RGB, 32-bit line padding, origin lower left corner
            "raw",
            "BGR",
            (size[0] * 3 + 3) & -4,
            -1,
        )

        if bbox:
            x0, y0 = offset
            left, top, right, bottom = bbox
            im = im.crop((left - x0, top - y0, right - x0, bottom - y0))

    return im

def get_current_monitor():
    x, y = pyautogui.position()
    monitors = (getDisplayRects())

    for monitor in monitors:
        left, top, right, bottom = monitor
        if left <= x <= right:
            if top <= y <= bottom:
                return Monitor(monitor)

    return Monitor(monitors[0])

def move_window_to_front():
    hwnd = pygame.display.get_wm_info()["window"]
    windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 3)