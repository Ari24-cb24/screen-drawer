import os
import logging
import win32con
import win32clipboard as clipboard
from io import BytesIO

import pygame
import screeninfo
import pyautogui

import utils

pygame.init()

class ScreenDrawer:
    def __init__(self):
        screen_info = screeninfo.get_monitors()[0]
        self.WIDTH, self.HEIGHT = screen_info.width, screen_info.height - 10
        self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT = self.WIDTH, self.HEIGHT
        self.screenshot_x = self.screenshot_y = 0

        self.stroke_size = 3
        self.max_stroke_size = 30

        self.saved_zoomed_frames = []
        self.current_zoom_frame_index = -1

        self.screenshot = pyautogui.screenshot()
        self.screenshot = utils.img_to_surf(self.screenshot)

        os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(0, 10)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.draw_surface = self.draw_surface.convert_alpha(self.draw_surface)

        pygame.display.set_caption("Pygame Preset")
        pygame.display.set_icon(pygame.image.load("./assets/icons/icon.png"))

    def startup_screen(self):
        logging.info("Setting up screen")
        self.screen.blit(pygame.transform.scale(self.screenshot, (self.WIDTH, self.HEIGHT)), (self.screenshot_x, self.screenshot_y))
        self.draw_surface.fill((0, 0, 0, 0))
        self.screen.blit(self.draw_surface, (self.screenshot_x, self.screenshot_y))

    def reset_drawing(self):
        logging.info("Resetting drawing")
        self.screen.blit(self.screenshot, (self.screenshot_x, self.screenshot_y))
        self.draw_surface.fill((0, 0, 0, 0))
        self.screen.blit(self.draw_surface, (self.screenshot_x, self.screenshot_y))

    def reset_screen(self):
        """
        Resets the screen size, zoom, position and the drawing
        """

        logging.info("Resetting screen")

        if self.saved_zoomed_frames:
            last_zoom_frame: tuple = self.saved_zoomed_frames.pop(0)
            self.current_zoom_frame_index = -1
            self.screenshot = last_zoom_frame[0]
            self.draw_surface = last_zoom_frame[1]

        self.screenshot_x = 0
        self.screenshot_y = 0

        self.draw_surface.fill((0, 0, 0))
        self.draw_surface.fill((0, 0, 0, 0))
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.screenshot, (0, 0))
        self.screen.blit(self.draw_surface, (0, 0))

        self.ZOOMED_WIDTH = self.WIDTH
        self.ZOOMED_HEIGHT = self.HEIGHT

        self.saved_zoomed_frames = []

    def save_clipboard(self):
        """
        Saves the current screenshot and drawing surface in the clipboard.
        The zoom and position also applies to the screenshot
        """
        logging.info("Copying surface into clipboard")

        final_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        final_surface.blit(pygame.transform.smoothscale(self.screenshot, (self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT)),
                           (self.screenshot_x, self.screenshot_y))
        final_surface.blit(pygame.transform.smoothscale(self.draw_surface, (self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT)),
                           (self.screenshot_x, self.screenshot_y))
        image = utils.surf_to_img(final_surface)

        with BytesIO() as output:
            image.save(output, "BMP")
            data = output.getvalue()[14:]

        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardData(win32con.CF_DIB, data)
        clipboard.CloseClipboard()

    def run(self):
        self.startup_screen()

        last_mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        straight_line_pos = []
        mouse_distance = [0, 0]
        space_pressed = False
        run = True

        while run:
            self.screen.blit(self.draw_surface, (self.screenshot_x, self.screenshot_y))
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
                        space_pressed = True
                        mouse_distance = [abs(self.screenshot_x - x), abs(self.screenshot_y - y)]

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        space_pressed = False

            x, y = pygame.mouse.get_pos()
            if pygame.key.get_mods() & pygame.KMOD_ALT:
                if keys[pygame.K_r]:
                    self.reset_drawing()
                else:
                    if direction != 0:
                        self.stroke_size += direction
                        self.stroke_size = max(1, min(self.stroke_size, self.max_stroke_size))

            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                if keys[pygame.K_c]:
                    self.save_clipboard()

                if keys[pygame.K_r]:
                    self.reset_screen()

                if space_pressed:
                    if self.screenshot_x < x < self.screenshot_x + self.ZOOMED_WIDTH:
                        if self.screenshot_y < y < self.screenshot_y + self.ZOOMED_HEIGHT:
                            if (x, y) != last_mouse_pos:
                                self.screenshot_x = x - mouse_distance[0]
                                self.screenshot_y = y - mouse_distance[1]

                                self.screen.fill((0, 0, 0))
                                self.screen.blit(self.screenshot, (self.screenshot_x, self.screenshot_y))

                if direction == 1:
                    self.ZOOMED_WIDTH *= 1.5
                    self.ZOOMED_HEIGHT *= 1.5
                    self.ZOOMED_WIDTH = int(self.ZOOMED_WIDTH)
                    self.ZOOMED_HEIGHT = int(self.ZOOMED_HEIGHT)

                    self.saved_zoomed_frames.append((self.screenshot, self.draw_surface))
                    self.current_zoom_frame_index = len(self.saved_zoomed_frames) - 1

                    self.screenshot = pygame.transform.smoothscale(self.screenshot,
                                                                   (self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT))
                    self.screen.blit(self.screenshot, (self.screenshot_x, self.screenshot_y))
                    self.draw_surface = pygame.transform.smoothscale(self.draw_surface,
                                                                     (self.ZOOMED_WIDTH, self.ZOOMED_HEIGHT))
                    self.screen.blit(self.draw_surface, (self.screenshot_x, self.screenshot_y))

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
                        self.screen.blit(self.screenshot, (self.screenshot_x, self.screenshot_y))
                        self.screen.blit(self.draw_surface, (self.screenshot_x, self.screenshot_y))

            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if pygame.mouse.get_pressed()[0]:
                    if len(straight_line_pos) == 0:
                        straight_line_pos.append([x - self.screenshot_x, y - self.screenshot_y])

                    if len(straight_line_pos) == 1:
                        dirs = utils.calc_direction(straight_line_pos[0][0], straight_line_pos[0][1], x - self.screenshot_x, y - self.screenshot_y)

                        if dirs[0] != 0 and dirs[1] != 0:
                            if abs(dirs[2]) > abs(dirs[3]):
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0],
                                                 (x - self.screenshot_x, straight_line_pos[0][1]), self.stroke_size)
                            else:
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0],
                                                 (straight_line_pos[0][0], y - self.screenshot_y), self.stroke_size)
                        else:
                            if dirs[0] != 0:
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0],
                                                 (x - self.screenshot_x, straight_line_pos[0][1]), self.stroke_size)

                            if dirs[1] != 0:
                                pygame.draw.line(self.draw_surface, (0, 255, 0), straight_line_pos[0],
                                                 (straight_line_pos[0][0], y - self.screenshot_y), self.stroke_size)

            else:
                straight_line_pos = []

            if pygame.mouse.get_pressed()[0] and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if self.screenshot_x < x < self.screenshot_x + self.ZOOMED_WIDTH:
                    if self.screenshot_y < y < self.screenshot_y + self.ZOOMED_HEIGHT:
                        pygame.draw.line(self.draw_surface, (255, 0, 0), last_mouse_pos, (x - self.screenshot_x, y - self.screenshot_y),
                                         self.stroke_size)

            last_mouse_pos = (x - self.screenshot_x, y - self.screenshot_y)
            pygame.display.update()

        pygame.quit()