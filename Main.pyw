import pygame
import screeninfo
import pyautogui
import os
import threading
import time
from pynput import keyboard
pygame.init()

def img_to_surf(img):
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

def calc_direction(x1, y1, x2, y2):
    direction_x_ = x2 - x1
    direction_x = -1 if direction_x_ < 0 else 1

    direction_y_ = y2 - y1
    direction_y = -1 if direction_y_ < 0 else 1

    return direction_x, direction_y, direction_x_, direction_y_

# TODO: Zooming
class ScreenDrawer:
    def __init__(self):
        s = screeninfo.get_monitors()[0]

        self.WIDTH, self.HEIGHT = s.width, s.height - 10

        self.screenshot = pyautogui.screenshot()
        self.screenshot = img_to_surf(self.screenshot)

        os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(0, 10)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.draw_surface = self.draw_surface.convert_alpha(self.draw_surface)

        pygame.display.set_caption("Pygame Preset")
        pygame.display.set_icon(pygame.image.load("./assets/icons/icon.png"))

        self.stroke_size = 3
        self.max_stroke_size = 30
        
        self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT = self.WIDTH, self.HEIGHT

        self.saved_zoomed_frames = []
        self.current_zoom_frame_index = -1

        self.X, self.Y = [0, 0]
        
    def startup_screen(self):
        self.screen.blit(pygame.transform.scale(self.screenshot, (self.WIDTH, self.HEIGHT)), (self.X, self.Y))

        self.draw_surface.fill((0, 0, 0, 0))
        self.screen.blit(self.draw_surface, (self.X, self.Y))

    def reset_screen(self):
        # TODO: reset zoom
        self.screen.blit(self.screenshot, (self.X, self.Y))
        self.draw_surface.fill((0, 0, 0, 0))
        self.screen.blit(self.draw_surface, (self.X, self.Y))

    def run(self):
        self.startup_screen()
        last_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        straight_line_pos = []

        spacebar_down = False
        distance = [0, 0]

        run = True
        while run:
            self.screen.blit(self.draw_surface, (self.X, self.Y))
            keys = pygame.key.get_pressed()
            direction = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        direction = 1

                    if event.button == 5:
                        direction = -1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        x, y = pygame.mouse.get_pos()
                        spacebar_down = True
                        distance = [abs(self.X - x), abs(self.Y - y)]

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        spacebar_down = False

            x, y = pygame.mouse.get_pos()
            if pygame.key.get_mods() & pygame.KMOD_ALT:
                if keys[pygame.K_r]:
                    self.reset_screen()
                else:
                    if direction != 0:
                        self.stroke_size += direction
                        self.stroke_size = max(1, min(self.stroke_size, self.max_stroke_size))
            
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                if keys[pygame.K_r]:
                    if self.saved_zoomed_frames:
                        last_zoom_frame = self.saved_zoomed_frames.pop(0)
                        self.current_zoom_frame_index = -1
                        self.screenshot = last_zoom_frame[0]
                        self.draw_surface = last_zoom_frame[1]

                    self.X = 0
                    self.Y = 0

                    self.draw_surface.fill((0, 0, 0))
                    self.draw_surface.fill((0, 0, 0, 0))
                    self.screen.fill((0, 0, 0))
                    self.screen.blit(self.screenshot, (0, 0))
                    self.screen.blit(self.draw_surface, (0, 0))

                    self.ZOOMED_WIDTH = self.WIDTH
                    self.ZOOMED_HEIGHT = self.HEIGHT

                    self.saved_zoomed_frames = []

                if spacebar_down:
                    if self.X < x < self.X + self.ZOOMED_WIDTH:
                        if self.Y < y < self.Y + self.ZOOMED_HEIGHT:
                            if (x, y) != last_pos:
                                self.X = x - distance[0]
                                self.Y = y - distance[1]

                                self.screen.fill((0, 0, 0))
                                self.screen.blit(self.screenshot, (self.X, self.Y))

                if direction == 1:
                    self.ZOOMED_WIDTH *= 1.5
                    self.ZOOMED_HEIGHT *= 1.5
                    self.ZOOMED_WIDTH = int(self.ZOOMED_WIDTH)
                    self.ZOOMED_HEIGHT = int(self.ZOOMED_HEIGHT)

                    self.saved_zoomed_frames.append((self.screenshot, self.draw_surface))
                    self.current_zoom_frame_index = len(self.saved_zoomed_frames) - 1

                    self.screenshot = pygame.transform.smoothscale(self.screenshot, (self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT))
                    self.screen.blit(self.screenshot, (self.X, self.Y))
                    self.draw_surface = pygame.transform.smoothscale(self.draw_surface, (self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT))
                    self.screen.blit(self.draw_surface, (self.X, self.Y))

                elif direction == -1:
                    if self.current_zoom_frame_index != -1:
                        self.ZOOMED_WIDTH /= 1.5
                        self.ZOOMED_HEIGHT /= 1.5
                        self.ZOOMED_WIDTH = int(self.ZOOMED_WIDTH)
                        self.ZOOMED_HEIGHT = int(self.ZOOMED_HEIGHT)

                        last_zoom_frame = self.saved_zoomed_frames.pop(self.current_zoom_frame_index)
                        self.current_zoom_frame_index -= 1
                        self.screenshot = last_zoom_frame[0]
                        self.draw_surface = last_zoom_frame[1]

                        self.screen.fill((0, 0, 0))
                        self.screen.blit(self.screenshot, (self.X, self.Y))
                        self.screen.blit(self.draw_surface, (self.X, self.Y))

            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if pygame.mouse.get_pressed()[0]:
                    if len(straight_line_pos) == 0:
                        straight_line_pos.append([x - self.X, y - self.Y])

                    if len(straight_line_pos) == 1:
                        dirs = calc_direction(straight_line_pos[0][0], straight_line_pos[0][1], x - self.X, y - self.Y)

                        if dirs[0] != 0 and dirs[1] != 0:
                            if abs(dirs[2]) > abs(dirs[3]):
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0], (x - self.X, straight_line_pos[0][1]), self.stroke_size)
                            else:
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0], (straight_line_pos[0][0], y - self.Y), self.stroke_size)
                        else:
                            if dirs[0] != 0:
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0], (x - self.X, straight_line_pos[0][1]), self.stroke_size)

                            if dirs[1] != 0:
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0], (straight_line_pos[0][0], y - self.Y), self.stroke_size)

            else:
                straight_line_pos = []

            if pygame.mouse.get_pressed()[0] and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if self.X < x < self.X + self.ZOOMED_WIDTH:
                    if self.Y < y < self.Y + self.ZOOMED_HEIGHT:
                        pygame.draw.line(self.draw_surface, (255, 0, 0), last_pos, (x - self.X, y - self.Y), self.stroke_size)

            last_pos = (x - self.X, y - self.Y)
            pygame.display.update()

        pygame.quit()

class Listener:
    def __init__(self):
        self.stages = [False, False]
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def run(self):
        s = ScreenDrawer()
        s.run()

    def on_press(self, key):
        if key == keyboard.Key.ctrl_l and not self.stages[1]:
            self.stages[0] = True

        if key == keyboard.Key.cmd_l:
            self.stages[1] = True

        if self.stages[0] and self.stages[1]:
            time.sleep(1)
            self.run()

            self.stages = [False, False]

    def on_release(self, key):
        if key == keyboard.Key.ctrl_l:
            self.stages[0] = False

        if key == keyboard.Key.cmd_l:
            self.stages[1] = False

    def listen(self):
        self.listener.run()


if __name__ == '__main__':
    listener = Listener()
    listener.listen()
    # s = ScreenDrawer()
    # s.run()
