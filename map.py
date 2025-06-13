import pygame as pg

class Map:
    def __init__(self):
        self.image = pg.image.load("Map.png")

    def draw(self, screen, camera):
        screen.blit(self.image, (-camera.x, -camera.y))
