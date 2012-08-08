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

from models import dbsession
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relationship, backref
from sqlalchemy.types import Unicode, Integer, Boolean
from models.BaseGameObject import BaseObject
from string import ascii_letters, digits


class Weapon(BaseObject):

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    _name = Column(Unicode(64), nullable=False)
    name = synonym('_name', descriptor=property(
        lambda self: self._name,
        lambda self, name: setattr(
            self, '_name', self.__class__.filter_string(name, " _-"))
    ))
    description = Column(Unicode(1024), nullable=False)
    required_level = Column(Integer, nullable=False)
    damage = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    advanced = Column(Boolean, nullable=False)
    classification = Column(Unicode(64), nullable=False)
    avatar = Column(Unicode(1024), nullable=False)
    equiped = Column(Boolean, default=False, nullable=False)

    @classmethod
    def get_all(cls):
        ''' Return all weapon objects '''
        return dbsession.query(cls).all()

    @classmethod
    def by_id(cls, uid):
        ''' Return the user object whose user id is uid '''
        return dbsession.query(cls).filter_by(id=unicode(uid)).first()

    @classmethod
    def by_name(cls, name):
        ''' Return the user object whose name is name '''
        return dbsession.query(cls).filter_by(name=unicode(name)).first()

    @classmethod
    def get_classification(cls, classify):
        ''' Return all non-admin item objects '''
        return dbsession.query(cls).filter_by(classification=unicode(classify)).all()

    @classmethod
    def filter_string(cls, string, extra_chars=''):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)
