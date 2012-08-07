# -*- coding: utf-8 -*-
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


import os
import imghdr
import logging

from uuid import uuid4
from base64 import b64encode, b64decode
from models import User
from models.Weapon import Weapon
from models.Armor import Armor
from mimetypes import guess_type
from libs.Form import Form
from libs.Session import SessionManager
from libs.SecurityDecorators import authenticated
from tornado.web import RequestHandler
from BaseHandlers import UserBaseHandler
from string import ascii_letters, digits
from recaptcha.client import captcha


class WelcomeUserHandler(UserBaseHandler):
    ''' This is the handler served when the user first logs in (Profile) '''

    @authenticated
    def get(self, *args, **kwargs):
        ''' Display the default user page '''
        user = self.get_current_user()
        self.render('user/home.html', user=user)

class EquipWeaponHandler(UserBaseHandler):
    ''' This is the handler that allows to equiping of weapons from the profile '''

    def initialize(self, dbsession):
        self.dbsession = dbsession
        self.session_manager = SessionManager.Instance()
        self.session = self.session_manager.get_session(
            self.get_secure_cookie('auth'), self.request.remote_ip)
        self.form = Form(
            weapon_id="You Must Select a Weapon"
        )

    @authenticated
    def post(self, *args, **kwargs):
        ''' Display the default user page '''
        user = self.get_current_user()
        if self.form.validate(self.request.arguments):
            if user != None and self.get_argument('weapon_id').isdigit():
                new_weapon = Weapon.by_id(self.get_argument('weapon_id'))
                # Make sure that we have the weapon they are attemping to equip
                if new_weapon in user.get_all_weapons():
                    old_weapon = user.equiped_weapon
                    old_weapon.equiped = False
                    new_weapon.equiped = True
                    self.dbsession.add(new_weapon)
                    self.dbsession.add(old_weapon)
                    self.dbsession.flush()
        self.redirect('/user')

class EquipArmorHandler(UserBaseHandler):
    ''' This is the handler that allows to equiping of armors from the profile '''

    def initialize(self, dbsession):
        self.dbsession = dbsession
        self.session_manager = SessionManager.Instance()
        self.session = self.session_manager.get_session(
            self.get_secure_cookie('auth'), self.request.remote_ip)
        self.form = Form(
            armor_id="You Must Select an Armor"
        )

    @authenticated
    def post(self, *args, **kwargs):
        ''' Display the default user page '''
        user = self.get_current_user()
        if self.form.validate(self.request.arguments):
            if user != None and self.get_argument('armor_id').isdigit():
                new_armor = Armor.by_id(self.get_argument('armor_id'))
                # Make sure that we have the weapon they are attemping to equip
                if new_armor in user.get_all_armor():
                    old_armor = user.equiped_armor
                    old_armor.equiped = False
                    new_armor.equiped = True
                    self.dbsession.add(new_armor)
                    self.dbsession.add(old_armor)
                    self.dbsession.flush()
        self.redirect('/user')

class SettingsHandler(RequestHandler):
    ''' Does NOT extend BaseUserHandler '''

    def initialize(self, dbsession):
        ''' Database and URI setup '''
        self.dbsession = dbsession
        self.session_manager = SessionManager.Instance()
        self.session = self.session_manager.get_session(
            self.get_secure_cookie('auth'), self.request.remote_ip)

    def get_current_user(self):
        ''' Returns the currently logged in user '''
        if self.session != None:
            return User.by_name(self.session.data['name'])
        return None

    @authenticated
    def get(self, *args, **kwargs):
        ''' Display the user settings '''
        self.render('user/settings.html', errors=None)

    @authenticated
    def post(self, *args, **kwargs):
        ''' Calls function based on parameter '''
        self.post_functions = {
            '/avatar': self.post_avatar,
            '/changepassword': self.post_password
        }
        if len(args) == 1 and args[0] in self.post_functions.keys():
            self.post_functions[args[0]]()
        else:
            self.render("public/404.html")

    def post_avatar(self):
        ''' Saves avatar - Reads file header an only allows approved formats '''
        user = self.get_current_user()
        if self.request.files.has_key('avatar') and len(self.request.files['avatar']) == 1:
            if len(self.request.files['avatar'][0]['body']) < (1024 * 1024):
                if user.avatar == "default_avatar.jpeg":
                    user.avatar = unicode(str(uuid4()))
                elif os.path.exists(self.application.settings['avatar_dir'] + '/' + user.avatar):
                    os.unlink(self.application.
                              settings['avatar_dir'] + '/' + user.avatar)
                ext = imghdr.what(
                    "", h=self.request.files['avatar'][0]['body'])
                if ext in ['png', 'jpeg', 'gif', 'bmp']:
                    user.avatar = user.avatar[:user.
                                              avatar.rfind('.')] + "." + ext
                    file_path = self.application.settings[
                        'avatar_dir'] + '/' + user.avatar
                    avatar = open(file_path, 'wb')
                    avatar.write(self.request.files['avatar'][0]['body'])
                    avatar.close()
                    self.dbsession.add(user)
                    self.dbsession.flush()
                    self.redirect("/user")
                else:
                    self.render("user/settings.html", errors=["Invalid image format"])
            else:
                self.render("user/settings.html", errors=["The image is too large"])
        else:
            self.render("user/settings.html", errors=["Please provide and image"])

    def post_password(self):
        ''' Changes a user's password '''
        form = Form(
            old_password='Please enter your current password',
            pass1='Please enter a new password',
            pass2='Please enter a new password',
        )
        if form.validate(self.request.arguments):
            user = self.get_current_user()
            if not user.validate_password(self.request.arguments['old_password'][0]):
                self.render("user/settings.html", errors=["Incorrect password"])
            elif not self.request.arguments['pass1'][0] == self.request.arguments['pass2'][0]:
                self.render("user/settings.html", errors=["Passwords do not match"])
            elif not 8 <= len(self.request.arguments['pass1'][0]):
                self.render("user/settings.html", errors=["Password must be at least 8 characters long"])
            else:
                user.password = self.request.arguments['pass1'][0]
                self.dbsession.add(user)
                self.dbsession.flush()
                self.redirect("/logout")
        else:
            self.render("user/settings.html", errors=form.errors)
                

class HighscoreHandler(UserBaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        '''Renders Highscore page'''
        user = self.get_current_user()
        self.render('public/highscore.html', user=user)

