import time
import logging
from pynput import keyboard

from ScreenDrawer import ScreenDrawer

class Listener:
    def __init__(self):
        self.listener_stages = [False, False]
        self.keybind = (keyboard.Key.ctrl_l, keyboard.Key.cmd_l)

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def run(self):
        logging.info("Opening ScreenDrawer")
        screenDrawer = ScreenDrawer()
        screenDrawer.run()

    def on_press(self, key):
        if key == self.keybind[0] and not self.listener_stages[1]:
            self.listener_stages[0] = True

        if key == self.keybind[1]:
            self.listener_stages[1] = True

        if self.listener_stages[0] and self.listener_stages[1]:
            time.sleep(1)

            self.run()
            self.listener_stages = [False, False]

    def on_release(self, key):
        if key == keyboard.Key.ctrl_l:
            self.listener_stages[0] = False

        if key == keyboard.Key.cmd_l:
            self.listener_stages[1] = False

    def listen(self):
        self.listener.run()