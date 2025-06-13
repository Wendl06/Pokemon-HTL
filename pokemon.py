from math import floor
from random import randint
import json
from conf import *


class PlayerPokemon:
    def __init__(self, name, pkn_id, graphic_path, level, base_type, current_xp, current_hp, max_hp, damage,
                 speed, moveset):
        # Base Stats
        self.name: str = name
        self.pkn_id: str = pkn_id
        self.graphic_path: str = graphic_path
        self.level: int = level
        self.type: str = base_type
        self.current_xp: int = current_xp
        self.xp_cap: int = BASE_XP_VALUE
        self.current_hp: int = current_hp
        self.max_hp: int = max_hp
        self.damage: int = damage
        self.speed: int = speed
        self.moveset: list = moveset

        # Current Stats
        self.set_base_stats()
    """
    def __repr__(self):
        return (f"{self.name} - ID: {self.pkn_id}, Path: {self.graphic_path}, Level: {self.level}, Type: {self.type}, "
                f"Current XP: {self.current_xp}, XP Cap: {self.xp_cap}, Current HP: {self.current_hp}, Max HP: "
                f"{self.max_hp}, Damage: {self.damage}, Speed: {self.speed}, Moveset: {self.moveset}")
                """

    # Prüft, ob Pokemon neues Level erreicht hat, falls ja wird Level UP gemacht
    def check_level_up(self, gained_xp):
        while (self.current_xp + gained_xp) >= self.xp_cap:
            self.level += 1
            if (self.current_xp + gained_xp) > self.xp_cap:
                dif = (self.current_xp + gained_xp) - self.xp_cap
                self.current_xp = dif
            else:
                self.current_xp = 0
            self.update_base_stats()
        
        self.current_xp += gained_xp
        
        if self.level >= 20: pass
        if self.level >= 40: pass

    # Synchronisiert Stats mit momentanen Level
    def update_base_stats(self):
        self.max_hp = round(self.max_hp + self.level,0)
        self.current_hp = round(self.current_hp + self.level,0)
        self.damage = self.damage + 0.25 * self.level
        self.speed = self.speed + self.level
        self.xp_cap = BASE_XP_VALUE * floor(self.level ** XP_MULTIPLIER)

    def set_base_stats(self):
        x = 0
        for i in range(0, self.level):
            x = x+i
        self.max_hp = round(self.max_hp + x,0)
        self.current_hp = self.max_hp
        self.damage = self.damage + 0.25 * x
        self.xp_cap = BASE_XP_VALUE * floor(self.level ** XP_MULTIPLIER)
        self.speed = self.speed + x


class TemporaryPokemon:
    def __init__(self, name, graphic_path, level, base_type, max_hp, damage, speed, moveset):
        # Base Stats
        self.name: str = name
        self.graphic_path: str = graphic_path
        self.level: int = level
        self.type: str = base_type
        self.max_hp: int = max_hp
        self.current_hp: int = self.max_hp
        self.damage: int = damage
        self.speed: int = speed
        self.moveset: list = moveset

        # Current Stats
        self.update_base_stats()

    def __repr__(self):
        return (f"{self.name} - Path: {self.graphic_path}, Level: {self.level}, Type: {self.type}, "
                f"Max HP: {self.max_hp}, Current HP: {self.current_hp}, Damage: {self.damage}, Speed: {self.speed}, "
                f"Moveset: {self.moveset}")

    # Synchronisiert Stats mit momentanen Level
    def update_base_stats(self):
        self.max_hp = round(self.max_hp + self.level,0)
        self.current_hp = round(self.current_hp + self.level,0)
        self.damage = self.damage + 0.25 * self.level

    def stats(self):
        return (self.name, self.graphic_path, self.level, self.type, self.current_hp, self.max_hp, self.damage,
                self.speed, self.moveset)
