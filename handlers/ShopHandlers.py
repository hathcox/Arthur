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


import json

from libs.SecurityDecorators import authenticated
from handlers.BaseHandlers import UserBaseHandler
from models import ArmoryWeapon, ArmoryArmor


class ShopWeaponsHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders weapons store page '''
        self.render("store/weapons.html", weapons=ArmoryWeapon.get_all())

    @authenticated
    def post(self, *args, **kwargs):
        pass


class ShopArmorHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders armor store page '''
        self.render("store/armor.html", armor=ArmoryArmor.get_all())


class ShopPotionsHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders potions store page '''
        self.render("store/potions.html", potions=Items.get_potions())


class ShopAjaxHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Sends item details via ajax '''
        try:
            classification = self.get_argument("cls")
            uuid = self.get_argument("uuid")
        except:
            self.write(json.dumps({"Error": "Missing parameter"}))
            return
        if classification == "weapon":
            weapon = ArmoryWeapon.by_uuid(uuid)
            details = {
                'Name': weapon.name,
                'Description': weapon.description,
                'Avatar': weapon.avatar,
            }
            self.write(json.dumps(details))
        elif classification == "armor":
            armor = ArmoryArmor.by_uuid(uuid)
            details = {
                'Name': armor.name,
                'Description': armor.description,
                'Avatar': armor.avatar,
            }
            self.write(json.dumps(details))
        else:
            self.write(json.dump({"Error": "Item not found"}))
        self.finish()
