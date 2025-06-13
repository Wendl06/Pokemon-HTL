import pygame as pg


TILE_SIZE = 160
MAP_WIDTH = 80
MAP_HEIGHT = 60
IMAGE_SIZE = MAP_HEIGHT * MAP_WIDTH

#Testzwecke
Colors = {
    "grass": (34, 139, 34),   # Grün
    "path": (210, 180, 140),  # Heller Braunton (Sandstein)
    "tree": (0, 100, 0),      # Dunkelgrün für den Baum
    "sand": (237, 201, 175),  # Sandfarbe
    "water": (0, 105, 148),   # Tiefes Blau für Wasser
    "stone": (112, 99, 77),   # Grau-Braun (erdiger Stein)
    "bush": (50, 170, 50)     # Helleres, aber dunkleres Grün als Gras
}

final = pg.Surface((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))


grass = pg.image.load("graphics/assets/Ground.png")
grass = pg.transform.scale(grass, (TILE_SIZE, TILE_SIZE))

#------------------------------------------------------------------------
path1 = pg.image.load("graphics/assets/Path_straight.png")
path1 = pg.transform.scale(path1, (TILE_SIZE, TILE_SIZE))

path2 = pg.image.load("graphics/assets/Path_straight_right.png")
path2 = pg.transform.scale(path2, (TILE_SIZE, TILE_SIZE))

path3 = pg.image.load("graphics/assets/Path_up.png")
path3 = pg.transform.scale(path3, (TILE_SIZE, TILE_SIZE))

path4 = pg.image.load("graphics/assets/Path_down.png")
path4 = pg.transform.scale(path4, (TILE_SIZE, TILE_SIZE))

#---------------------------------------------------------------------------

path5 = pg.image.load("graphics/assets/Path_corner.png")
path5 = pg.transform.scale(path5, (TILE_SIZE, TILE_SIZE))

path6 = pg.image.load("graphics/assets/Path_corner_right.png")
path6 = pg.transform.scale(path6, (TILE_SIZE, TILE_SIZE))

path7 = pg.image.load("graphics/assets/Path_corner_down.png")
path7 = pg.transform.scale(path7, (TILE_SIZE, TILE_SIZE))

path8 = pg.image.load("graphics/assets/Path_corner_right_down.png")
path8 = pg.transform.scale(path8, (TILE_SIZE, TILE_SIZE))

#---------------------------------------------------------------------------
path9 = pg.image.load("graphics/assets/Path_inner_corner.png")
path9 = pg.transform.scale(path9, (TILE_SIZE, TILE_SIZE))

path10 = pg.image.load("graphics/assets/Path_inner_corner_right.png")
path10 = pg.transform.scale(path10, (TILE_SIZE, TILE_SIZE))

path11 = pg.image.load("graphics/assets/Path_inner_corner_down.png")
path11 = pg.transform.scale(path11, (TILE_SIZE, TILE_SIZE))

path12 = pg.image.load("graphics/assets/Path_inner_corner_right_down.png")
path12 = pg.transform.scale(path12, (TILE_SIZE, TILE_SIZE))
#--------------------------------------------------------------------------

path13 = pg.image.load("graphics/assets/path_plain.png")
path13 = pg.transform.scale(path13, (TILE_SIZE, TILE_SIZE))

#--------------------------------------------------------------------------

tree1 = pg.image.load("graphics/assets/baum_gross_1.png")
tree1 = pg.transform.scale(tree1, (TILE_SIZE, TILE_SIZE))

tree2 = pg.image.load("graphics/assets/baum_gross_2.png")
tree2 = pg.transform.scale(tree2, (TILE_SIZE, TILE_SIZE))

tree3 = pg.image.load("graphics/assets/baum_gross_3.png")
tree3 = pg.transform.scale(tree3, (TILE_SIZE, TILE_SIZE))

tree4 = pg.image.load("graphics/assets/baum_gross_4.png")
tree4 = pg.transform.scale(tree4, (TILE_SIZE, TILE_SIZE))

#--------------------------------------------------------------------------

ufer_straight = pg.image.load("graphics/assets/22.png")
ufer_straight = pg.transform.scale(ufer_straight, (TILE_SIZE, TILE_SIZE))

ufer_straight1 = pg.image.load("graphics/assets/23.png")
ufer_straight1 = pg.transform.scale(ufer_straight1, (TILE_SIZE, TILE_SIZE))

ufer_straight2 = pg.image.load("graphics/assets/24.png")
ufer_straight2 = pg.transform.scale(ufer_straight2, (TILE_SIZE, TILE_SIZE))

ufer_straight3 = pg.image.load("graphics/assets/25.png")
ufer_straight3 = pg.transform.scale(ufer_straight3, (TILE_SIZE, TILE_SIZE))

# -------------------------------------------------------------------------------------

ufer_ecke = pg.image.load("graphics/assets/Ufer_ecke.png")
ufer_ecke = pg.transform.scale(ufer_ecke, (TILE_SIZE, TILE_SIZE))

ufer_corner = pg.image.load("graphics/assets/Ufer_corner.png")
ufer_corner = pg.transform.scale(ufer_corner, (TILE_SIZE, TILE_SIZE))

#---------------------------------------------------------------------------

water = pg.image.load("graphics/assets/Wasser.png")
water = pg.transform.scale(water, (TILE_SIZE, TILE_SIZE))

stone = pg.image.load("graphics/assets/Stein_grass.png")
stone = pg.transform.scale(stone, (TILE_SIZE, TILE_SIZE))

bush = pg.image.load("graphics/assets/Busch_klein.png")
bush = pg.transform.scale(bush, (TILE_SIZE, TILE_SIZE))

# -----------------------------------------------------------------------------
House1 = pg.image.load("graphics/assets/House1.png")
House1 = pg.transform.scale(House1, (TILE_SIZE, TILE_SIZE))

House2 = pg.image.load("graphics/assets/House2.png")
House2 = pg.transform.scale(House2, (TILE_SIZE, TILE_SIZE))

House3 = pg.image.load("graphics/assets/House3.png")
House3 = pg.transform.scale(House3, (TILE_SIZE, TILE_SIZE))

House4 = pg.image.load("graphics/assets/House4.png")
House4 = pg.transform.scale(House4, (TILE_SIZE, TILE_SIZE))

House5 = pg.image.load("graphics/assets/House5.png")
House5 = pg.transform.scale(House5, (TILE_SIZE, TILE_SIZE))

House6 = pg.image.load("graphics/assets/House6.png")
House6 = pg.transform.scale(House6, (TILE_SIZE, TILE_SIZE))

House7 = pg.image.load("graphics/assets/House7.png")
House7 = pg.transform.scale(House7, (TILE_SIZE, TILE_SIZE))

House8 = pg.image.load("graphics/assets/House8.png")
House8 = pg.transform.scale(House8, (TILE_SIZE, TILE_SIZE))

House9 = pg.image.load("graphics/assets/House9.png")
House9 = pg.transform.scale(House9, (TILE_SIZE, TILE_SIZE))



