from battle import Battle
from utilities import *
#from pokemon import *
from conf import PKN_BLUEPRINT, NPC_PATH
import random


class BattleManager():
    def __init__(self, player, team, items, battle_counter, npc, trainer_battle):
        self.player = player
        self.team = team
        self.items = items
        self.battle_counter = battle_counter
        self.npc = npc
        self.trainer_battle = trainer_battle

        self.i = 0 

        with open(PKN_BLUEPRINT, "r", encoding="utf-8") as file1:
            self.data = json.load(file1)

        with open(NPC_PATH, "r", encoding="utf-8") as file2:
            self.npc_data = json.load(file2)
        
        self.npc_pokemons = []
        #print(self.npc_data[self.npc]["pokemons"])
        
    def run(self):
        pg.mixer.music.stop()
        while self.team[self.i].current_hp <= 0:
            if self.i < len(self.team)-1:
                self.i += 1
            else: return False
        spieler_pkmn = self.team[self.i]

        #----------------------------------------------------------
        highest = 0
        lowest = 100
        for i in self.team:
            if i.level > highest: highest = i.level
            if i.level < lowest: lowest = i.level

        match self.npc:
            case "Baran": 
                if highest < 10 or self.player[5][0] == "True" or self.player[2]!=0: 
                    self.npc = None
                index = 0
            case "Hannah": 
                if highest < 20 or self.player[5][1] == "True" or self.player[2]!=1: 
                    self.npc = None
                index = 1
            case "Wendl": 
                if highest < 30 or self.player[5][2] == "True" or self.player[2]!=2: 
                    self.npc = None
                index = 2
            case "Tobi": 
                if highest < 40 or self.player[5][3] == "True" or self.player[2]!=3: 
                    self.npc = None
                index = 3
            case "Valle": 
                if highest < 50 or self.player[5][4] == "True" or self.player[2]!=4: 
                    self.npc = None
                index = 4

        if self.npc != None and self.trainer_battle:
            for i in self.npc_data[self.npc]["pokemons"]:
                self.npc_pokemons.append([i[0],i[2]])

            for pokemon in self.npc_pokemons:
                gegner = pokemon[0]
                lvl = pokemon[1]
                gegner_pkmn = load_basic_pkmn(gegner, lvl)

                if spieler_pkmn.current_hp > 0:
                    Kampf = Battle(spieler_pkmn, gegner_pkmn, self.items, self.team, True, self.npc, self.npc_data)

            if Kampf.won == True:
                PlayerPokemon.check_level_up(spieler_pkmn, self.npc_data[self.npc]["xp"]) #xp
                self.player[1]+= self.npc_data[self.npc]["money"] #Geld
                self.player[5][index] = "True"
                if self.player[2]<4:
                    self.player[2]+=1
        #----------------------------------------------------------
        elif self.npc == None and not self.trainer_battle:
            gegner = random.choice(list(self.data.keys()))
            lvl = random.randint(lowest-2,highest+2)
            lvl = max(1 ,lvl)
            lvl = min(lvl,100)

            gegner_pkmn = load_basic_pkmn(gegner, lvl)

            Kampf = Battle(spieler_pkmn, gegner_pkmn, self.items, self.team, False, None, None )
            if Kampf.is_caught():
                caught_pkmn = caught_pkn(gegner_pkmn)
                caught_pkmn.current_hp = 2*(caught_pkmn.max_hp//3)
                if len(self.team)<6:
                    self.team.append(caught_pkmn)
        #----------------------------------------------------------
            if Kampf.won == True:
                PlayerPokemon.check_level_up(spieler_pkmn,150*lvl) #xp
                self.player[1]+= 50*lvl #Geld

            
if __name__ == "__main__":
    player, team, items = load_game_saves() 
    #battleManager = BattleManager(player, team, items,0)
    cnt = 1
    while True:
        battleManager = BattleManager(player, team, items,cnt, None,None)
        battleManager.run()
        cnt+=1
