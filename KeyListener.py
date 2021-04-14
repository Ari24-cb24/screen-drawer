import time
import logging
from pynput import keyboard

from ScreenDrawer import ScreenDrawer

class Listener:
    def __init__(self):
        """
        Initializes keybinds
        You can currently only create keybinds that have 2 keys min and max
        """
        self.listener_stages = [False, False]
        self.keybinds = [
                (keyboard.Key.ctrl_l, keyboard.Key.cmd_l)
            ]

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def run(self):
        logging.info("Opening ScreenDrawer")
        screenDrawer = ScreenDrawer()
        screenDrawer.run()

    def on_press(self, key):
        for i in range(len(self.keybinds)):
            if key == self.keybinds[i][0] and not self.listener_stages[1]:
                self.listener_stages[0] = True

            if key == self.keybinds[i][1]:
                self.listener_stages[1] = True

            if self.listener_stages[0] and self.listener_stages[1]:
                time.sleep(1)

                self.run()
                self.listener_stages = [False, False]
                break

    def on_release(self, key):
        for i in range(len(self.keybinds)):
            if key == self.keybinds[i][0]:
                self.listener_stages[0] = False

            if key == self.keybinds[i][1]:
                self.listener_stages[1] = False

    def listen(self):
        self.listener.run()