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
from base64 import b64encode
from hashlib import sha256
from models import dbsession
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, Integer, Boolean
from models.BaseGameObject import BaseObject
from models.Permission import Permission

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
    gold = Column(Integer, default=0, nullable=False)
    health = Column(Integer, default=100, nullable=False)
    mana = Column(Integer, default=100, nullable=False)
    weapons = relationship("Weapon", backref=backref("User",
                                                     lazy="joined"), cascade="all, delete-orphan")
    armors = relationship("Armor", backref=backref("User",
                                                   lazy="joined"), cascade="all, delete-orphan")
    potions = relationship("Potion", backref=backref("User",
                                                     lazy="joined"), cascade="all, delete-orphan")

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
