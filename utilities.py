from conf import *
import json
from time import strftime
from datetime import date
from pokemon import *


# Funktion, mit der in das Log File geschrieben wird
def write_log(text):
    current_time = strftime("%H:%M.%S")
    current_date = date.today().strftime("%Y-%m-%d")

    new_content = f"{current_date} [{current_time}]: {text}\n"

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        old_content = file.read()

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        file.write(new_content + old_content)


# Lade Player Daten
def load_player():
    with open(GAME_SAV, "r", encoding="utf-8") as file:
        data = json.load(file)
        player_stats = data["player"]

    if not player_stats:
        # Player muss erstellt werden
        create_player()
        write_log("utilities.py, load_player: Spieler wurde erstellt")
    else:
        write_log("utilities.py, load_player: Spieler geladen")
        return player_stats


# Erstelle einen neuen Player/Spielstand
def create_player():
    # Hier kann man ein Create Player Fenster einfügen

    # Beispielwerte [],[]
    player_stats = ["Du", 100, 0, 8800, 5000,["False","False","False","False","False",]]
    starter = [["Bisasam","51000",5,0,110],["Glumanda","52000",5,0,100],["Shiggy","53000",5,0,120],[],[],[]]
    items = ["Trank","Supertrank","Pokeball"]*5
    items.sort()

    with open(GAME_SAV, "r", encoding="utf-8") as file:
        data = json.load(file)
        data["player"] = list(player_stats)
        data["pokemons"] = list(starter)
        data["items"] = list(items)

    with open(GAME_SAV, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        print("write")


# Speichere momentane Player Daten
def save_player(player_stats):
    with open(GAME_SAV, "r", encoding="utf-8") as file:
        data = json.load(file)
        data["player"] = list(player_stats)

    with open(GAME_SAV, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_basic_pkmn(name, level):
    with open(PKN_BLUEPRINT, "r", encoding="utf-8") as file:
        data = json.load(file)
        base_stats = data[name]

    return TemporaryPokemon(name=name, graphic_path=base_stats[0], level=level, base_type=base_stats[1],
                            max_hp=base_stats[2],
                            damage=base_stats[3], speed=base_stats[4], moveset=base_stats[5])


def load_player_pkmn(pos):
    with open(GAME_SAV, "r", encoding="utf-8") as file:
        save_content = json.load(file)
    team = save_content["pokemons"]
    pkmn_unique_stats = team[pos]

    if not pkmn_unique_stats:
        return []

    with open(PKN_BLUEPRINT, "r") as file:
        blueprint_content = json.load(file)
    pkmn_base_stats = blueprint_content[pkmn_unique_stats[0]]

    return PlayerPokemon(name=pkmn_unique_stats[0], pkn_id=pkmn_unique_stats[1], graphic_path=pkmn_base_stats[0],
                         level=pkmn_unique_stats[2], base_type=pkmn_base_stats[1], current_xp=pkmn_unique_stats[3],
                         current_hp=pkmn_unique_stats[4], max_hp=pkmn_base_stats[2], damage=pkmn_base_stats[3],
                         speed=pkmn_base_stats[4], moveset=pkmn_base_stats[5])


def load_team():
    team = []
    for i in range(0, 6):
        if not load_player_pkmn(i):
            pass
        else:
            team.append(load_player_pkmn(i))

    return team


def load_items():
    with open(GAME_SAV, "r") as file:
        data = json.load(file)

    return data["items"]


def load_game_saves():
    player_stats = load_player()            # Bsp.: ['Spieler', 100, 0]
    player_team = load_team()               # Bsp.: [<pokemon.PlayerPokemon object at 0x00000219EC817790>,
                                            # <pokemon.PlayerPokemon object at 0x00000219EC817390>, [], [], [], []]
    player_items = load_items()             # Bsp.: ['Trank', 'Supertrank', 'Pokeball']

    return player_stats, player_team, player_items


def save_game(player_stats, player_team, player_items):
    with open(GAME_SAV, "r") as file:
        data = json.load(file)

    # Speichere Spielerdaten
    data["player"] = player_stats

    # Speicher Spieler Pokemon
    team_length = len(player_team)
    empty_elements = 6 - team_length
    team_saves = []
    for i in range(team_length):
        team_saves.append([player_team[i].name, player_team[i].pkn_id, player_team[i].level, player_team[i].current_xp,
                          player_team[i].current_hp])

    for j in range(empty_elements):
        team_saves.append([])

    data["pokemons"] = team_saves

    # Speichere Spieleritems
    data["items"] = data["items"]

    with open(GAME_SAV, "w") as file:
        json.dump(data, file, indent=4)


# Generiert eine einzigartige ID für jedes Pokemon, welches man besitzt
def generate_unique_id():
    with open(GAME_SAV, "r", encoding="utf-8") as file:
        data = json.load(file)
        id_blacklist = set(data["id-blacklist"])

    while True:
        unique_id = f"{randint(0, 0xFFFFF):05X}"  # Hex-Format ohne '0x'
        if unique_id not in id_blacklist:
            id_blacklist.add(unique_id)
            break

    data["id-blacklist"] = list(id_blacklist)
    with open(GAME_SAV, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

        return unique_id


def caught_pkn(default_pkn):
    stats = default_pkn.stats()         # Bsp.: ('Glumanda', 'Pfad', 3, 'Feuer', 103, 103, 41, 2, ['Kratzer', 'Heuler'])
    pkn_id = generate_unique_id()

    return PlayerPokemon(name=stats[0], pkn_id=pkn_id, graphic_path=stats[1], level=stats[2], base_type=stats[3],
                         current_xp=0, current_hp=stats[4], max_hp=stats[5], damage=stats[6], speed=stats[7],
                         moveset=stats[8])


if __name__ == "__main__":
    # print(load_basic_pkmn("Bisasam", 2))
    # print(load_player_pkmn(1))
    # print(load_team())
    print(load_items())
    # print(load_player())
