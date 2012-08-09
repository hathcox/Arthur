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

from models import User, Weapon, Armor
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
        ''' Renders Highscore page '''
        user = self.get_current_user()
        self.render('user/quest.html', user=self.get_current_user())


class QuestBattleHandler(UserBaseHandler):
    ''' This loads the starting point of a given battle '''
    
    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders Highscore page '''
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
        print message

    def on_close(self):
        logging.info("WebSocket closed with %s" % self.request.remote_ip)

    def handle_message(self, message):
        ''' State machine to deal with battle commands '''
        print message
        print message.type
        print message.sid
        session_manager = SessionManager.Instance()
        battle_Manager = BattleManager.Instance()
        if message.type == BattleMessage.START_BATTLE:
            session = session_manager.get_session(str(message.sid), str(self.request.remote_ip))
            if session != None:
                #Valid session, lets make a battle
                battle = battle_Manager.start_battle(session)
                #Send GO back to client
                BattleMessage.send_setup(self, battle.monster, battle.text)
            else:
                #Invalid session, send back to client
                BattleMessage.send_invalid(self)
        # if message.type == BattleMessage.ATTACK: