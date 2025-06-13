#from battle import Battle
from utilities import *
from conf import PKN_BLUEPRINT, ATK_PATH, GAME_SAV, NPC_PATH
import random


"""
zähler = 1
x = zähler-1
while x < len(text):
    if text[x] == "":
        x = len(text)-1
    print(text[x])
    x+=1
print(len(text))"""

if __name__ == "__main__":

    player, team, items = load_game_saves() 
    #print(team)


    x = 11.92
    print(round(x,0))

    print(player)


    for i in team:
        print(i.level)

    with open(NPC_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    #print(data)
    x = "Wendl"
    pokemons = []
    print(data[x]["pokemons"])

    for i in data[x]["pokemons"]:
        pokemons.append([i[0],i[2]])

    print(pokemons)
    hallo = {
        "a" : (1,2),
        "b" : (2,3),
        "c" : (3,4),
        "d" : (4,5)
    }
    #print(hallo["a"])


    #print(player[0])
    #print(team)

    #print(player)

    #print(items.count("Trank")+items.count("Supertrank"))

    """hallo = ["Trank","Supertrank","Pokeball"]*5
    hallo.sort()
    print(hallo)"""

    """text = ["Hallo", "Griasdi", "Pfiatdi", "", "", "Tschüss"]
    print(text.pop(-1))
    print(text)"""

    #print(team.remove(2))
    """items2 = []

    for i in items:
        for j in range(10):
            items2.append(i)
    print(items2)"""

    #items.remove("Pokeball")

    """ausschluss = []

    for i in items:
        if i not in ausschluss:
            print(items.count(i))
            ausschluss.append(i)
    print(items.count("Pokeball"))"""

    """names = []

    objekt_dict = {}
    index = 1  # Startindex bei 1

    for obj in team:
        objekt_dict[index] = obj
        index += 1
    
    print(objekt_dict)

    idx1, idx2 = 1, 3
    objekt_dict[idx1], objekt_dict[idx2] = objekt_dict[idx2], objekt_dict[idx1]

    team = list(objekt_dict.values())
    for i in team:
        print(i.name)"""

    """    for i in team:
        names.append(i.name)
        print(i.name)

    print(names)
    selection = ["Glumanda","Bisasam"]
    
    index = []
    cnt = 0
    for i in team:
        if i.name == selection[0] or i.name == selection[1]:
            index.append(cnt)
        cnt +=1 
    print(index)

    temp_team = team.copy()
    temp_team[index[0]] = team[index[1]]
    temp_team[index[1]] = team[index[0]]

    team = temp_team.copy()
    for i in team: 
        print(i.name)"""





    
"""    #temp_team = []

    #temp_team.append(team[1])
    #print(temp_team[0].name)
    #print(team[0].moveset)

    text = []
    for i in range(len(items)):
        text.append(items[i])
    while len(text) < 4:
        text.append("")
    text.append("Zurück")

    #print(text)

    with open(PKN_BLUEPRINT, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    with open(ATK_PATH, "r", encoding="utf-8") as atks:
        atk_list = json.load(atks)

    with open(GAME_SAV, "r", encoding="utf-8") as file_items:
        item_list = json.load(file_items)

    #print(atk_list)
    sx = item_list["items"]
    print(x)
    i = 12
    x = f"Hallo {i}."

    splitted = list(x)
    #print(splitted)

    joined = "".join(splitted)
    #print(joined)
    
    
    i = 0
    while False:
        if team[i].current_hp > 0:
            spieler = team[i]
        else:
            i += 1
            spieler = team[i]
        gegner = random.choice(list(data.keys()))
        lvl = random.randint(1,10)
        gegner = load_basic_pkmn(gegner, lvl)
        
        Kampf = Battle(spieler, gegner, items, team, False)

    # player[0] = "Heinrich"

    # Bisasam.pkn_id = "51000"
    # Bisasam.level = 6

    # team.append(Bisasam)

    # save_game(player, team, items)
"""