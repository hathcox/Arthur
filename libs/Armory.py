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
        items = []
        items.append({
            'name': 'The Holy Handgrande of Antiok',
            'description': 'Count to three',
            'cost': 5000,
            'rating': 100,
            'advanced': True,
            'classification': MELEE,
        })
        return items

    @classmethod
    def get_armor(cls):
        items = []
        return items

    @classmethod
    def get_potions(cls):
        items = []
        items.append({
            'name': 'Mana Potion',
            'description': 'Restores 100 mana',
            'cost': 100,
            'classification': MANA,
        })
        items.append({
            'name': 'Health Potion',
            'description': 'Restores 100 health',
            'cost': 100,
            'classification': HEALTH,
        })
        return items