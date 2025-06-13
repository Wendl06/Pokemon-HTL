import pygame as pg

import os

# Basisverzeichnis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dateipfade
GAME_SAV = os.path.join(BASE_DIR, "data", "savegame.json")
PKN_BLUEPRINT = os.path.join(BASE_DIR, "data", "pknblueprint.json")
ATK_PATH = os.path.join(BASE_DIR, "data", "attacks.json")
NPC_PATH = os.path.join(BASE_DIR, "data", "npcs.json")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")

# Konstante Variablen
BASE_XP_VALUE = 100
XP_MULTIPLIER = 1.5

TYPE_CHART = {
    "Normal":   {"Normal":1, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":1, "Kampf":1, "Gift":1,
                 "Boden":1, "Flug":1, "Psycho":1, "Käfer":1, "Gestein":0.5, "Geist":0, "Drache":1,
                 "Unlicht":1, "Stahl":0.5, "Fee":1},
    "Kampf":    {"Normal":2, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":2, "Kampf":1, "Gift":1,
                 "Boden":1, "Flug":0.5, "Psycho":0.5, "Käfer":0.5, "Gestein":2, "Geist":0, "Drache":1,
                 "Unlicht":2, "Stahl":2, "Fee":0.5},
    "Flug":     {"Normal":1, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":2, "Eis":1, "Kampf":2, "Gift":1,
                 "Boden":1, "Flug":1, "Psycho":1, "Käfer":2, "Gestein":0.5, "Geist":1, "Drache":1,
                 "Unlicht":1, "Stahl":0.5, "Fee":1},
    "Gift":     {"Normal":1, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":1, "Kampf":1, "Gift":0.5,
                 "Boden":0.5, "Flug":1, "Psycho":1, "Käfer":1, "Gestein":0.5, "Geist":0.5, "Drache":1,
                 "Unlicht":1, "Stahl":0, "Fee":2},
    "Boden":    {"Normal":1, "Feuer":2, "Wasser":1, "Elektro":2, "Pflanze":0.5, "Eis":1, "Kampf":1, "Gift":2,
                 "Boden":1, "Flug":0, "Psycho":1, "Käfer":0.5, "Gestein":2, "Geist":1, "Drache":1,
                 "Unlicht":1, "Stahl":2, "Fee":1},
    "Gestein":  {"Normal":1, "Feuer":2, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":2, "Kampf":0.5, "Gift":1,
                 "Boden":0.5, "Flug":2, "Psycho":1, "Käfer":2, "Gestein":1, "Geist":1, "Drache":1,
                 "Unlicht":1, "Stahl":0.5, "Fee":1},
    "Käfer":    {"Normal":1, "Feuer":0.5, "Wasser":1, "Elektro":1, "Pflanze":2, "Eis":1, "Kampf":0.5, "Gift":0.5,
                 "Boden":1, "Flug":0.5, "Psycho":2, "Käfer":1, "Gestein":1, "Geist":0.5, "Drache":1,
                 "Unlicht":2, "Stahl":0.5, "Fee":0.5},
    "Geist":    {"Normal":0, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":1, "Kampf":1, "Gift":1,
                 "Boden":1, "Flug":1, "Psycho":2, "Käfer":1, "Gestein":1, "Geist":2, "Drache":1,
                 "Unlicht":0.5, "Stahl":1, "Fee":1},
    "Stahl":    {"Normal":1, "Feuer":0.5, "Wasser":0.5, "Elektro":0.5, "Pflanze":1, "Eis":2, "Kampf":1, "Gift":1,
                 "Boden":1, "Flug":0.5, "Psycho":0.5, "Käfer":0.5, "Gestein":2, "Geist":1, "Drache":1,
                 "Unlicht":1, "Stahl":0.5, "Fee":2},
    "Feuer":    {"Normal":1, "Feuer":0.5, "Wasser":0.5, "Elektro":1, "Pflanze":2, "Eis":2, "Kampf":1, "Gift":1,
                 "Boden":1, "Flug":1, "Psycho":1, "Käfer":2, "Gestein":0.5, "Geist":1, "Drache":0.5,
                 "Unlicht":1, "Stahl":2, "Fee":1},
    "Wasser":   {"Normal":1, "Feuer":2, "Wasser":0.5, "Elektro":1, "Pflanze":0.5, "Eis":1, "Kampf":1, "Gift":1,
                 "Boden":2, "Flug":1, "Psycho":1, "Käfer":1, "Gestein":2, "Geist":1, "Drache":0.5,
                 "Unlicht":1, "Stahl":1, "Fee":1},
    "Pflanze":  {"Normal":1, "Feuer":0.5, "Wasser":2, "Elektro":0.5, "Pflanze":0.5, "Eis":1, "Kampf":1, "Gift":0.5,
                 "Boden":2, "Flug":0.5, "Psycho":1, "Käfer":0.5, "Gestein":2, "Geist":1, "Drache":0.5,
                 "Unlicht":1, "Stahl":0.5, "Fee":1},
    "Elektro":  {"Normal":1, "Feuer":1, "Wasser":2, "Elektro":0.5, "Pflanze":0.5, "Eis":1, "Kampf":1, "Gift":1,
                 "Boden":0, "Flug":2, "Psycho":1, "Käfer":1, "Gestein":1, "Geist":1, "Drache":0.5,
                 "Unlicht":1, "Stahl":1, "Fee":1},
    "Psycho":   {"Normal":1, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":1, "Kampf":2, "Gift":2,
                 "Boden":1, "Flug":1, "Psycho":0.5, "Käfer":1, "Gestein":1, "Geist":1, "Drache":1,
                 "Unlicht":0, "Stahl":0.5, "Fee":1},
    "Eis":      {"Normal":1, "Feuer":0.5, "Wasser":0.5, "Elektro":1, "Pflanze":2, "Eis":0.5, "Kampf":1, "Gift":1,
                 "Boden":2, "Flug":2, "Psycho":1, "Käfer":1, "Gestein":1, "Geist":1, "Drache":2,
                 "Unlicht":1, "Stahl":0.5, "Fee":1},
    "Drache":   {"Normal":1, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":1, "Kampf":1, "Gift":1,
                 "Boden":1, "Flug":1, "Psycho":1, "Käfer":1, "Gestein":1, "Geist":1, "Drache":2,
                 "Unlicht":1, "Stahl":0.5, "Fee":0},
    "Unlicht":  {"Normal":1, "Feuer":1, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":1, "Kampf":0.5, "Gift":1,
                 "Boden":1, "Flug":1, "Psycho":2, "Käfer":1, "Gestein":1, "Geist":2, "Drache":1,
                 "Unlicht":0.5, "Stahl":1, "Fee":0.5},
    "Fee":      {"Normal":1, "Feuer":0.5, "Wasser":1, "Elektro":1, "Pflanze":1, "Eis":1, "Kampf":2, "Gift":0.5,
                 "Boden":1, "Flug":1, "Psycho":1, "Käfer":1, "Gestein":1, "Geist":1, "Drache":2,
                 "Unlicht":2, "Stahl":0.5, "Fee":1},
}

SCREEN_W = 1920
SCREEN_H = 1080

MAP_WIDTH = 80
MAP_HEIGHT = 60
TILE_SIZE = 160
SPRITE_SIZE = 160

TICK_SPEED = 60

PLAYER_SPEED = 10
battle_chance = 15

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
pg.display.set_caption("Map")

font_menu = pg.font.Font("font/pixel.ttf", 26)  # Standard-Schriftart mit Größe 36
font_button = pg.font.Font("font/pixel.ttf", 18)
clock = pg.time.Clock()

#--------------------------------def draw_battle():------------------------------------
background = pg.Surface((SCREEN_W,SCREEN_H))
background.fill("White")
background_pos = (0,0)

battle = pg.image.load("graphics/assets/battle.png")
battle_pos = (0,0)

ground = pg.Surface((SCREEN_W,SCREEN_H))
ground.fill("Green")
ground_pos = (0,800)

trainer_img = trainer_img = pg.image.load("graphics/assets/player_fight.png")
trainer_pos = (200,400)

own_pkmn_pos = (850,800-SPRITE_SIZE)

enemy_pkmn_start_pos = (SCREEN_W+200,800-SPRITE_SIZE)
enemy_pkmn_end_pos = (1200,800-SPRITE_SIZE)

#--------------------------------def draw_outlines():------------------------------------
atk_window_x = 250
atk_window_y = 200
atk_window_width = 450
atk_window_height = 180
atk_window_rect = pg.Rect(atk_window_x, atk_window_y, atk_window_width, atk_window_height)

hp_bar_width = 100
hp_bar_height = 10

own_hp_bar_x = ((own_pkmn_pos[0]+SPRITE_SIZE//2)-(hp_bar_width//2))
hp_bar_y = own_pkmn_pos[1]
hp_bar_y -= 50

button_pos_x = atk_window_x + 15
button_pos_y = atk_window_y + 25
button_color = "Gray36"
#----------------------------------------------------------------------------------------------





