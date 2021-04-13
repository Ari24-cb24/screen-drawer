from PIL import Image
import pygame

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
