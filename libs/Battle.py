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
from models.Quest import Quest
from random import choice
from models import dbsession
from models.ArmoryWeapon import ArmoryWeapon
from threading import Lock

class BattleUser():
    ''' This is a wraper for the database user object, this make sure we donnt mess things up '''
    def __init__(self, user):
        self.gold = user.gold
        self.name = user.name
        self.health = user.health
        self.mana = user.mana
        self.strength = user.strength
        self.defense = user.defense
        self.experience = user.experience
        self.level = user.level
        self.id = user.id
        self.avatar = user.avatar

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

    def attack_monster(self, monster):
        ''' Calculates the damage toward a given monster '''
        return 10


class BattleMonster():
    ''' lol pokemon reference '''

    def __init__(self, monster):
        self.gold = monster.gold
        self.name = monster.name
        self.health = monster.health
        self.mana = monster.mana
        self.strength = monster.strength
        self.defense = monster.defense
        self.experience = monster.experience
        self.level = monster.level
        self.id = monster.id
        self.avatar = monster.avatar
        self.weapon_id = monster.weapon_id

    def attack_user(self, user):
        ''' calculates damage agianst a provided user '''
        return 3

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

class Battle():
    ''' This is the battle instance that is linked to the players session '''

    def __init__(self, user):
        ''' Randomly generates a monster for the player to fight '''
        self.user = BattleUser(user)
        self.monster = BattleMonster(Monster.get_monster(user))
        self.text = "A random "+self.monster.name+" appears!"
        #True means its the users turn, False means its the cpu's turn
        self.turn = True

    def check_ended(self):
        valid_user = User.by_id(self.user.id)
        #check is the user died
        if self.monster.health <= 0:
            #update the user
            valid_user.experience += self.monster.experience
            valid_user.gold += self.monster.gold

            #Grab the quest
            quest = Quest.by_id(user.current_quest_battle)
            if quest != None:
                #If we still have battles left in our quest
                if valid_user.current_quest_battle < quest.number_of_battles:
                    valid_user.current_quest_battle += 1
                #If not, give us the next quest
                else:
                    valid_user.current_quest_battle = 0
                    valid_user.quest_level += 1
            dbsession.add(valid_user)
            dbsession.flush()

            #set variable for the client
            self.victor = self.user
            self.text = self.user.name+" has defeated "+self.monster.name+" !"
            self.exp = self.monster.experience
            self.gold = self.monster.gold
            return True

        elif self.user.health <= 0:
            #decrement experience
            valid_user.lost_battle()
            dbsession.add(valid_user)
            dbsession.flush()

            #set variable for the client
            self.victor = self.monster
            self.text = self.monster.name+" has defeated "+self.user.name+" !"
            self.exp = valid_user.experience
            self.gold = 0
            return True

        #Both user and monster are alive
        return False

    def do_user_round(self, choice):
        ''' perform the users turn '''
        self.check_ended()
        if choice == BattleMessage.ATTACK:
            damage = self.user.attack_monster(self.monster)
            self.monster.health -= damage
            self.text = self.user.name+" hits "+self.monster.name +" for "+str(damage)+" damage!"

    def do_computer_round(self):
        ''' perform the computers turn '''
        #Make sure its not already over
        self.check_ended()
        #Randomly choose a move
        move = self.choose_random_computer_move()
        #perform that move
        # if move == BattleMessage.ATTACK:
        damage = self.monster.attack_user(self.user)
        self.user.health -= damage
        self.text = self.monster.name+" hits "+self.user.name+" for "+str(damage)+" damage!"


    def choose_random_computer_move(self):
        ''' returns one or three possible moves '''
        choices = [
            BattleMessage.ATTACK,
            BattleMessage.DEFEND
        ]
        monster_weapon = ArmoryWeapon.by_id(self.monster.weapon_id)
        #If the monster can do advanced attacks
        if monster_weapon.advanced:
            choices.append(BattleMessage.ADVANCED)

        return choice(choices)

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
    ATTACK = "attack"
    DEFEND = "defend"
    ADVANCED = "advanced"

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
    def send_end(cls, websocket, battle):
        websocket.write_message(json.dumps(
            {
            "type":"END",
            "victor": battle.victor.name,
            "text":battle.text,
            "experience":battle.exp,
            "gold":battle.gold
            }))

    @classmethod
    def send_update(cls, websocket, battle):
        websocket.write_message(json.dumps(
            {
            "type":"UPDATE",
            "user": battle.user.to_json,
            "monster":battle.monster.to_json,
            "text":battle.text
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
        self.lock = Lock()

    def start_battle(self, session):
        ''' Creates a battle instance and links it to an sid '''
        user = User.by_name(session.data['name'])
        self.lock.acquire()
        self.battles[session.id] = Battle(user)
        self.lock.release()
        return self.battles[session.id]

    def get_battle(self, session):
        if session.id in self.battles.keys():
            return self.battles[session.id]
        return None

    def remove_battle(self, session):
        if session.id in self.battles.keys():
            self.lock.acquire()
            del self.battles[session.id]
            self.lock.release()