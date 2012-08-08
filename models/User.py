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


from os import urandom
from math import sqrt
from base64 import b64encode
from hashlib import sha256
from models import dbsession, Weapon, Armor, Potion
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, Integer, Boolean
from models.BaseGameObject import BaseObject
from models.Permission import Permission
from string import ascii_letters, digits
from models.Weapon import Weapon
from models.Armor import Armor


def get_salt():
    ''' Generate a 24-byte random salt '''
    return unicode(b64encode(urandom(24)))


class User(BaseObject):
    ''' User definition '''

    _name = Column(Unicode(64), unique=True, nullable=False)
    name = synonym('_name', descriptor=property(
        lambda self: self._name,
        lambda self, name: setattr(
            self, '_name', self.__class__.filter_string(name, " _-"))
    ))
    permissions = relationship("Permission", backref=backref(
        "User", lazy="joined"), cascade="all, delete-orphan")
    _password = Column('password', Unicode(128))
    password = synonym('_password', descriptor=property(
        lambda self: self._password,
        lambda self, password: setattr(self, '_password',
                                       self.__class__._hash_password(password, self.salt))
    ))
    salt = Column(
        Unicode(32), unique=True, nullable=False, default=get_salt)
    avatar = Column(Unicode(128), default=unicode("default_avatar.jpeg"))
    gold = Column(Integer, default=0, nullable=False)
    health = Column(Integer, default=100, nullable=False)
    mana = Column(Integer, default=100, nullable=False)
    strength = Column(Integer, default=1, nullable=False)
    defense = Column(Integer, default=1, nullable=False)
    experience = Column(Integer, default=0, nullable=False)
    weapons = relationship("Weapon", backref=backref("User",
                                                     lazy="joined"), cascade="all, delete-orphan")
    armor = relationship("Armor", backref=backref("User",
                                                   lazy="joined"), cascade="all, delete-orphan")
    potions = relationship("Potion", backref=backref("User",
                                                     lazy="joined"), cascade="all, delete-orphan")
    quest_level = Column(Integer, default=1, nullable=False)
    current_quest_battle = Column(Integer, default=0, nullable=False)


    @classmethod
    def by_id(cls, uid):
        ''' Return the user object whose user id is uid '''
        return dbsession.query(cls).filter_by(id=unicode(uid)).first()

    @classmethod
    def by_name(cls, name):
        ''' Return the user object whose name is name '''
        return dbsession.query(cls).filter_by(name=unicode(name)).first()

    @classmethod
    def get_all(cls):
        ''' Return all non-admin user objects '''
        return dbsession.query(cls).filter(cls.name != u'admin').all()

    @classmethod
    def filter_string(cls, string, extra_chars=''):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)

    def validate_password(self, attempt):
        ''' Check the password against existing credentials '''
        return self.password == self._hash_password(attempt, self.salt)

    def has_permission(self, permission):
        ''' Return True if 'permission' is in permissions_names '''
        return True if permission in self.permissions_names else False

    def get_all_weapons(self):
        ''' Returns all weapons that are not equiped '''
        return dbsession.query(Weapon).filter_by(user_id = self.id).filter_by(equiped=False).all()

    def get_all_armor(self):
        ''' Returns all armor that are not equiped '''
        return dbsession.query(Armor).filter_by(user_id = self.id).filter_by(equiped=False).all()

    @property
    def level(self):
        ''' log(exp) = current level '''
        if self.experience > 100:
            return int(sqrt(self.experience*.01))
        return 1

    @property
    def equiped_weapon(self):
        ''' Returns the current equiped weapon on that user '''
        return filter(lambda weapon: weapon.equiped == True, self.weapons)[0]

    @property
    def equiped_armor(self):
        ''' Returns the current equiped weapon on that user '''
        return filter(lambda armor: armor.equiped == True, self.armor)[0]

    @property
    def permissions_names(self):
        ''' Return a list with all permissions names granted to the user '''
        return [permission.permission_name for permission in self.permissions]

    @classmethod
    def _hash_password(cls, password, salt):
        '''
        Hashes the password using 15,001 rounds of salted SHA-256, come at me bro.
        This function will always return a unicode string, but can take an arg of
        any type not just ascii strings, the salt will always be unicode
        '''
        sha = sha256()
        sha.update(password + salt)
        for count in range(0, 15000):
            sha.update(sha.hexdigest() + str(count))
        return unicode(sha.hexdigest())
