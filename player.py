import pygame as pg
import conf
from conf import NPC_PATH, GAME_SAV
from graphics import map_zammbauer as mp
import random
from BattleManager import BattleManager
from utilities import load_game_saves
from menu import Menu
import json

class Player:
    def __init__(self, special):
        self.special = special
        self.player, self.team, self.items = load_game_saves()

        with open(GAME_SAV, "r", encoding="utf-8") as file:
            data = json.load(file)
        index = 0
        for i in self.team:
            i.current_hp = data["pokemons"][index][4] 
            index+=1
        self.image = pg.image.load("graphics/assets/player.png")
        self.rect = self.image.get_rect(center = (self.player[3],self.player[4]))
        self.speed = conf.PLAYER_SPEED
        self.in_battle = False
        self.collision = set()

        self.battle_counter = 0

        pg.mixer.music.set_volume(1)
        self.sound = pg.mixer.music.load("sound/overworld.ogg")

        self.name = self.player[0]
        self.money = self.player[1]
        self.badges = self.player[2]


    def move(self, keys, boundary, boundary_list, ):
        dx, dy = 0, 0
        if keys[pg.K_UP]: dy -= self.speed
        if keys[pg.K_DOWN]: dy += self.speed
        if keys[pg.K_LEFT]: dx -= self.speed
        if keys[pg.K_RIGHT]: dx += self.speed

        new_rect = self.rect.move(dx, dy)

        if boundary.contains(new_rect):
            if not any(new_rect.colliderect(b) for b in boundary_list):
                self.rect = new_rect
                self.player[3] = self.rect.x
                self.player[4] = self.rect.y
             

    def check_collision(self):
        for key, value in self.special.items():
            if self.rect.colliderect(value) == False:
                self.collision.discard(value.center)

            if self.rect.colliderect(value) and key != "Heiler" and self.in_battle == False and value.center not in self.collision:
                self.collision.add(value.center)
                self.in_battle = True
                self.battle_counter += 1

                #print(key)
                battle_manager = BattleManager(self.player, self.team, self.items, self.battle_counter, key, True)
                battle_manager.run()

                self.in_battle = False
                pg.mixer.music.stop()
                pg.mixer.music.load("sound/overworld.ogg")
                pg.mixer.music.play(-1)
            
            elif self.rect.colliderect(value) and key == "Heiler" and self.in_battle == False and value.center not in self.collision:
                self.collision.add(value.center)
                if self.player[1] >= 200*self.player[2]:
                    self.player[1] -= 200*self.player[2]
                    for i in self.team:
                        i.current_hp = i.max_hp
                    with open(NPC_PATH, "r", encoding="utf-8") as file:
                        data = json.load(file)
                    self.items = data["Heiler"]["Items"].copy()
                    #print(self.items)

        for value in mp.battle_rect:
            if self.rect.colliderect(value) == False:
                self.collision.discard(value.center)
                continue

            if self.rect.colliderect(value) and self.in_battle == False and value.center not in self.collision:
                self.collision.add(value.center)
                if(random.randint(1,100//conf.battle_chance) == 1):
                    self.in_battle = True
                    self.battle_counter += 1
                    #--------------------------------
                    #Kampfbildschirmklasse
                    battle_manager = BattleManager(self.player, self.team, self.items, self.battle_counter, None, False)
                    battle_manager.run()
                    #print("Hallo")
                    #--------------------------------
                    self.in_battle = False
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/overworld.ogg")
                    pg.mixer.music.play(-1)

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))

    def inv(self, keys, i_pressed):
        if keys[pg.K_i] or i_pressed:
            menu = Menu(self.player, self.team, self.items)
            menu.run()
            self.team = menu.new_team().copy()