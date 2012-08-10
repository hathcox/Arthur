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


import logging

from models import User, Weapon, Armor, Quest
from libs.Form import Form
from libs.Session import SessionManager
from libs.SecurityDecorators import authenticated
from tornado.web import RequestHandler
from BaseHandlers import UserBaseHandler
from libs.Battle import Battle, BattleMessage, BattleManager
from tornado.websocket import WebSocketHandler


class QuestHomeHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders Quest page '''
        user = self.get_current_user()
        quest = Quest.by_id(user.quest_level)
        self.render('user/quest.html', user=self.get_current_user(), quest=quest)

class QuestRetreatHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        ''' Retreats from the current quest '''
        user = self.get_current_user()
        quest = Quest.by_id(user.quest_level)
        user.quest_level -=1
        user.quest_level = max(user.quest_level, 1)
        user.current_quest_battle = 0
        self.dbsession.add(user)
        self.dbsession.flush()
        self.redirect('/user/quest')



class QuestBattleHandler(UserBaseHandler):
    ''' This loads the starting point of a given battle '''
    
    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders Battle page '''
        auth_cookie = self.get_secure_cookie('auth')
        self.render('user/battle.html', user=self.get_current_user(), auth=auth_cookie)


class QuestWebsocketHandler(WebSocketHandler):
    ''' This deals with a quest when it happens '''

    def open(self):
        logging.info("WebSocket opened with %s" % self.request.remote_ip)
        
    def on_message(self, message):
        client_message = BattleMessage(message)
        #If the message translated to a format we know
        if(client_message.valid):
            #State machine time
            self.handle_message(client_message)

    def on_close(self):
        logging.info("WebSocket closed with %s" % self.request.remote_ip)

    def handle_message(self, message):
        ''' State machine to deal with battle commands '''
        session_manager = SessionManager.Instance()
        battle_manager = BattleManager.Instance()
        session = session_manager.get_session_alternate(str(message.sid))
        if session != None:
            if message.type == BattleMessage.START_BATTLE:
                    #Valid session, lets make a battle
                    battle = battle_manager.start_battle(session)
                    #Send GO back to client
                    BattleMessage.send_setup(self, battle.monster, battle.text)
                    BattleMessage.send_go(self)
            else:
                battle = battle_manager.get_battle(session)
                if battle != None:
                    #Make sure the battle isn't over
                    if not battle.check_ended():
                        #If it is the user's turn
                        if battle.turn:
                            if not battle.check_ended():
                                #play the user's turn
                                battle.do_user_round(message.type)
                                #Send the update
                                BattleMessage.send_update(self, battle)
                            else:
                                #The battle has ended send it to the client
                                BattleMessage.send_end(self, battle)
                                battle_manager.remove_battle(session)
                            if not battle.check_ended():
                                #play the computer's turn
                                battle.do_computer_round()
                                #Send the update
                                BattleMessage.send_update(self, battle)
                            else:
                                #The battle has ended send it to the client
                                BattleMessage.send_end(self, battle)
                                battle_manager.remove_battle(session)
                            #Final check to make sure we have another round to do
                            if battle.check_ended():
                                #The battle has ended send it to the client
                                BattleMessage.send_end(self, battle)
                                battle_manager.remove_battle(session)
                        else:
                            #It's not our turn yet
                            BattleMessage.send_wait(self)
                    else:
                        #The battle has ended send it to the client
                        BattleMessage.send_end(self, battle)
                        battle_manager.remove_battle(session)
                else:
                    #No battle linked to that session
                    BattleMessage.send_invalid(self)
        else:
            #Invalid session, send back to client
            BattleMessage.send_invalid(self)