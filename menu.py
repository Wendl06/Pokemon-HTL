import pygame as pg
import conf                  
from utilities import create_player,load_game_saves, save_game
import json
#---------------------------------------------------------------------------------
#Bildschirm der als erstes beim Starten des Spiels kommt
#---------------------------------------------------------------------------------
class Startbildschirm():
    def __init__(self):
        self.screen = conf.screen
        self.color = conf.button_color
        self.font = conf.font_menu

        self.button_number = 2
        self.hover_color = [self.color]*self.button_number
        self.neutral = True
        self.running = True
        self.kb_num = 0
        self.click_active = False
        self.accept = False

        self.draw()

    def draw(self):
        pos_x = 1350
        pos_y = [500,580]

        self.screen.blit(pg.image.load("graphics/assets/test.png"), (0,0))
        
        self.new_game = self.font.render("Starte Neues Spiel", False, self.hover_color[0])
        self.load_game = self.font.render("Lade bestehendes Spiel", False, self.hover_color[1])

        self.rect_ng = self.new_game.get_rect(center = (pos_x, pos_y[0]))
        self.rect_lg = self.load_game.get_rect(center = (pos_x, pos_y[1]))

        self.screen.blit(self.new_game, self.rect_ng)
        self.screen.blit(self.load_game, self.rect_lg)

    def handling(self):
        #------------------------------------------------------------
        if self.kb_num > self.button_number: self.kb_num = 0
        elif self.kb_num < 0: self.kb_num = self.button_number

        cursor = self.kb_num-1

        match self.kb_num:
            case 0:
                self.neutral = True
            case 1:
                self.hover_color[cursor] = "Yellow"
                if self.accept:
                    self.accept = False
                    create_player()
                    self.running = False
                    return

            case 2:
                self.hover_color[cursor] = "Yellow"
                if self.accept:
                    self.accept = False
                    self.running = False
                    return

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_UP or pg.K_SPACE and not self.click_active:
                    self.click_active = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN and self.click_active:
                    self.kb_num += 1
                    self.click_active = False
                if event.key == pg.K_UP and self.click_active:
                    self.kb_num -= 1
                    self.click_active = False
                if event.key == pg.K_SPACE and self.click_active:
                    self.accept = True

    def update(self):
        pg.event.pump()
        self.draw()
        self.events()
        self.handling()
        pg.display.update()

    def run(self):
        while self.running:
            self.update()
#---------------------------------------------------------------------------------
#MÜbermenü wenn man 'I' drückt
#---------------------------------------------------------------------------------
class Menu():
    def __init__(self,player,team,items):
        self.screen = conf.screen
        self.color = conf.button_color
        self.font = conf.font_menu

        self.running = True
        self.accept = False
        self.neutral = True
        self.click_active = False
        self.heal = False
        self.kb_num = 0
        self.button_number = 2
        self.hover_color = [self.color] * self.button_number

        self.team = team
        self.player = player
        self.items = items

        self.draw()

    def draw(self):
        pg.draw.rect(self.screen, "White", pg.Rect(conf.SCREEN_W- conf.SCREEN_W//4, 200, 
                        conf.SCREEN_W//4-250, conf.SCREEN_H-400), 0, 50 )

        pg.draw.rect(self.screen, "Gray36", pg.Rect(conf.SCREEN_W- conf.SCREEN_W//4, 200, 
                        conf.SCREEN_W//4-250, conf.SCREEN_H-400), 5, 50 )
        
        pos_x = conf.SCREEN_W-conf.SCREEN_W//4+35
        pos_y = conf.SCREEN_H//4

        self.SnE = self.font.render("Save & Exit",False, self.hover_color[0])
        self.SnE_rect = self.SnE.get_rect(midleft = (pos_x,pos_y))

        self.Pkmn_button = self.font.render("Pokemon", False, self.hover_color[1])
        self.Pkmn_button_rect = self.Pkmn_button.get_rect(midleft = (pos_x, pos_y + 50)) 

        self.screen.blit(self.SnE, self.SnE_rect)
        self.screen.blit(self.Pkmn_button, self.Pkmn_button_rect)

        money = self.font.render(f"Geld: {self.player[1]}€", False, "Gray46")
        Rmoney = money.get_rect(midleft=(pos_x,pos_y+500))
        self.screen.blit(money, Rmoney)

        badges = self.font.render(f"Orden: {self.player[2]}/4", False, "Gray46")
        Rbadges = badges.get_rect(midleft=(pos_x,pos_y+550))
        self.screen.blit(badges,Rbadges)
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()

                if event.key == pg.K_o:
                    self.running = False

            if event.type == pg.KEYDOWN:
                self.click_active = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN and self.click_active:
                    self.kb_num += 1
                    self.click_active = False
                if event.key == pg.K_UP and self.click_active:
                    self.kb_num -= 1
                    self.click_active = False
                if event.key == pg.K_SPACE and self.click_active and self.neutral == False:
                    self.accept = True
                
                    
    def handling(self):
        self.hover_color = [conf.button_color] * 7

        if self.kb_num > self.button_number: self.kb_num = 0
        elif self.kb_num < 0: self.kb_num = self.button_number

        cursor = self.kb_num-1
        match self.kb_num:
            case 0:
                self.neutral = True
            case 1:
                self.hover_color[cursor] = "Yellow"
                self.neutral = False
                if self.accept:
                    save_game(self.player, self.team, self.items,)
                    pg.quit()
                    self.accept = False

            case 2:
                self.hover_color[cursor] = "Yellow"
                self.neutral = False
                if self.accept:
                    self.accept = False
                    sw_pkmn = Inv(self.team,self.items)
                    sw_pkmn.run()
                    self.team = sw_pkmn.output().copy()
                    self.running = False

    def new_team(self):
        return self.team

    def update(self):
        pg.event.pump()
        self.draw()
        self.events()
        self.handling()
        pg.display.update()

    def run(self):
        while self.running:
            self.update()
#---------------------------------------------------------------------------------
#Pokemon außerhalb des Kampfes wechseln
#---------------------------------------------------------------------------------
class Inv():
    def __init__(self,team,items):
        self.screen = conf.screen
        self.color = conf.button_color
        self.font = conf.font_menu
        
        self.hover_color = [self.color]*6

        self.running = True
        self.neutral = True
        self.click_active = False
        self.accept = False
        self.heal = False
        self.kb_num = 0

        self.selection = []
        self.selection_cnt = 0
        self.remove = False

        self.team = team
        self.items = items
        self.item_cnt = items.count("Trank")

        self.names = []

        for i in self.team: 
            self.names.append(i.name)

        while len(self.names)<6: self.names.append("")
        try:
            self.button_number = self.names.index("")
        except: self.button_number = 6
        self.draw()

    def draw(self):
        pg.draw.rect(self.screen, "White", pg.Rect(conf.SCREEN_W- conf.SCREEN_W//3, 200, 
                        conf.SCREEN_W//3-250, conf.SCREEN_H-400), 0, 50 )

        pg.draw.rect(self.screen, "Gray36", pg.Rect(conf.SCREEN_W- conf.SCREEN_W//3, 200, 
                        conf.SCREEN_W//3-250, conf.SCREEN_H-400), 5, 50 )
        
        pos_x = conf.SCREEN_W-conf.SCREEN_W//3+35
        pos_y = conf.SCREEN_H//4
        self.pos_x = pos_x
        self.pos_y = pos_y
        #----------------------------------------------
        self.pkmn1 = self.font.render(self.names[0],False, self.hover_color[0])
        self.pkmn2 = self.font.render(self.names[1],False, self.hover_color[1])
        self.pkmn3 = self.font.render(self.names[2],False, self.hover_color[2])
        self.pkmn4 = self.font.render(self.names[3],False, self.hover_color[3])
        self.pkmn5 = self.font.render(self.names[4],False, self.hover_color[4])
        self.pkmn6 = self.font.render(self.names[5],False, self.hover_color[5])

        self.Rpkmn1 = self.pkmn1.get_rect(midleft = (pos_x,pos_y    ))
        self.Rpkmn2 = self.pkmn2.get_rect(midleft = (pos_x,pos_y+50 ))
        self.Rpkmn3 = self.pkmn3.get_rect(midleft = (pos_x,pos_y+100))
        self.Rpkmn4 = self.pkmn4.get_rect(midleft = (pos_x,pos_y+150))
        self.Rpkmn5 = self.pkmn5.get_rect(midleft = (pos_x,pos_y+200))
        self.Rpkmn6 = self.pkmn6.get_rect(midleft = (pos_x,pos_y+250))
        
        self.screen.blit(self.pkmn1, self.Rpkmn1)
        self.screen.blit(self.pkmn2, self.Rpkmn2)
        self.screen.blit(self.pkmn3, self.Rpkmn3)
        self.screen.blit(self.pkmn4, self.Rpkmn4)
        self.screen.blit(self.pkmn5, self.Rpkmn5)
        self.screen.blit(self.pkmn6, self.Rpkmn6)
        #----------------------------------------------
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()

                if event.key == pg.K_o:
                    self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_UP or pg.K_SPACE and not self.click_active:
                    self.click_active = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN and self.click_active:
                    self.kb_num += 1
                    self.click_active = False
                if event.key == pg.K_UP and self.click_active:
                    self.kb_num -= 1
                    self.click_active = False
                if event.key == pg.K_SPACE and self.click_active and self.neutral == False:
                    self.accept = True
                if event.key == pg.K_h and self.click_active and not self.neutral:
                    self.heal = True

                if event.key == pg.K_x and self.click_active and not self.neutral:
                    self.remove = True      
        
    def handling(self):
        self.hover_color = [conf.button_color] * 7
        if self.kb_num > self.button_number: self.kb_num = 0
        elif self.kb_num < 0: self.kb_num = self.button_number

        cursor = self.kb_num-1

        if cursor != -1:
            self.hover_color[cursor] = "Yellow"
            self.neutral = False

            if self.accept and cursor not in self.selection:
                self.selection.append(cursor)
                self.selection_cnt +=1
                self.accept = False

            if self.remove and cursor-1>=0:
                self.team.remove(self.team[cursor])

                self.names = []
                for i in self.team:
                    self.names.append(i.name)
                while len(self.names) < 6:
                    self.names.append("")
                try:
                    self.button_number = self.names.index("")
                except: self.button_number = 6

                self.remove = False
                cursor = cursor-1
                self.kb_num = 0

            if self.heal and self.item_cnt > 0:                
                with open(conf.GAME_SAV, "r") as file:
                    data = json.load(file)
                if "Trank" in data["items"]:
                    self.team[cursor].current_hp += 50
                    self.team[cursor].current_hp = min(self.team[cursor].current_hp, self.team[cursor].max_hp)
                    data["items"].remove("Trank")
                else: self.item_cnt =0
                with open(conf.GAME_SAV, "w") as file:
                    json.dump(data,file, indent=4)

                self.item_cnt -= 1
                self.heal = False

            self.hp = self.font.render(f"HP:{self.team[cursor].current_hp}/{self.team[cursor].max_hp}", False, "Gray46")
            self.Rhp = self.hp.get_rect(midleft = (self.pos_x,self.pos_y+400))
            self.screen.blit(self.hp, self.Rhp)

            level = self.font.render(f"Lvl:{self.team[cursor].level}",False, "Gray46")
            Rlevel = level.get_rect(midleft = (self.pos_x,self.pos_y+450))
            self.screen.blit(level,Rlevel)

            xp = self.font.render(f"XP:{self.team[cursor].current_xp}/{self.team[cursor].xp_cap}",False, "Gray46")
            Rxp = xp.get_rect(midleft = (self.pos_x,self.pos_y+500))
            self.screen.blit(xp,Rxp)

            self.accept = False

        else:
            self.hover_color = [conf.button_color] * 7 
            self.neutral = True
        
        if self.selection_cnt >=2:
            self.switch(self.selection)
 
    def switch(self, selection):

        objekt_dict = {}
        index = 1  

        for obj in self.team:
            objekt_dict[index] = obj
            index += 1

        idx1, idx2 = selection[0]+1,selection[1]+1
        objekt_dict[idx1], objekt_dict[idx2] = objekt_dict[idx2], objekt_dict[idx1]

        self.team = list(objekt_dict.values())

        self.names = []
        for i in self.team:
            self.names.append(i.name)
        while len(self.names) < 6:
            self.names.append("")
        try:
            self.button_number = self.names.index("")
        except: self.button_number = 6

        self.selection_cnt = 0
        self.selection = []
    
    def output(self):
        return self.team
            
    def update(self):
        pg.event.pump()
        self.draw()
        self.events()
        self.handling()
        
        pg.display.update()

    def run(self):
        while self.running:
            self.update()


if __name__ == "__main__":
    player, team, items = load_game_saves() 
    start = Startbildschirm()
    start.run()