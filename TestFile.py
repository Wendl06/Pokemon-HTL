import json
from random import randint


def generate_unique_id():
    with open("data/savegame.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        id_blacklist = set(data["id-blacklist"])

    while True:
        unique_id = f"{randint(0, 0xFFFFF):05X}"  # Hex-Format ohne '0x'
        if unique_id not in id_blacklist:
            id_blacklist.add(unique_id)
            break

    data["id-blacklist"] = list(id_blacklist)
    with open("data/savegame.json", "w", encoding="utf-8") as file:
        json.dump(data, file)

    """
    RUN "generate_unique_id":
        id = generate_unique_id()
        print(id)
    """
    return unique_id


class Test:
    def __init__(self, par, par2):
        self.par = par
        self.par2 = par2


class Test2:
    def __init__(self, par):
        self.haha(par)

    @staticmethod
    def haha(tar):
        tar.par = 24


if __name__ == "__main__":
    modul = Test(1, 1)
    battle = Test2(modul)
    print(modul.par)
