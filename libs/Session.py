'''
Created on Mar 13, 2012

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
from threading import Lock
from libs.Singleton import *
from datetime import datetime, timedelta
from string import ascii_letters, digits

SID_SIZE = 24
SESSION_TIME = 60


@Singleton
class SessionManager():
    ''' Mostly thread safe session manager '''

    def __init__(self):
        self.sessions = {}
        self.sessions_lock = Lock()

    def start_session(self):
        ''' Creates a new session and returns the session id and the new session object '''
        sid = self.filter_string(b64encode(urandom(SID_SIZE)))
        self.sessions_lock.acquire()
        self.sessions[sid] = Session(sid)
        self.sessions_lock.release()
        return sid, self.sessions[sid]

    def filter_string(self, string, extra_chars=''):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)

    def remove_session(self, sid):
        ''' Removes a given session '''
        if sid in self.sessions.keys():
            self.sessions_lock.acquire()
            del self.sessions[sid]
            self.sessions_lock.release()

    def get_session(self, sid, ip_address):
        ''' Returns a session object if it exists or None '''
        if sid in self.sessions.keys():
            if self.sessions[sid].is_expired():
                self.remove_session(sid)
            elif self.sessions[sid].data['ip'] == ip_address:
                return self.sessions[sid]
        return None

    def get_session_alternate(self, sid):
        if sid in self.sessions.keys():
            if self.sessions[sid].is_expired():
                self.remove_session(sid)
            else:
                return self.sessions[sid]

    def clean_up(self):
        ''' Removes all expired sessions '''
        for sid in self.sessions.keys():
            if self.sessions[sid].is_expired():
                self.sessions_lock.acquire()
                del self.sessions[sid]
                self.sessions_lock.release()


class Session():
    ''' Session object stores data, time, id '''

    def __init__(self, sid):
        self.id = sid
        self.data = {}
        self.expiration = datetime.now() + timedelta(minutes=SESSION_TIME)

    def is_expired(self):
        ''' Returns boolean based on if session has expired '''
        return (timedelta(0) < (datetime.now() - self.expiration))
