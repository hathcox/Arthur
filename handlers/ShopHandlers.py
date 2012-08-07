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

from libs.Armory import Items
from handlers.BaseHandlers import UserBaseHandler
from libs.SecurityDecorators import authenticated


class ShopWeaponsHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders weapons store page '''
        self.render("store/weapons.html", weapons=Items.get_weapons())

    @authenticated
    def post(self, *args, **kwargs):
        pass


class ShopArmorHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders armor store page '''
        self.render("store/armor.html", armor=Items.get_armor())


class ShopPotionsHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders potions store page '''
        self.render("store/potions.html", potions=Items.get_potions())