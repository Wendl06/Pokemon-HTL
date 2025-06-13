import pygame as pg
from player import Player
from map import Map
from camera import Camera
import conf
from menu import Startbildschirm
import graphics.map_zammbauer as map_zammbauer

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((conf.SCREEN_W, conf.SCREEN_H))
        pg.display.set_caption("Pokemon HTL Edition")
        self.clock = pg.time.Clock()
        self.running = True

        pg.mixer.music.set_volume(1)
        self.sound = pg.mixer.music.load("sound/overworld.ogg")

        self.boundaries = map_zammbauer.barrier_rect
        
        #-------------------------
        self.baran = pg.image.load("graphics/assets/baran.png")
        self.Rbaran = self.baran.get_rect(center = ((12800/4),(9600/4)))
        
        self.hannah = pg.image.load("graphics/assets/hannah.png")
        self.Rhannah = self.hannah.get_rect(center = ((12800/4*3),(9600/4)))
        
        self.wendl = pg.image.load("graphics/assets/wendl.png")
        self.Rwendl = self.wendl.get_rect(center = ((12800/4),(9600/4*3)))
        
        self.tobi = pg.image.load("graphics/assets/tobi.png")
        self.Rtobi = self.tobi.get_rect(center = ((12800/4*3),(9600/4*3)))

        self.valle = pg.image.load("graphics/assets/valle.png")
        self.Rvalle = self.helli.get_rect(center = ((12800/2),(9600/2)))
        
        self.heiler = pg.image.load("graphics/assets/heiler.png")
        self.Rheiler = self.heiler.get_rect(center = (8800, 5000)) 

        self.special = {
            "Baran" : self.Rbaran,
            "Hannah" : self.Rhannah,
            "Wendl" : self.Rwendl,
            "Tobi" : self.Rtobi,
            "Valentin" : self.Rvalle,
            "Heiler" : self.Rheiler,
        }
        #-------------------------

        menu = Startbildschirm()
        menu.run()

        self.map = Map()
        self.player = Player(self.special)
        self.camera = Camera()

        self.start = True
        self.c_a = False
        self.i_pressed = False

    def run(self):
        pg.mixer.music.play(-1)
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(conf.TICK_SPEED)

    def handle_events(self):
        self.player.check_collision()
        self.i_pressed = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.running = False
                    pg.quit()

                if event.key == pg.K_i:
                    self.c_a = True
            if event.type == pg.KEYUP: 
                if event.key == pg.K_i and self.c_a == True:
                    self.c_a = False
                    self.i_pressed = True
                    #-------------------------------------------------------
    def update(self):
        self.keys = pg.key.get_pressed()
        self.player.move(self.keys, pg.Rect(0, 0, conf.MAP_WIDTH * conf.TILE_SIZE, conf.MAP_HEIGHT * conf.TILE_SIZE), 
                         self.boundaries)
        self.player.inv(self.keys,self.i_pressed)
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        self.screen.blit(self.baran, self.Rbaran.move(-self.camera.x, -self.camera.y))
        self.screen.blit(self.hannah, self.Rhannah.move(-self.camera.x, -self.camera.y))
        self.screen.blit(self.wendl, self.Rwendl.move(-self.camera.x, -self.camera.y))
        self.screen.blit(self.tobi, self.Rtobi.move(-self.camera.x, -self.camera.y))
        self.screen.blit(self.helli, self.Rhelli.move(-self.camera.x, -self.camera.y))
        self.screen.blit(self.heiler, self.Rheiler.move(-self.camera.x, -self.camera.y))

        pg.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()

