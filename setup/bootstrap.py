# -*- coding: utf-8 -*-
'''
    Copyright [2012] [Redacted Labs]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''


import os
import sys
import getpass

from libs.ConsoleColors import *
from libs.ConfigManager import ConfigManager
from models import dbsession, User, Permission, ArmoryWeapon, ArmoryArmor, Quest, Monster

# Fills the database with some startup data.
config = ConfigManager.Instance()

# if config.debug:
password = 'nimda123'
# else:
#     sys.stdout.write(PROMPT + "New Admin ")
#     sys.stdout.flush()
#     password1 = getpass.getpass()
#     sys.stdout.write(PROMPT + "Confirm New Admin ")
#     sys.stdout.flush()
#     password2 = getpass.getpass()
#     if password1 == password2 and 12 <= len(password1):
#         password = password1
#     else:
#         print WARN + 'Error: Passwords did not match, or were less than 12 chars'
#         os._exit(1)

# User Account
user = User(
    name=unicode('admin'),
)
dbsession.add(user)
dbsession.flush()
user.password = password
dbsession.add(user)
dbsession.flush()
permission = Permission(
    name=unicode('admin'),
    user_id=user.id
)
dbsession.add(permission)

##### BOOT STRAP ITEMS ##### 

### Weapons
weapon = ArmoryWeapon(
    name="Dagger",
    description="Slightly better than a butter knife",
    required_level=1,
    cost=50,
    damage=10,
    advanced=True,
    classification="Sword",
    rating=30,
    avatar="/static/images/weapons/dagger.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="Short Sword",
    description="A small light sword",
    required_level=3,
    cost=150,
    damage=20,
    advanced=True,
    classification="Sword",
    rating=30,
    avatar="/static/images/weapons/short_sword.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="Mace",
    description="Metal rod with a spiked ball on top",
    required_level=5,
    cost=300,
    damage=35,
    advanced=False,
    classification="Mace",
    rating=35,
    avatar="/static/images/weapons/mace.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="Long Sword",
    description="A long sword",
    required_level=8,
    cost=700,
    damage=40,
    advanced=True,
    classification="Sword",
    rating=35,
    avatar="/static/images/weapons/long_sword.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="Cutlass",
    description="A pirates sword! Yar!",
    required_level=10,
    cost=1500,
    damage=50,
    advanced=True,
    classification="Sword",
    rating=40,
    avatar="/static/images/weapons/cutlass.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="War Axe",
    description="A simple and small axe",
    required_level=13,
    cost=4000,
    damage=70,
    advanced=True,
    classification="Axe",
    rating=50,
    avatar="/static/images/weapons/war_axe.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="War Hammer",
    description="Large hammer like weapon",
    required_level=15,
    cost=6000,
    damage=900,
    advanced=True,
    classification="Hammer",
    rating=70,
    avatar="/static/images/weapons/war_hammer.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="Katana",
    description="Choice weapon for the Samurai",
    required_level=17,
    cost=7000,
    damage=150,
    advanced=True,
    classification="Sword",
    rating=75,
    avatar="/static/images/weapons/katana.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="Battle Axe",
    description="A large double-sided axe",
    required_level=18,
    cost=9000,
    damage=200,
    advanced=True,
    classification="Axe",
    rating=90,
    avatar="/static/images/weapons/battle_axe.png",
)
dbsession.add(weapon)

weapon = ArmoryWeapon(
    name="Claymore",
    description="A very large two handed sword",
    required_level=20,
    cost=10000,
    damage=400,
    advanced=True,
    classification="Sword",
    rating=95,
    avatar="/static/images/weapons/claymore.png",
)
dbsession.add(weapon)

### Armor
armor = ArmoryArmor(
    name="Simple Robe",
    description="Weak cloth to cover your disgusting naked body...",
    required_level=1,
    cost=50,
    classification="Light Armor",
    rating=10,
    avatar="/static/images/armor/simple_robe.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Fur Hide",
    description="Armor made from the hide of an animal",
    required_level=3,
    cost=200,
    classification="Light Armor",
    rating=35,
    avatar="/static/images/armor/fur_armor.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Leather Straps",
    description="Armor made from hide",
    required_level=5,
    cost=500,
    classification="Light Armor",
    rating=55,
    avatar="/static/images/armor/leather_straps.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Scaled Armor",
    description="Scaled armor",
    required_level=10,
    cost=1000,
    classification="Light Armor",
    rating=150,
    avatar="/static/images/armor/scaled_armor.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Light Plated Armor",
    description="Lightly plated armor with leather",
    required_level=12,
    cost=3000,
    classification="Light Armor",
    rating=200,
    avatar="/static/images/armor/leather_plated_armor.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Studded Leather Straps",
    description="Fine leather with studded straps",
    required_level=15,
    cost=5000,
    classification="Light Armor",
    rating=250,
    avatar="/static/images/armor/studded_leather_armor.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Plated Armor",
    description="Steel plated armor",
    required_level=18,
    cost=6500,
    classification="Heavy Armor",
    rating=300,
    avatar="/static/images/armor/plated_armor.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Superior Leather Armor",
    description="The finest leather armor money can buy",
    required_level=20,
    cost=8000,
    classification="Light Armor",
    rating=350,
    avatar="/static/images/armor/superior_leather_armor.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Gold Plated Armor",
    description="Plated armor made of Gold",
    required_level=23,
    cost=10000,
    classification="Heavy Armor",
    rating=400,
    avatar="/static/images/armor/gold_plated_armor.png",
)
dbsession.add(armor)

armor = ArmoryArmor(
    name="Dragon Plate",
    description="Armor made only of the bones of Dragons",
    required_level=25,
    cost=12000,
    classification="Heavy Armor",
    rating=500,
    avatar="/static/images/armor/dragon_armor.png",
)
dbsession.add(armor)

## Quick flush to generate id's
dbsession.flush()

### Quests ###
quest = Quest(
    name = "The Training Grounds",
    level = 1,
    number_of_battles = 10,
    min_monster_level = 1,
    max_monster_level = 1
)
dbsession.add(quest)

quest = Quest(
    name = "Into the Woods",
    level = 2,
    number_of_battles = 15,
    min_monster_level = 1,
    max_monster_level = 3
)
dbsession.add(quest)

quest = Quest(
    name = "The River of Glien",
    level = 3,
    number_of_battles = 15,
    min_monster_level = 3,
    max_monster_level = 4
)
dbsession.add(quest)

quest = Quest(
    name = "The River of Bassas",
    level = 4,
    number_of_battles = 20,
    min_monster_level = 4,
    max_monster_level = 6
)
dbsession.add(quest)

quest = Quest(
    name = "The City of Legion",
    level = 5,
    number_of_battles = 20,
    min_monster_level = 6,
    max_monster_level = 9
)
dbsession.add(quest)

quest = Quest(
    name = "The River of Tribuit",
    level = 6,
    number_of_battles = 25,
    min_monster_level = 9,
    max_monster_level = 12
)
dbsession.add(quest)

quest = Quest(
    name = "Mount Agned",
    level = 7,
    number_of_battles = 30,
    min_monster_level = 12,
    max_monster_level = 15
)
dbsession.add(quest)

quest = Quest(
    name = "Mount Badon",
    level = 8,
    number_of_battles = 30,
    min_monster_level = 15,
    max_monster_level = 17
)
dbsession.add(quest)

quest = Quest(
    name = "Camlann",
    level = 9,
    number_of_battles = 40,
    min_monster_level = 17,
    max_monster_level = 20
)
dbsession.add(quest)

quest = Quest(
    name = "The Holy Grail",
    level = 10,
    number_of_battles = 1,
    min_monster_level = 25,
    max_monster_level = 25,
)
dbsession.add(quest)

quest = Quest(
    name = "Pokemon League",
    level = 11,
    number_of_battles = 999,
    min_monster_level = 999,
    max_monster_level = 999
)
dbsession.add(quest)

### Monsters ###

monster = Monster(
    name = "Bunny",
    health = 50,
    experience = 50,
    level = 1,
    gold = 10,
    avatar = "/static/images/monsters/bunny.jpg",
    armor_id = 1,
    weapon_id = 1,
)
dbsession.add(monster)

monster = Monster(
    name = "Stag",
    health = 100,
    experience = 100,
    level = 2,
    gold = 15,
    avatar = "/static/images/monsters/stag.jpg",
    armor_id = 1,
    weapon_id = 1,
)
dbsession.add(monster)

monster = Monster(
    name = "Wolf",
    health = 250,
    experience = 200,
    level = 3,
    gold = 30,
    avatar = "/static/images/monsters/wolf.jpg",
    armor_id = 2,
    weapon_id = 3,
)
dbsession.add(monster)

monster = Monster(
    name = "Bear",
    health = 400,
    experience = 300,
    level = 4,
    gold = 50,
    avatar = "/static/images/monsters/bear.jpg",
    armor_id = 2,
    weapon_id = 4,
)
dbsession.add(monster)

monster = Monster(
    name = "Thief",
    health = 500,
    experience = 350,
    level = 5,
    gold = 90,
    avatar = "/static/images/monsters/thief.jpg",
    armor_id = 3,
    weapon_id = 5,
)
dbsession.add(monster)

monster = Monster(
    name = "Pre-Teen Troll",
    health = 650,
    experience = 500,
    level = 6,
    gold = 120,
    avatar = "/static/images/monsters/pre_teen_troll.jpg",
    armor_id = 4,
    weapon_id =4,
)
dbsession.add(monster)

monster = Monster(
    name = "Bandit",
    health = 800,
    experience = 500,
    level = 7,
    gold = 200,
    avatar = "/static/images/monsters/bandit.jpg",
    armor_id = 5,
    weapon_id = 5,
)
dbsession.add(monster)

monster = Monster(
    name = "Guinevere",
    health = 800,
    experience = 800,
    level = 8,
    gold = 300,
    avatar = "/static/images/monsters/guinevere.jpg",
    armor_id = 7,
    weapon_id = 2,
)
dbsession.add(monster)

monster = Monster(
    name = "Squire",
    health = 1000,
    experience = 800,
    level = 9,
    gold = 350,
    avatar = "/static/images/monsters/squire.jpg",
    armor_id = 5,
    weapon_id = 6,
)
dbsession.add(monster)

monster = Monster(
    name = "Knight",
    health = 2000,
    experience = 900,
    level = 10,
    gold = 400,
    avatar = "/static/images/monsters/knight.jpg",
    armor_id = 6,
    weapon_id = 6,
)
dbsession.add(monster)

monster = Monster(
    name = "Ogre",
    health = 3000,
    experience = 900,
    level = 11,
    gold = 450,
    avatar = "/static/images/monsters/ogre.jpg",
    armor_id = 5,
    weapon_id = 7,
)
dbsession.add(monster)

monster = Monster(
    name = "Baby Dragon",
    health = 4500,
    experience = 1000,
    level = 12,
    gold = 500,
    avatar = "/static/images/monsters/baby_dragon.jpg",
    armor_id = 5,
    weapon_id = 6,
)
dbsession.add(monster)

monster = Monster(
    name = "Troll",
    health = 6000,
    experience = 1100,
    level = 13,
    gold = 550,
    avatar = "/static/images/monsters/troll.jpg",
    armor_id = 7,
    weapon_id = 7,
)
dbsession.add(monster)

monster = Monster(
    name = "King's Guard",
    health = 10000,
    experience = 1150,
    level = 14,
    gold = 600,
    avatar = "/static/images/monsters/kings_guard.jpg",
    armor_id = 8,
    weapon_id = 7,
)
dbsession.add(monster)

monster = Monster(
    name = "Sir Lancelot",
    health = 12000,
    experience = 1200,
    level = 15,
    gold = 700,
    avatar = "/static/images/monsters/sir_lancelot.jpg",
    armor_id = 7,
    weapon_id = 9,
)
dbsession.add(monster)

monster = Monster(
    name = "Griffon",
    health = 13000,
    experience = 1300,
    level = 16,
    gold = 600,
    avatar = "/static/images/monsters/griffon.jpg",
    armor_id = 9,
    weapon_id = 9,
)
dbsession.add(monster)

monster = Monster(
    name = "Leviathan",
    health = 15000,
    experience = 1400,
    level = 17,
    gold = 700,
    avatar = "/static/images/monsters/leviathan.jpg",
    armor_id = 10,
    weapon_id = 9,
)
dbsession.add(monster)

monster = Monster(
    name = "Behemoth",
    health = 18000,
    experience = 1500,
    level = 18,
    gold = 850,
    avatar = "/static/images/monsters/behemoth.jpg",
    armor_id = 10,
    weapon_id = 10,
)
dbsession.add(monster)

monster = Monster(
    name = "Dragon",
    health = 20000,
    experience = 1700,
    level = 19,
    gold = 900,
    avatar = "/static/images/monsters/dragon.jpg",
    armor_id = 10,
    weapon_id = 10,
)
dbsession.add(monster)

monster = Monster(
    name = "Elder Dragon",
    health = 25000,
    experience = 2000,
    level = 20,
    gold = 1000,
    avatar = "/static/images/monsters/elder_dragon.jpg",
    armor_id = 10,
    weapon_id = 10,
)
dbsession.add(monster)

monster = Monster(
    name = "Guardian of the Holy Grail",
    health = 50000,
    experience = 5000,
    level = 25,
    gold = 1500,
    avatar = "/static/images/monsters/guardian_of_the_holy_grail.jpg",
    armor_id = 10,
    weapon_id = 10,
)
dbsession.add(monster)

### Flush database session
dbsession.flush()

#### CONSOLE #### 
if config.debug:
    environ = bold + R + "Developement boot strap" + W
    details = ", default admin password is '%s'." % password
else:
    environ = bold + "Production boot strap" + W
    details = '.'
print INFO + '%s completed successfully%s' % (environ, details)
