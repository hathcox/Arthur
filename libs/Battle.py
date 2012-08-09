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
import json
from libs.Singleton import *
from models.User import User
from models.Monster import Monster

class Battle():
    ''' This is the battle instance that is linked to the players session '''
    def __init__(self, user):
        ''' Randomly generates a monster for the player to fight '''
        self.user = user
        self.monster = Monster.get_monster(user)
        self.text = "A random "+self.monster.name+" appears!"
        #True means its the users turn, False means its the cpu's turn
        self.turn = True

    def do_round(self, choice):
        ''' perform the users turn '''
        pass

class BattleMessage():
    ''' 
    This is the serialized message from a websocket 

    Response Types:
        Invalid - This means we got something that doesn't make send_response
        
        Setup - Send all of the monster information back to the player

        Update - This is sent after every round, regardless of player or computer
            - This constains the user, monster, and text results
        
        Battle End - This means that the battle has ended, either the player or the monster diead
            - This contains the victor, the final text, experience gained, and gold gained
        
        Wait - This means its not your turn yet
        
        Go - This means it is your turn

    '''
    
    START_BATTLE = "startbattle"

    def __init__(self, json_string):
        try:
            print json.loads(json_string)
            self.raw_json = json.loads(json_string)
            self.type = self.raw_json["type"]
            self.sid = self.raw_json["sid"]
            self.valid = True
        except Exception as e:
            self.raw_json = None
            self.valid = False

    @classmethod
    def send_end(cls, websocket, victor, text, exp, gold):
        websocket.write_message(json.dumps(
            {
            "type":"END",
            "victor": victor.name,
            "text":text,
            "experience":exp,
            "gold":gold
            }))

    @classmethod
    def send_update(cls, websocket, user, monster, text):
        websocket.write_message(json.dumps(
            {
            "type":"UPDATE",
            "user": user.to_json(),
            "monster":monster.to_json,
            "text":text
            }))

    @classmethod
    def send_setup(cls, websocket, monster, text):
        websocket.write_message(json.dumps(
            {
            "type":"SETUP",
            "monster":monster.to_json,
            "text":text
            }))

    @classmethod
    def send_go(cls, websocket):
        websocket.write_message(json.dumps({"type":"GO"}))

    @classmethod
    def send_wait(cls, websocket):
        websocket.write_message(json.dumps({"type":"WAIT"}))

    @classmethod
    def send_invalid(cls, websocket):
        websocket.write_message(json.dumps({"type":"INVALID"}))


@Singleton
class BattleManager():

    def __init__(self):
        self.battles = {}

    def start_battle(self, session):
        ''' Creates a battle instance and links it to an sid '''
        user = User.by_name(session.data['name'])
        self.battles[session.id] = Battle(user)
        return self.battles[session.id]

    def get_battle(self, session):
        return self.battles[session.id]