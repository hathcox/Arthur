'''
Created on Mar 12, 2012

@author: hathcox

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
from threading import Lock
from libs.Singleton import *
from datetime import datetime, timedelta


BID_SIZE = 24
battle_TIME = 60


@Singleton
class BattleManager():
    ''' Mostly thread safe battle manager '''

    def __init__(self):
        self.battles = {}
        self.battles_lock = Lock()

    def start_battle(self):
        ''' Creates a new battle and returns the battle id and the new battle object '''
        bid = b64encode(urandom(BID_SIZE))
        self.battles_lock.acquire()
        self.battles[bid] = Battle(bid)
        self.battles_lock.release()
        return bid, self.battles[bid]

    def remove_battle(self, bid):
        ''' Removes a given battle '''
        if bid in self.battles.keys():
            self.battles_lock.acquire()
            del self.battles[bid]
            self.battles_lock.release()

    def get_battle(self, bid, ip_address):
        ''' Returns a battle object if it exists or None '''
        if bid in self.battles.keys():
            if self.battles[bid].is_expired():
                self.remove_battle(bid)
            elif self.battles[bid].data['ip'] == ip_address:
                return self.battles[bid]
        return None

    def clean_up(self):
        ''' Removes all expired battles '''
        for bid in self.battles.keys():
            if self.battles[bid].is_expired():
                self.battles_lock.acquire()
                del self.battles[bid]
                self.battles_lock.release()


class Battle():
    ''' battle object stores data, time, id '''

    def __init__(self, bid):
        self.id = bid
        self.data = {}
        self.expiration = datetime.now() + timedelta(minutes=battle_TIME)

    def is_expired(self):
        ''' Returns boolean based on if battle has expired '''
        return (timedelta(0) < (datetime.now() - self.expiration))
