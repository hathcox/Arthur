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
from libs.Battle import BattleManager
from libs.SecurityDecorators import authenticated
from tornado.web import RequestHandler
from BaseHandlers import UserBaseHandler

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
        self.render('user/battle.html', user=self.get_current_user())


class QuestWebsocketHandler(WebSocketHandler):
    ''' This deals with a quest when it happens '''

    def open(self):
        logging.info("WebSocket opened with %s" % self.request.remote_ip)
        print self.request.headers
        
    def on_message(self, message):
        pass

    def on_close(self):
        logging.info("WebSocket closed with %s" % self.request.remote_ip)