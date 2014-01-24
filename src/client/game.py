import sys
import pygame as pg
from pygame.sprite import Sprite, Group, spritecollide

pg.init()
SIZE = WIDTH, HEIGHT = 1024, 480

RED = pg.Color("red")
BLACK = pg.Color("black")
CLOCK = pg.time.Clock()

FPS = 60
GRAVITY = 1

class Player(Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        pg.draw.circle(self.image, RED, (20, 20), 20)
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
        self.speed = 5

    def update(self):
        self.dy += GRAVITY

        self.rect.move_ip(self.dx, self.dy)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.dx = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.dy = 0

    def jump(self):
        if self.dy == 0:
            self.dy = -20

class Game(object):
    def __init__(self):
        self.player = Player()
        self.tiles = Group()
        self.all_sprites = Group(self.player, self.tiles)
        self.screen = pg.display.set_mode(SIZE)

    def run(self):
        while True:
            CLOCK.tick(FPS)
            self.handle_events()

            self.all_sprites.update()
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                elif event.key == pg.K_LEFT:
                    self.player.dx = -5
                elif event.key == pg.K_RIGHT:
                    self.player.dx = 5
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    if (self.player.dx < 0):
                        self.player.dx = 0
                elif event.key == pg.K_RIGHT:
                    if (self.player.dx > 0):
                        self.player.dx = 0

if __name__ == "__main__":
    Game().run()
