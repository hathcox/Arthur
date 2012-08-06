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


class Weapon(BaseObject):

    _name = Column(Unicode(64), unique=True, nullable=False)
    name = synonym('_name', descriptor=property(
        lambda self: self._name,
        lambda self, name: setattr(
            self, '_name', self.__class__.filter_string(name, " _-"))
    ))
    description = Column(Unicode(1024), nullable=False)
    required_level = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    damage = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    advanced = Column(Boolean, nullable=False)
    classification = Column(Unicode(64), nullable=False)

    @classmethod
    def get_all(cls):
        ''' Return all weapon objects '''
        return dbsession.query(cls).all()

    @classmethod
    def get_classification(cls, classify):
        ''' Return all non-admin item objects '''
        return dbsession.query(cls).filter_by(classification=unicode(classify)).all()

    @classmethod
    def filter_string(cls, string, extra_chars=''):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)
