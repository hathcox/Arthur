# -*- coding: utf-8 -*-
'''
Created on Mar 13, 2012

@author: moloch

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

# Classifications
MELEE = "melee"
SPELL = "spell"
LIGHT_ARMOR = "light_armor"
HEAVY_ARMOR = "heavy_armor"
HEALTH = "health"
MANA = "mana"

class Items(object):

    @classmethod
    def get_weapons(cls):
        items = {}
        items['The Holy Hand Grenade of Antioch'] = {
            'description': 'Count to three',
            'damage': 5000,
            'required_level': 50,
            'avatar': '/static/images/weapons/antioch.png',
            'cost': 5000,
            'rating': 500,
            'advanced': True,
            'classification': MELEE,
        }
        items['Short Sword'] = {
            'name':'Short Sword',
            'description': 'A small blade',
            'damage': 20,
            'required_level': 1,
            'avatar': '/static/images/weapons/short_sword.png',
            'cost': 50,
            'rating': 20,
            'advanced': False,
            'required_level':1,
            'damage':10,
            'classification': MELEE,
        }
        return items

    @classmethod
    def get_armor(cls):
        items = {}
        items['Leather Straps'] = {
            'description': 'Weak armor',
            'required_level': 1,
            'avatar': '/static/images/armor/leather_straps.png',
            'cost': 50,
            'rating': 20,
            'classification': LIGHT_ARMOR,
        }
        return items

    @classmethod
    def get_potions(cls):
        items = {}
        items['Mana Potion'] = {
            'description': 'Restores 100 mana',
            'required_level': 1,
            'avatar': '/static/images/potions/mana.png',
            'cost': 100,
            'classification': MANA,
        }
        items['Health Potion'] = {
            'description': 'Restores 100 health',
            'required_level': 1,
            'avatar': '/static/images/potions/health.png',
            'cost': 100,
            'classification': HEALTH,
        }
        return items