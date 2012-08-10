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
from models import dbsession
from models.Quest import Quest
from random import choice

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
    gold = Column(Integer, nullable=False)

    armor_id = Column(Integer, nullable=False)
    weapon_id = Column(Integer, nullable=False)

    @classmethod
    def by_id(cls, uid):
        ''' Return the user object whose user id is uid '''
        return dbsession.query(cls).filter_by(id=unicode(uid)).first()

    @classmethod
    def get_all(cls):
        ''' Return all non-admin user objects '''
        return dbsession.query(cls).filter(cls.name != u'admin').all()

    @classmethod
    def filter_string(cls, string, extra_chars=''):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)

    @classmethod
    def get_monster(cls, user):
        ''' Based on the users quest and level this will choose an appropriate monster '''
        quest = Quest.by_id(user.quest_level)
        #If we are still on quests
        if quest != None:
            #Get all valid monsters
            all = dbsession.query(cls).filter(cls.level<=quest.max_monster_level).filter(cls.level>=quest.min_monster_level).all()
            return choice(all)
        return choice(cls.get_all())

    @property
    def to_json(self):
        json = { "name" : self.name,
            "health" : self.health,
            "mana" : self.mana,
            "strength" : self.strength,
            "defense" : self.defense,
            "level" : self.level,
            "avatar" : self.avatar }
        return json