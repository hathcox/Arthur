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

from libs.Form import Form
from libs.SecurityDecorators import authenticated
from handlers.BaseHandlers import UserBaseHandler
from models import ArmoryWeapon, ArmoryArmor, Weapon, Armor


class ShopWeaponsHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders weapons store page '''
        self.render("store/weapons.html", errors=None, weapons=ArmoryWeapon.get_all())

    @authenticated
    def post(self, *args, **kwargs):
        form = Form(
            uuid="Weapon not found",
        )
        if form.validate(self.request.arguments):
            user = self.get_current_user()
            weapon = ArmoryWeapon.by_uuid(self.request.arguments['uuid'][0])
            if user == None or weapon == None:
                self.render("store/weapons.html", errors=None, weapons=ArmoryWeapon.get_all())
            elif user.gold < weapon.cost:
                self.render("store/weapons.html", errors=['You cannot afford this weapon'], weapons=ArmoryWeapon.get_all())
            else:
                user.gold -= weapon.cost
                new_weapon = Weapon(
                    user_id=user.id,
                    name=weapon.name,
                    description=weapon.description,
                    required_level=weapon.required_level,
                    damage=weapon.damage,
                    rating=weapon.rating,
                    advanced=weapon.advanced,
                    classification=weapon.classification,
                    avatar=weapon.avatar,
                )
                self.dbsession.add(new_weapon)
                self.dbsession.add(user)
                self.dbsession.flush()
                self.render("store/purchase.html", item=weapon.name)
        else:
            self.render("store/weapons.html", errors=form.errors, weapons=ArmoryWeapon.get_all())


class ShopArmorHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders armor store page '''
        self.render("store/armor.html", errors=None, armors=ArmoryArmor.get_all())

    @authenticated
    def post(self, *args, **kwargs):
        form = Form(
            uuid="Armor not found",
        )
        if form.validate(self.request.arguments):
            user = self.get_current_user()
            armor = ArmoryArmor.by_uuid(self.request.arguments['uuid'][0])
            if user == None or armor == None:
                self.render("store/armor.html", errors=None, armors=ArmoryArmor.get_all())
            elif user.gold < armor.cost:
                self.render("store/armor.html", errors=['You cannot afford this armor'], armors=ArmoryArmor.get_all())
            else:
                user.gold -= armor.cost
                new_armor = Armor(
                    user_id=user.id,
                    name=armor.name,
                    description=armor.description,
                    required_level=armor.required_level,
                    rating=armor.rating,
                    classification=armor.classification,
                    avatar=armor.avatar,
                )
                self.dbsession.add(new_armor)
                self.dbsession.add(user)
                self.dbsession.flush()
                self.render("store/purchase.html", item=armor.name)
        else:
            self.render("store/armor.html", errors=form.errors, armors=ArmoryArmor.get_all())


class ShopPotionsHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders potions store page '''
        self.render("store/potions.html")

    @authenticated
    def post(self, *arg, **kwargs):
        pass


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
                'RequiredLevel': weapon.required_level,
                'Rating': weapon.rating,
                'Damage': weapon.damage,
                'Advanced': str(weapon.advanced),
                'Classification': weapon.classification,
            }
            self.write(json.dumps(details))
        elif classification == "armor":
            armor = ArmoryArmor.by_uuid(uuid)
            details = {
                'Name': armor.name,
                'Description': armor.description,
                'RequiredLevel': armor.required_level,
                'Avatar': armor.avatar,
                'Rating': armor.rating,
                'Classification': armor.classification,
            }
            self.write(json.dumps(details))
        else:
            self.write(json.dump({"Error": "Item not found"}))
        self.finish()
