import json
import inquirer
from conf import ATK_PATH, TYPE_CHART, GAME_SAV
import conf
import pygame as pg
import random
import time

def answer_chooser(q, *args):
    question = [
        inquirer.List(
            'action',
            message=q,
            choices=args,
        ),
    ]
    return inquirer.prompt(question)


class Battle:
    def __init__(self, pkmn1, pkmn2, items, team, trainer_battle, npc, npc_data):
        self.player_pkmn = pkmn1
        self.enemy_pkmn = pkmn2
        self.items = items
        self.team = team
        self.trainer_battle = trainer_battle
        self.round_counter = 1
        
        self.won = True
        self.caught = False
        #GUI----------------------------------------------
        self.screen = conf.screen
        self.enemy_pkmn_pos_x = conf.enemy_pkmn_start_pos[0]

        self.kb_num = 0
        self.cursor = self.kb_num

        self.neutral = True
        self.click_active = False
        self.accept = False
        self.start = False
        self.bm_cnt = 1
        self.selection = None
        self.hover_color = [conf.button_color]*7 #nit hinterfragen
        
        self.font = conf.font_button
        self.status_font = pg.font.Font("font/pixel.ttf", 24)
        self.merker = 0
        self.AlleTot = False
        self.tot = False
        self.hp_liste = []

        self.atk_info = None
        self.catch_chance = 40 #grundwert

        self.npc = npc #name
        self.npc_data = npc_data #json

        self.enemy_acc_mult = 1
        self.pkmn_acc_mult = 1

        self.enemy_dmg_mult = 1
        self.pkmn_dmg_mult = 1
        #------------------------------------------------

        self.draw()
        if self.npc != None:
            self.status(f"{self.npc} fordert dich zu einem Kampf heraus!")
        self.start_battle()

#--------------------------------------------------------------------------------------
    def draw(self):
        self.screen.blit(conf.battle, conf.battle_pos)              #Hintergrund
        self.screen.blit(conf.trainer_img, conf.trainer_pos)        #Trainer
        
        if self.npc != None:
            npc = pg.image.load(self.npc_data[self.npc]["battle"])
            self.screen.blit(npc, (1200,200))
        #------------------------------------------------------------------------------
        own_pkmn_img = pg.image.load(self.player_pkmn.graphic_path)
        self.screen.blit(own_pkmn_img,conf.own_pkmn_pos)

        enemy_pkmn_img_raw = pg.image.load(self.enemy_pkmn.graphic_path)
        enemy_pkmn_img = pg.transform.flip(enemy_pkmn_img_raw, True, False)
        self.screen.blit(enemy_pkmn_img, (self.enemy_pkmn_pos_x,conf.enemy_pkmn_start_pos[1]-150))
        
        if self.enemy_pkmn_pos_x> conf.enemy_pkmn_end_pos[0]:
            self.enemy_pkmn_pos_x -= 5
        else:
            self.start = True
        #-------------------------------------------------------------------------------
        pg.draw.rect(self.screen,"White",conf.atk_window_rect, 0, 10)
        pg.draw.rect(self.screen,"Gray",conf.atk_window_rect, 2, 10)

        pg.draw.rect(self.screen,"Gray",
                     pg.Rect(conf.own_hp_bar_x,conf.hp_bar_y,conf.hp_bar_width,conf.hp_bar_height), 
                     2, conf.hp_bar_height//2)
        
        pg.draw.rect(self.screen,"Gray",
                     pg.Rect(self.enemy_pkmn_pos_x,conf.hp_bar_y-150,conf.hp_bar_width,conf.hp_bar_height),
                     2, conf.hp_bar_height//2)
        
        name = self.font.render(f"{self.player_pkmn.name}", False, "Black")
        Rname = name.get_rect(midleft=(conf.own_hp_bar_x,conf.hp_bar_y-15))
        self.screen.blit(name,Rname)

        e_name = self.font.render(f"{self.enemy_pkmn.name}", False, "Black")
        e_Rname = e_name.get_rect(midleft=(self.enemy_pkmn_pos_x,conf.hp_bar_y-165))
        self.screen.blit(e_name,e_Rname)
        
        lvl = self.font.render(f"lvl:{self.player_pkmn.level}", False, "Black")
        Rlvl = lvl.get_rect(midleft=(conf.own_hp_bar_x,conf.hp_bar_y+20))
        self.screen.blit(lvl,Rlvl)

        e_lvl = self.font.render(f"lvl:{self.enemy_pkmn.level}", False, "Black")
        e_Rlvl = lvl.get_rect(midleft=(self.enemy_pkmn_pos_x,conf.hp_bar_y-130))
        self.screen.blit(e_lvl,e_Rlvl)
        #-------------------------------------------------------------------------------
        #aktuelle leben nie höher als max leben
        self.player_pkmn.current_hp = min(self.player_pkmn.current_hp, self.player_pkmn.max_hp)
        self.enemy_pkmn.current_hp = min(self.enemy_pkmn.current_hp, self.enemy_pkmn.max_hp)

        self.player_pkmn.current_hp = max(0, self.player_pkmn.current_hp)
        self.enemy_pkmn.current_hp = max(0, self.enemy_pkmn.current_hp)

        own_hp =  (self.player_pkmn.current_hp / self.player_pkmn.max_hp)*100
        enemy_hp = (self.enemy_pkmn.current_hp / self.enemy_pkmn.max_hp)*100

        self.percent_own_hp = own_hp
        self.percent_enemy_hp = enemy_hp

        if own_hp < 0: own_hp = 0
        if enemy_hp <0: enemy_hp = 0

        if self.player_pkmn.current_hp > self.player_pkmn.max_hp//2: color = "Green"
        elif self.player_pkmn.current_hp > self.player_pkmn.max_hp//4: color = "Yellow"
        else: color = "Red"
        pg.draw.rect(self.screen,color,pg.Rect(conf.own_hp_bar_x, conf.hp_bar_y, own_hp, conf.hp_bar_height),
                     0, conf.hp_bar_height//2)
        
        if self.enemy_pkmn.current_hp > self.enemy_pkmn.max_hp//2: color = "Green"
        elif self.enemy_pkmn.current_hp > self.enemy_pkmn.max_hp//4: color = "Yellow"
        else: color = "Red"
        pg.draw.rect(self.screen,color,
                     pg.Rect(self.enemy_pkmn_pos_x, conf.hp_bar_y-150, enemy_hp, conf.hp_bar_height),
                     0, conf.hp_bar_height//2)
        
        pg.draw.rect(self.screen,"Gray",
                pg.Rect(conf.own_hp_bar_x,conf.hp_bar_y,conf.hp_bar_width,conf.hp_bar_height), 
                2, conf.hp_bar_height//2)
        
        pg.draw.rect(self.screen,"Gray",
                     pg.Rect(self.enemy_pkmn_pos_x,conf.hp_bar_y-150,conf.hp_bar_width,conf.hp_bar_height),
                     2, conf.hp_bar_height//2)
        #--------------------------------------------------------------------------------
        position = [(conf.button_pos_x, conf.button_pos_y), (conf.button_pos_x, conf.button_pos_y+30),
                    (conf.button_pos_x, conf.button_pos_y+60), (conf.button_pos_x, conf.button_pos_y+90),
                    (conf.button_pos_x, conf.button_pos_y+120)]
        text = []
        match self.bm_cnt:
            case 1:
                text = ["Kampf", "Pokemon", "Beutel", "Flucht", ""]
            case 2:
                text = [self.player_pkmn.moveset[0], self.player_pkmn.moveset[1], 
                        self.player_pkmn.moveset[2], self.player_pkmn.moveset[3], "Zurück"]
            case 3:
                position = [(conf.button_pos_x, conf.button_pos_y), (conf.button_pos_x+125, conf.button_pos_y),
                            (conf.button_pos_x, conf.button_pos_y+30), (conf.button_pos_x+125, conf.button_pos_y+30),
                            (conf.button_pos_x, conf.button_pos_y+60),(conf.button_pos_x+125, conf.button_pos_y+60),
                            (conf.button_pos_x, conf.button_pos_y+90)]
                for i in range(len(self.team)):
                    text.append(self.team[i].name)
                while len(text) < 6:
                    text.append("")
                text.append("Zurück")
                ##print("text=",text)

                self.wechseln = self.font.render(text[4], False, self.hover_color[4])
                self.rect_wechseln = self.wechseln.get_rect(midleft =position[4])
                self.screen.blit(self.wechseln, self.rect_wechseln)

                self.wechseln2 = self.font.render(text[5], False, self.hover_color[5])
                self.rect_wechseln2 = self.wechseln2.get_rect(midleft =position[5])
                self.screen.blit(self.wechseln2, self.rect_wechseln2)
            
            case 4:
                for i in self.items:
                    if i not in text:
                        text.append(i)
                while len(text) < 4:
                    text.append("")
                text.append("Zurück")
          
        self.text = text

        self.atk_button =    self.font.render(self.text[0], False, self.hover_color[0])
        self.pkmn_button =   self.font.render(self.text[1], False, self.hover_color[1])
        self.item_button =   self.font.render(self.text[2], False, self.hover_color[2])
        self.flight_button = self.font.render(self.text[3], False, self.hover_color[3])
        
        self.rect_atk_button = self.atk_button.get_rect(midleft =position[0])
        self.rect_pkmn_button = self.pkmn_button.get_rect(midleft =position[1])
        self.rect_item_button = self.item_button.get_rect(midleft =position[2])
        self.rect_flight_button = self.flight_button.get_rect(midleft =position[3])

        self.screen.blit(self.atk_button, self.rect_atk_button)
        self.screen.blit(self.pkmn_button, self.rect_pkmn_button)
        self.screen.blit(self.item_button, self.rect_item_button)
        self.screen.blit(self.flight_button, self.rect_flight_button)

        #return button
        for i in range(len(self.text)):
            if self.text[i] in ["Zurück",""]:
                if self.tot: self.text[i] = ""
                self.back_button =   self.font.render(self.text[i], False, self.hover_color[i])
                self.rect_back_button = self.back_button.get_rect(midleft =position[i])
                self.screen.blit(self.back_button, self.rect_back_button)
        #--------------------------------------------------------------------------------
        self.atk_overview()
        self.item_counter()

        pg.display.update()
        conf.clock.tick(conf.TICK_SPEED)
        #----------------------------------------------------
    def handling(self):
        mouse_pos = pg.mouse.get_pos()

        if self.neutral:
            self.hover_color = [conf.button_color] * 7

            if self.rect_atk_button.collidepoint(mouse_pos):
                self.hover_color[0] = "Yellow"

            elif self.rect_pkmn_button.collidepoint(mouse_pos):
                self.hover_color[1] = "Yellow"

            elif self.rect_item_button.collidepoint(mouse_pos):
                self.hover_color[2] = "Yellow"

            elif self.rect_flight_button.collidepoint(mouse_pos):
                self.hover_color[3] = "Yellow"

            elif self.bm_cnt in [2, 3] and self.rect_back_button.collidepoint(mouse_pos):
                self.hover_color[4] = "Yellow"

            elif self.bm_cnt == 3 and self.rect_wechseln.collidepoint(mouse_pos):
                self.hover_color[5] = "Yellow"
        #-----------------------------------------------------------------------------        
        if self.bm_cnt == 1: button_num = 4
        elif self.bm_cnt == 2 or self.bm_cnt == 4: button_num = 5
        elif self.bm_cnt == 3: button_num = 7

        if self.kb_num > button_num: self.kb_num = 0
        if self.kb_num < 0: self.kb_num = button_num

        if "" in self.text:
            self.merker = self.text.index("")-1
        else: self.merker = None

        if self.bm_cnt == 3 or self.bm_cnt == 4:
            if self.kb_num - self.cursor > 0:
                if self.kb_num != 0:
                    self.cursor = self.kb_num-1
                    if self.kb_num <= len(self.text):
                        if self.text[self.cursor]== "":
                            self.kb_num = len(self.text)
                            self.merker = self.cursor-1    
            
            elif self.kb_num - self.cursor <= 0:  
                if self.kb_num != 0:
                    self.cursor = self.kb_num -1  
                    if self.kb_num >= 1:  
                        if self.text[self.cursor] == "":  
                            self.kb_num = self.merker +1 

            else: self.cursor = self.kb_num

        selection = self.selection
        self.neutral = True
        match self.kb_num:
            case 1: 
                self.hover_color = ["Yellow", conf.button_color,conf.button_color,
                                    conf.button_color, conf.button_color, conf.button_color,
                                    conf.button_color]
                self.neutral = False
                self.atk_info = self.text[0]
                if self.accept:
                    selection = self.text[0]
            
            case 2:
                self.hover_color = [conf.button_color, "Yellow",conf.button_color,
                                    conf.button_color, conf.button_color, conf.button_color,
                                    conf.button_color]
                self.neutral = False
                self.atk_info = self.text[1]
                if self.accept:
                    selection = self.text[1]
            
            case 3:
                self.hover_color = [conf.button_color,conf.button_color, "Yellow",
                                    conf.button_color, conf.button_color, conf.button_color,
                                    conf.button_color]
                self.neutral = False
                self.atk_info = self.text[2]
                if self.accept:
                    selection = self.text[2]

            case 4:
                self.hover_color = [conf.button_color,conf.button_color,conf.button_color,
                                     "Yellow", conf.button_color, conf.button_color,
                                    conf.button_color]
                self.neutral = False
                self.atk_info = self.text[3]
                if self.accept:
                    selection = self.text[3]  

            case 5:
                self.hover_color = [conf.button_color,conf.button_color,conf.button_color,
                                     conf.button_color, "Yellow", conf.button_color,
                                    conf.button_color]
                self.neutral = False
                self.atk_info = self.text[4]
                if self.accept:
                    selection = self.text[4]
                
            case 6:
                self.hover_color = [conf.button_color,conf.button_color,conf.button_color,
                                     conf.button_color, conf.button_color, "Yellow",
                                    conf.button_color]
                self.neutral = False
                self.atk_info = self.text[5]
                if self.accept:
                    selection = self.text[5]
                
            case 7:
                self.hover_color = [conf.button_color,conf.button_color,conf.button_color,
                                    conf.button_color, conf.button_color, conf.button_color,
                                    "Yellow"]
                self.neutral = False
                self.atk_info = self.text[6]
                if self.accept:
                    selection = self.text[6]
            
        if self.accept and selection is not None:
            if selection == "Zurück":
                self.accept = False
                self.bm_cnt = 1
            return selection
#--------------------------------------------------------------------------------------------------------------------------------
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
                if event.key == pg.K_SPACE and self.click_active and not self.neutral:
                    self.accept = True
#------------------------------------------------------------------------------------------------------------------------------
    def skip_empty_buttons(self, direction, max_index):
        original = self.kb_num
        while True:
            self.kb_num += direction
            if self.kb_num > max_index:
                self.kb_num = 1  # Skip index 0 (neutral)
            elif self.kb_num < 1:
                self.kb_num = max_index

            if self.text[self.kb_num - 1] != "":
                break
            # Verhindere Endlosschleife, falls alles leer ist
            if self.kb_num == original:
                break
#------------------------------------------------------------------------------------------------------------------------------
    def status(self,status):
        """
        liste machen
        for
            liste in jedem durchlauf um 1 buchstaben erweitern
            liste in string umwandeln
            string ausgeben
            überschreiben
        """
        pos_x = (conf.SCREEN_W//3)+100
        pos_y_status = 200

        new_text = []

        self.draw()

        border = self.status_font.render(status, False, "White")
        rect_border = border.get_rect(topleft =(pos_x, pos_y_status))

        rect_background = pg.Rect(
            rect_border.left-10,
            rect_border.top,
            rect_border.width + 2 * 10,
            rect_border.height + 5
        )

        characters = list(status)
        #print(characters)
        
        for i in range(len(characters)):
            pg.draw.rect(self.screen, "White", rect_background, 0, 5)
            pg.draw.rect(self.screen, "Gray", rect_background, 2, 5)

            new_text.append(characters[i])
            string = ''.join(new_text)

            status = self.status_font.render(string, False, "Black")
            rect_status = status.get_rect(topleft =(pos_x, pos_y_status))
            self.screen.blit(status, rect_status)
            time.sleep(0.02)
            pg.display.update()

        time.sleep(0.75)
#------------------------------------------------------------------------------------------------------------------------------ 
    def update(self):
        pg.event.pump()
        self.draw()
        self.events()

        answers = self.handling()
        #self.draw() #mal schaugen ob des schoa geaht
        return answers
#-----------------------------------------------------------------------------------------------------------------------------
    def check_team_status(self):
        self.AlleTot = not any(p.current_hp > 0 for p in self.team)
#-----------------------------------------------------------------------------------------------------------------------------
    def is_caught(self):
        if self.caught and not self.trainer_battle:
            return True
#-----------------------------------------------------------------------------------------------------------------------------
    def item_counter(self):
        if not self.neutral and self.atk_info != "Zurück":         
            if self.atk_info in self.items:
                text_x = 500
                text_y = conf.button_pos_y

                cnt = self.font.render(f"{self.items.count(self.atk_info)} Stück", False, "Gray46")
                Rcnt = cnt.get_rect(midleft=(text_x,text_y ))
                self.screen.blit(cnt, Rcnt)
            
                pg.display.update()

    def atk_overview(self):
        """
        wenn kb_num = ... werd text gehighlighted -> je nach text der im button steht 
        soll aus der attacken übersicht information geladen werden die in einem eigenen fenster (weißes umrandetetes rechteck)
        """
        if not self.neutral and self.atk_info != "Zurück" and (self.atk_info != "" or ''): 
            with open(ATK_PATH, "r") as file:
                data = json.load(file)

            if self.atk_info in data.keys():
                text_x = 530
                text_y = [conf.button_pos_y,conf.button_pos_y+30,conf.button_pos_y+60]

                #info_rect = pg.Rect(info_x, info_y, 150,200)
                #pg.draw.rect(self.screen, "White", info_rect, 0, 5)
                #pg.draw.rect(self.screen, "Gray", info_rect, 2, 5)

                dmg = self.font.render(f"Schaden: {data[self.atk_info]['damage']}", False, "Gray46")
                type = self.font.render(f"Typ: {data[self.atk_info]['type']}", False, "Gray46")
                acc = self.font.render(f"Genauigkeit: {data[self.atk_info]['accuracy']}", False, "Gray46")

                dmg_rect = dmg.get_rect(midleft = (text_x, text_y[0]))
                type_rect = type.get_rect(midleft = (text_x, text_y[1]))
                acc_rect = acc.get_rect(midleft = (text_x, text_y[2]))

                self.screen.blit(dmg, dmg_rect)
                self.screen.blit(type,type_rect)
                self.screen.blit(acc, acc_rect)

                pg.display.update()
    #----------------------------------------------------------------------------------------------------------------------------
    def check_effect(self, attack, yourturn):
        if yourturn:
            if "effect" in attack:
                match attack["effect"]:
                    case "attack_reducing": 
                        self.enemy_dmg_mult -= 0.15
                        self.status(f"Angriff des Gegeners um 15% verringert.")
                    case "accuracy_reducing": 
                        self.enemy_acc_mult -= 0.10
                        self.status(f"Genauigkeit des Gegeners um 10% verringert.")
                    case "attack_boost": 
                        self.pkmn_dmg_mult += 0.15
                        self.status(f"Angriff deines Pokemon um 15% erhöht.")
                    case "healing": 
                        self.player_pkmn.current_hp += (self.player_pkmn.max_hp//5)*self.pkmn_dmg_mult
                        self.status(f"Dein Pokemon wurde um {(self.player_pkmn.max_hp//5)*self.pkmn_dmg_mult} HP geheilt.")
                    case "steal_hp": 
                        self.enemy_pkmn.current_hp -= self.enemy_pkmn.max_hp//10
                        self.player_pkmn.current_hp += self.enemy_pkmn.max_hp//10
                        self.status(f"Dein Pokemon hat {self.enemy_pkmn.max_hp//10} HP gestohlen.")
        if not yourturn:
            if "effect" in attack:
                match attack["effect"]:
                    case "attack_reducing": 
                        self.pkmn_dmg_mult -= 0.15
                        self.status(f"Angriff deines Pokemon um 15% verringert.")
                    case "accuracy_reducing":
                        self.pkmn_acc_mult -= 0.10
                        self.status(f"Genauigkeit eines Pokemon um 10% verringert.")
                    case "attack_boost":
                        self.enemy_dmg_mult += 0.15
                        self.status(f"Angriff des Gegners um 15% erhöht.")
                    case "healing": 
                        self.enemy_pkmn.current_hp += (self.enemy_pkmn.max_hp//5)*self.enemy_dmg_mult
                        self.status(f"Gegner wurde um {(self.enemy_pkmn.max_hp//5)*self.enemy_dmg_mult} HP geheilt.")
                    case "steal_hp": 
                        self.player_pkmn.current_hp -= self.player_pkmn.max_hp//10
                        self.enemy_pkmn.current_hp += self.player_pkmn.max_hp//10
                        self.status(f"Der Gegner hat {self.player_pkmn.max_hp//10} HP gestohlen.")
    #----------------------------------------------------------------------------------------------------------------------------
    def start_battle(self):
        #print(f"Fight: {self.player_pkmn.name} vs. {self.enemy_pkmn.name}\n---------------------------------------")
        self.check_team_status()
        while not self.AlleTot and not self.caught:
            while (self.player_pkmn.current_hp > 0) and (self.enemy_pkmn.current_hp > 0):
                #time.sleep(1)
                if self.start:
                    #-----------------
                    answers = self.update()
                    #----------------
                    ##print(f"Runde {self.round_counter}:")

                    # KAMPF MENU
                    #answers = answer_chooser("Was möchtest du tun?", 'Kampf', 'Beutel', 'Pokemon', 'Flucht')
                    if answers == "Kampf" or self.bm_cnt == 2:
                        ##print("Kampf")
                        if self.bm_cnt != 2:
                            self.bm_cnt = 2
                            self.kb_num = 0
                        
                        self.fight()
                    elif answers == "Pokemon" or self.bm_cnt == 3:
                        ##print("Pokemon")
                        if self.bm_cnt != 3:
                            self.bm_cnt = 3
                            self.kb_num = 0
                        self.sw_pokemons(tot=False)
                    elif answers == "Beutel" or self.bm_cnt == 4:
                        if self.bm_cnt != 4:
                            self.bm_cnt = 4
                            self.kb_num = 0
                        ##print("Beutel")
                        self.bag()
                    elif answers == "Flucht" or self.bm_cnt == 5:
                        self.kb_num = 0
                        if self.flight():
                            return
                    
                else: 
                    self.accept = False
                    self.update()
            
            if self.enemy_pkmn.current_hp <= 0:
                break
            self.check_team_status()
            if self.AlleTot:
                break
            self.bm_cnt = 3
            self.tot = True
            self.selection = None
            self.text.pop(-1)
            self.sw_pokemons(self.tot)
        
        #print("\n")
        if self.player_pkmn.current_hp <= 0:
            self.player_pkmn.current_hp = 0
            ##print("Kampf vorbei. Dein Gegner gewinnt. SPIELERNAME wird schwarz vor Augen 🤬")
            self.status("Kampf vorbei. Dein Gegner gewinnt. Dir wird schwarz vor Augen...")
            time.sleep(0.5)
            self.won = False
        elif self.enemy_pkmn.current_hp <= 0:
            self.enemy_pkmn.current_hp = 0
            ##print("Kampf vorbei. SPIELERNAME gewinnt.")
            self.status("Kampf vorbei. Du gewinnst!")
            time.sleep(0.5)
            self.won = True

    def fight(self):
        chosen_attack = self.update()#answer_chooser("Welche Attacke möchtest du einsetzen?", *(self.player_pkmn.moveset +
                                                                                  #["Zurück"]))
        
        self.accept = False
        if chosen_attack == "Zurück":
            self.bm_cnt = 1
        if chosen_attack in self.player_pkmn.moveset:
            if self.player_pkmn.speed >= self.enemy_pkmn.speed:
                # Pokemon 1 hat Erstschlag
                attack_stats = self.get_attack(chosen_attack)
                #print(f"{self.player_pkmn.name} greift mit {chosen_attack} an")

                self.status(f"{self.player_pkmn.name} greift mit {chosen_attack} an")
                # Schaden
                type_multiplier = TYPE_CHART[attack_stats["type"]][self.enemy_pkmn.type]
                damage = round(((attack_stats["damage"] * type_multiplier * self.player_pkmn.damage)//50)*self.pkmn_dmg_mult,0)
                if attack_stats["accuracy"]*self.pkmn_acc_mult >= random.randint(1,100):
                    self.enemy_pkmn.current_hp -= damage
                    # Ausgabe
                    #print(f"{self.enemy_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.enemy_pkmn.current_hp}/"
                    #    f"{self.enemy_pkmn.max_hp}")
                
                    self.status(f"{self.enemy_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.enemy_pkmn.current_hp}/"
                        f"{self.enemy_pkmn.max_hp}")
                    
                    self.check_effect(attack_stats, yourturn=True)
                else:
                    self.status(f"{chosen_attack} verfehlt den Gegner...")

                if self.enemy_pkmn.current_hp > 0:
                    # Logik für Gegner Attacke
                    random_attack = random.choice(self.enemy_pkmn.moveset)
                    enemy_attack = self.get_attack(random_attack)
                    #print(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                    self.status(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                    # Schaden
                    type_multiplier = TYPE_CHART[enemy_attack["type"]][self.player_pkmn.type]
                    damage = round(((enemy_attack["damage"] * type_multiplier * self.enemy_pkmn.damage)//50) *self.enemy_dmg_mult,0)
                    if enemy_attack["accuracy"]*self.enemy_acc_mult >= random.randint(1,100):
                        self.player_pkmn.current_hp -= damage
                        # Ausgabe
                        #print(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                        #    f"{self.player_pkmn.max_hp}")
                        
                        self.status(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                            f"{self.player_pkmn.max_hp}")
                        
                        self.check_effect(enemy_attack, yourturn=False)
                    else:
                        self.status(f"{random_attack} verfehlt dein Pokemon...")

            else:
                # Pokemon 2 hat Erstschlag
                # Logik für Gegner Attacke
                random_attack = random.choice(self.enemy_pkmn.moveset)
                enemy_attack = self.get_attack(random_attack)
                #print(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                self.status(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                # Schaden
                type_multiplier = TYPE_CHART[enemy_attack["type"]][self.player_pkmn.type]
                damage = round(((enemy_attack["damage"] * type_multiplier * self.enemy_pkmn.damage)//50)*self.enemy_dmg_mult,0)
                if enemy_attack["accuracy"]*self.enemy_acc_mult >= random.randint(1,100):
                    self.player_pkmn.current_hp -= damage
                    # Ausgabe
                    #print(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                    #    f"{self.player_pkmn.max_hp}")
                    
                    self.status(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                        f"{self.player_pkmn.max_hp}")
                    self.check_effect(enemy_attack, yourturn=False)
                else:
                    self.status(f"{random_attack} verfehlt dein Pokemon...")

                if self.player_pkmn.current_hp > 0:
                    attack_stats = self.get_attack(chosen_attack)
                    #print(f"{self.player_pkmn.name} greift mit {chosen_attack} an")
                    self.status(f"{self.player_pkmn.name} greift mit {chosen_attack} an")
                    # Schaden
                    type_multiplier = TYPE_CHART[attack_stats["type"]][self.enemy_pkmn.type]
                    damage = round(((attack_stats["damage"] * type_multiplier * self.player_pkmn.damage)//50)*self.pkmn_dmg_mult)
                    if attack_stats["accuracy"]*self.pkmn_acc_mult >= random.randint(1,100):
                        self.enemy_pkmn.current_hp -= damage
                        # Ausgabe
                        #print(f"{self.enemy_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.enemy_pkmn.current_hp}/"
                        #    f"{self.enemy_pkmn.max_hp}")
                    
                        self.status(f"{self.enemy_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.enemy_pkmn.current_hp}/"
                            f"{self.enemy_pkmn.max_hp}")
                        self.check_effect(attack_stats, yourturn=True)
                    else:
                        self.status(f"{chosen_attack} verfehlt den Gegner...")
            self.bm_cnt = 1
            self.round_counter += 1
            self.kb_num = 0
        self.update()


    def bag(self):
        item = self.update()#answer_chooser("Nutze ein Item:", *(self.items + ["Zurück"]))

        self.accept = False
        if item == "Zurück":
            self.bm_cnt = 1

        """with open(GAME_SAV, "r") as file:
                data = json.load(file)"""

        if item in self.items:
            if item == "Trank":
                self.player_pkmn.current_hp += 50
                self.status(f"{self.player_pkmn.name} wurde um 50 HP geheilt")
                self.items.remove(item)
            elif item == "Supertrank":
                self.player_pkmn.current_hp += 100
                self.status(f"{self.player_pkmn.name} wurde um 100 HP geheilt")
                self.items.remove(item)
            elif item == "Pokeball":
                if not self.trainer_battle:
                    self.status(f"SPIELER wirft einen Pokeball.")
                    self.items.remove(item)
                    #if chance > ... random int iwas halt
                    #pokemon fangen
                    catch_probability = self.catch_chance * (1 - self.percent_enemy_hp / 100) 
                    if catch_probability >= random.randint(0,35):
                        self.status(f"{self.enemy_pkmn.name} wurde gefangen")
                        self.enemy_pkmn.current_hp = 0
                        self.caught = True
                    else:
                        self.status(f"{self.enemy_pkmn.name} ist ausgebrochen")
                else:
                    self.status(f"Sei kein Dieb!")
            #------------------------------------------------------------------------
            if not self.caught:
                random_attack = random.choice(self.enemy_pkmn.moveset)
                enemy_attack = self.get_attack(random_attack)
                ##print(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                self.status(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                # Schaden
                type_multiplier = TYPE_CHART[enemy_attack["type"]][self.player_pkmn.type]
                damage = round(((enemy_attack["damage"] * type_multiplier * self.enemy_pkmn.damage)//50)*self.enemy_dmg_mult,0)
                if enemy_attack["accuracy"]*self.enemy_acc_mult >= random.randint(1,100):
                    self.player_pkmn.current_hp -= damage
                    # Ausgabe
                    ##print(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                    #    f"{self.player_pkmn.max_hp}")
                    
                    self.status(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                        f"{self.player_pkmn.max_hp}")
                    self.check_effect(enemy_attack, yourturn=False)
                else:
                    self.status(f"{random_attack} verfehlt dein Pokemon...")
            #-------------------------------------------------------------------------
            """with open(GAME_SAV, "w") as file:
                json.dump(data,file, indent=4)"""

            self.bm_cnt = 1
            self.kb_num = 0
            self.round_counter += 1
        self.update()

    def sw_pokemons(self,tot):
        #pokemon_names = [pokemon.name for pokemon in self.team] + ["Zurück"]
        new_pokemon = self.update()#answer_chooser("Wähle ein Pokemon:", *pokemon_names)
        ##print(new_pokemon)
        self.accept = False
        if new_pokemon == "Zurück":
            self.bm_cnt = 1

        else:
            if any(p.name == new_pokemon for p in self.team):
                for pkmn in self.team:
                    #-----------------------------------------
                    """self.hp_liste.append(pkmn.current_hp)
                    if any(x > 0 for x in self.hp_liste):
                        self.AlleTot = False
                    else: self.AlleTot = True"""
                    #----------------------------------------
                    if pkmn.name == new_pokemon:
                        if pkmn != self.player_pkmn:
                            #print(pkmn.current_hp)
                            if pkmn.current_hp > 0:
                                self.player_pkmn = pkmn
                                #print(f"Neues Pokemon: {self.player_pkmn.name}")
                                self.status(f"Neues Pokemon: {self.player_pkmn.name}")
                                self.pkmn_acc_mult = 1
                                self.pkmn_dmg_mult = 1
                                #------------------------------------------------------------------
                                # Logik für Gegner Attacke
                                if not tot:
                                    random_attack = random.choice(self.enemy_pkmn.moveset)
                                    enemy_attack = self.get_attack(random_attack)
                                    #print(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                                    self.status(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                                    # Schaden
                                    type_multiplier = TYPE_CHART[enemy_attack["type"]][self.player_pkmn.type]
                                    damage = round(((enemy_attack["damage"] * type_multiplier * self.enemy_pkmn.damage)//50)*self.enemy_dmg_mult)
                                    if enemy_attack["accuracy"]*self.enemy_acc_mult >= random.randint(1,100):
                                        self.player_pkmn.current_hp -= damage
                                        # Ausgabe
                                        #print(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                                        #    f"{self.player_pkmn.max_hp}")
                                        
                                        self.status(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                                            f"{self.player_pkmn.max_hp}")
                                        self.check_effect(enemy_attack, yourturn=False)
                                    else:
                                        self.status(f"{random_attack} verfehlt dein Pokemon...")
                                else: self.tot = False
                                #------------------------------------------------------------------
                                self.bm_cnt = 1
                                self.kb_num = 0
                                self.round_counter += 1
                            else: 
                                #print(f"{pkmn.name} ist K.O.!")
                                self.status(f"{pkmn.name} ist K.O.!")

                        else:
                            if self.player_pkmn.current_hp > 0:
                                #print(f"{self.player_pkmn.name} kämpft bereits!")
                                self.status(f"{self.player_pkmn.name} kämpft bereits!")
                            else:
                                self.status(f"{self.player_pkmn.name} ist K.O.!")
            self.update()

    def flight(self):
        if self.trainer_battle:
            ##print("Du kannst nicht fliehen!")
            self.status("Du kannst nicht fliehen!")
        else:
            if random.randint(0,100)<70:
                ##print("Du bist geflohen.")
                self.status("Du bist geflohen")
                time.sleep(0.5)
                return True
            else:
                self.status("Flucht gescheitert")
                random_attack = random.choice(self.enemy_pkmn.moveset)
                enemy_attack = self.get_attack(random_attack)
                #print(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                self.status(f"{self.enemy_pkmn.name} greift mit {random_attack} an")
                # Schaden
                type_multiplier = TYPE_CHART[enemy_attack["type"]][self.player_pkmn.type]
                damage = round(((enemy_attack["damage"] * type_multiplier * self.enemy_pkmn.damage)//50)*self.enemy_dmg_mult)
                if enemy_attack["accuracy"]*self.enemy_acc_mult >= random.randint(1,100):
                    self.player_pkmn.current_hp -= damage
                    # Ausgabe
                    #print(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                    #    f"{self.player_pkmn.max_hp}")
                    
                    self.status(f"{self.player_pkmn.name} erhält {damage} Schadenspunkte. HP: {self.player_pkmn.current_hp}/"
                        f"{self.player_pkmn.max_hp}")
                    self.check_effect(enemy_attack, yourturn=False)
                else:
                    self.status(f"{random_attack} verfehlt dein Pokemon...")
                
                self.accept = False
                self.bm_cnt = 1
                self.kb_num = 0
                self.round_counter += 1
                self.update()

    @staticmethod
    def get_attack(attack_name):
        with open(ATK_PATH, "r") as file:
            data = json.load(file)

        return data[attack_name]
