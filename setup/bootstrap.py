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

if config.debug:
    password = 'nimda123'
else:
    sys.stdout.write(PROMPT + "New Admin ")
    sys.stdout.flush()
    password1 = getpass.getpass()
    sys.stdout.write(PROMPT + "Confirm New Admin ")
    sys.stdout.flush()
    password2 = getpass.getpass()
    if password1 == password2 and 12 <= len(password1):
        password = password1
    else:
        print WARN + 'Error: Passwords did not match, or were less than 12 chars'
        os._exit(1)

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
    number_of_battles = 5,
    max_monster_level = 1
)
dbsession.add(quest)

quest = Quest(
    name = "Into the Woods",
    level = 2,
    number_of_battles = 10,
    max_monster_level = 3
)
dbsession.add(quest)

quest = Quest(
    name = "The River of Glien",
    level = 3,
    number_of_battles = 15,
    max_monster_level = 5
)
dbsession.add(quest)

quest = Quest(
    name = "The River of Bassas",
    level = 4,
    number_of_battles = 20,
    max_monster_level = 7
)
dbsession.add(quest)

quest = Quest(
    name = "The City of Legion",
    level = 5,
    number_of_battles = 20,
    max_monster_level = 10
)
dbsession.add(quest)

quest = Quest(
    name = "The River of Tribuit",
    level = 6,
    number_of_battles = 25,
    max_monster_level = 13
)
dbsession.add(quest)

quest = Quest(
    name = "Mount Badon",
    level = 7,
    number_of_battles = 25,
    max_monster_level = 16
)
dbsession.add(quest)

quest = Quest(
    name = "Camlann",
    level = 8,
    number_of_battles = 30,
    max_monster_level = 18
)
dbsession.add(quest)

quest = Quest(
    name = "The Holy Grail",
    level = 9,
    number_of_battles = 40,
    max_monster_level = 20
)
dbsession.add(quest)

quest = Quest(
    name = "Pokemon League",
    level = 10,
    number_of_battles = 999,
    max_monster_level = 999
)
dbsession.add(quest)

### Monsters ###

monster = Monster(
    name = "Faggot Monster",
    health = 200,
    mana = 300,
    experience = 200,
    level = 3,
    gold = 20,
    avatar = "/static/images/monster/fuck.jpg",
    armor_id = 1,
    weapon_id = 10,
)
dbsession.add(monster)

monster = Monster(
    name = "LVL 1 Monster",
    health = 1,
    mana = 300,
    experience = 200,
    level = 1,
    gold = 20,
    avatar = "/static/images/monster/fuck.jpg",
    armor_id = 1,
    weapon_id = 1,
)

dbsession.add(monster)
monster = Monster(
    name = "LVL 2 Monster",
    health = 3,
    mana = 300,
    experience = 200,
    level = 2,
    gold = 20,
    avatar = "/static/images/monster/fuck.jpg",
    armor_id = 1,
    weapon_id = 1,
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
