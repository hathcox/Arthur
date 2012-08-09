'''
Created on Mar 12, 2012

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


from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, Integer, Boolean
from models.BaseGameObject import BaseObject
from string import ascii_letters, digits


class Monster(BaseObject):

    _name = Column(Unicode(64), unique=True, nullable=False)
    name = synonym('_name', descriptor=property(
        lambda self: self._name,
        lambda self, name: setattr(
            self, '_name', self.__class__.filter_string(name, " _-"))
    ))
    health = Column(Integer, default=100, nullable=False)
    mana = Column(Integer, default=100, nullable=False)
    strength = Column(Integer, default=1, nullable=False)
    defense = Column(Integer, default=100, nullable=False)
    experience = Column(Integer, default=100, nullable=False)
    avatar = Column(Unicode(128), default=unicode("default_avatar.jpeg"))  
    level = Column(Integer, nullable=False)

    armor_id = Column(Integer, ForeignKey('armor.id'))
    weapon_id = Column(Integer, ForeignKey('weapon.id'))

    @classmethod
    def filter_string(cls, string, extra_chars=''):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)

    @classmethod
    def get_monster(cls, user):
        ''' Based on the users quest and level this will choose an appropriate monster '''
        return None