import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
import sys

T_P = 10
GREEN = pg.Color(0, 255, 0)
WHITE = pg.Color(255, 255, 255)

class Map(object):
    
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.m = {}
        for x in xrange(w):
            self.m[(x, h-1)] = Ground(x, h-1)

    def draw(self, surface, camera):
        ul_t = self.pixel_to_tile(camera.x, camera.y)
        rect = surface.get_rect()
        dr_t = self.pixel_to_tile(camera.x + rect[2], camera.y + rect[3])
        for tile_x in xrange(ul_t[0], dr_t[0]+1):
            for tile_y in xrange(ul_t[1], dr_t[1]+1):
                if self.m.has_key((tile_x, tile_y)):
                    tile = self.m[(tile_x, tile_y)]
                    surface.blit(tile.image, camera.to_local(tile.rect))

    def pixel_to_tile(self, p_x, p_y):
        return (p_x / T_P, p_y / T_P)       

    def add_tile(self, t_x, t_y):
        self.m[(t_x, t_y)] = Ground(t_x, t_y)

class Tile(Sprite):

    def __init__(self, x, y, color):
        Sprite.__init__(self)
        
        self.image = pg.Surface([T_P, T_P])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.move_ip(x*T_P, y*T_P)

class Ground(Tile):

    def __init__(self, x, y):
        Tile.__init__(self, x, y, GREEN)
        self.solid = True

class Camera(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_local(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)

    def to_global(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)
        

 
pg.init()
fpsClock = pg.time.Clock()
WIDTH = 640
HEIGHT = 480
window = pg.display.set_mode((WIDTH, HEIGHT))
world_map = Map(64, 48)
camera = Camera(0, 0)
mouse_x, mouse_y = 0, 0
mouse_button_pressed = False

while True:
    window.fill(WHITE)

    world_map.draw(window, camera)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            mouse_button_pressed = True
        elif event.type == MOUSEBUTTONUP:
            mouse_button_pressed = False

    if mouse_button_pressed:
        mouse_x, mouse_y = event.pos
        global_x, global_y = camera.to_global((mouse_x, mouse_y))
        world_map.add_tile(global_x / T_P, global_y / T_P)




    pg.display.flip()
    fpsClock.tick(120)


    
