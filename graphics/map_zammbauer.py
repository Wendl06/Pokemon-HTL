"""
Wichtig isch, dass die Zahlen im match case mit die Zahlen in da Excel-Datei zammpassen

sinsch isch des eigentlich relativ freestyle
"""

import pygame as pg
import csv
#from graphics import map_setup
import graphics.map_setup as map_setup

with open("graphics/csv/Map.CSV", mode='r') as file:
    data = csv.reader(file,delimiter=';')

    row_cnt = 0

    size = map_setup.TILE_SIZE #160pixel

    action_rect = []
    barrier_rect = []
    battle_rect = []

    for row in data:
        item_cnt = 0
        for item in row:
            match int(item):
                case 1: #Gras
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                #-----------------------------------------------------------------------------------
                case 2: #Path straight left
                    map_setup.final.blit(map_setup.path1, (size * item_cnt, size * row_cnt))
                case 3: #Path straight right
                    map_setup.final.blit(map_setup.path2, (size * item_cnt, size * row_cnt))
                case 4: #Path corner left
                    map_setup.final.blit(map_setup.path3, (size * item_cnt, size * row_cnt))
                case 5: #Path corner right
                    map_setup.final.blit(map_setup.path4, (size * item_cnt, size * row_cnt))
                case 6: #Path corner left down
                    map_setup.final.blit(map_setup.path5, (size * item_cnt, size * row_cnt))
                case 7: #Path corner right down
                    map_setup.final.blit(map_setup.path6, (size * item_cnt, size * row_cnt))
                case 8: #Path corner right down
                    map_setup.final.blit(map_setup.path7, (size * item_cnt, size * row_cnt))
                case 9: #Path corner right down
                    map_setup.final.blit(map_setup.path8, (size * item_cnt, size * row_cnt))
                case 10: #Path corner right down
                    map_setup.final.blit(map_setup.path9, (size * item_cnt, size * row_cnt))
                case 11: #Path corner right down
                    map_setup.final.blit(map_setup.path10, (size * item_cnt, size * row_cnt))
                case 12: #Path corner right down
                    map_setup.final.blit(map_setup.path11, (size * item_cnt, size * row_cnt))
                case 13: #Path corner right down
                    map_setup.final.blit(map_setup.path12, (size * item_cnt, size * row_cnt))
                case 14: #Path corner right down
                    map_setup.final.blit(map_setup.path13, (size * item_cnt, size * row_cnt))
                #------------------------------------------------------------------------------------
                case 15: #Baum 
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.tree1, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 16: #Baum 
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.tree2, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 17: #Baum 
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.tree3, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 18: #Baum 
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.tree4, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                #------------------------------------------------------------------------------------
                case 19: #Busch
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.bush, (size * item_cnt, size * row_cnt))
                    battle_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                #-----------------------------------------------------------------------------------
                case 20: #Stein
                    map_setup.final.blit(map_setup.stone, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                #-----------------------------------------------------------------------------------
                case 21: #Wasser
                    map_setup.final.blit(map_setup.water, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                #----------------------------------------------------------------------------------
                case 22: #Ufer 
                    map_setup.final.blit(map_setup.ufer_straight, (size * item_cnt, size * row_cnt))
                case 23: #Ufer right
                    map_setup.final.blit(map_setup.ufer_straight1, (size * item_cnt, size * row_cnt))
                case 24: #Ufer down
                    map_setup.final.blit(map_setup.ufer_straight2, (size * item_cnt, size * row_cnt))
                case 25: #Ufer up
                    map_setup.final.blit(map_setup.ufer_straight3, (size * item_cnt, size * row_cnt))

                case 26: #Ufer ecke außen
                    map_setup.final.blit(map_setup.ufer_ecke, (size * item_cnt, size * row_cnt))
                case 27: #Ufer ecke right
                    ufer_ecke_right = pg.transform.flip(map_setup.ufer_ecke, True, False)
                    map_setup.final.blit(ufer_ecke_right, (size * item_cnt, size * row_cnt))
                case 28: #Ufer 
                    ufer_ecke_down = pg.transform.flip(map_setup.ufer_ecke, False, True)
                    map_setup.final.blit(ufer_ecke_down, (size * item_cnt, size * row_cnt))
                case 29: #Ufer 
                    ufer_ecke_right_down = pg.transform.flip(map_setup.ufer_ecke, True, True)
                    map_setup.final.blit(ufer_ecke_right_down, (size * item_cnt, size * row_cnt))

                case 30: #Ufer 
                    map_setup.final.blit(map_setup.ufer_corner, (size * item_cnt, size * row_cnt))
                case 31: #Ufer 
                    ufer_corner_right = pg.transform.flip(map_setup.ufer_corner, True, False)
                    map_setup.final.blit(ufer_corner_right, (size * item_cnt, size * row_cnt))
                case 32: #Ufer 
                    ufer_corner_down = pg.transform.flip(map_setup.ufer_corner, False, True)
                    map_setup.final.blit(ufer_corner_down, (size * item_cnt, size * row_cnt))
                case 33: #Ufer 
                    ufer_corner_right_down = pg.transform.flip(map_setup.ufer_corner, True, True)
                    map_setup.final.blit(ufer_corner_right_down, (size * item_cnt, size * row_cnt))
                #------------------------------------------------------------------------------------------------
                case 34: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House1, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 35: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House2, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 36: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House3, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 37: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House4, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 38: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House5, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 39: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House6, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 40: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House7, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 41: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House8, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                case 42: #House
                    map_setup.final.blit(map_setup.grass, (size * item_cnt, size * row_cnt))
                    map_setup.final.blit(map_setup.House9, (size * item_cnt, size * row_cnt))
                    barrier_rect.append(pg.Rect(size * item_cnt, size * row_cnt, size, size))
                
                
                case _: 
                    pass

            item_cnt+=1
        row_cnt+=1
        
#print(barrier_rect)
#pg.image.save(map_setup.final,"Map.png")
#pg.quit()
