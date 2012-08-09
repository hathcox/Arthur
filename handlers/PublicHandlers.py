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


import logging

from models import User, Armor, Weapon
from libs.Form import Form
from libs.ConfigManager import ConfigManager
from libs.Session import SessionManager
from handlers.BaseHandlers import UserBaseHandler
from tornado.web import RequestHandler
from string import ascii_letters, digits

class HomePageHandler(RequestHandler):

    def get(self, *args, **kwargs):
        ''' Renders the about page '''
        self.render("public/home.html")


class LoginHandler(RequestHandler):
    ''' Takes care of the login process '''

    def initialize(self):
        self.form = Form(
            username="Enter a username",
            password="A password is required to login",
        )

    def get(self, *args, **kwargs):
        ''' Display the login page '''
        self.render('public/login.html', errors=None)

    def post(self, *args, **kwargs):
        ''' Checks submitted username and password '''
        if self.form.validate(self.request.arguments):
            user = User.by_name(self.request.arguments['username'][0])
            if user != None and user.validate_password(self.request.arguments['password'][0]):
                self.successful_login(user)
                self.redirect('/user')
            else:
                self.failed_login()
        else:
            self.render('public/login.html', errors=self.form.errors)

    def successful_login(self, user):
        ''' Called when a user successfully logs in '''
        logging.info("Successful login: %s from %s" % (user.name, self.request.remote_ip))
        session_manager = SessionManager.Instance()
        sid, session = session_manager.start_session()
        print "login handler", sid
        #We cant be http only for battles, this could open up security problems
        self.set_secure_cookie(name='auth', value=str(sid), expires_days=1)
        session.data['name'] = str(user.name)
        session.data['ip'] = str(self.request.remote_ip)
        if user.has_permission('admin'):
            session.data['menu'] = 'admin'
        else:
            session.data['menu'] = 'user'

    def failed_login(self):
        ''' Called if username or password is invalid '''
        logging.info("Failed login attempt from %s " % self.request.remote_ip)
        self.render('public/login.html', errors=["Bad username and/or password, try again"])


class RegistrationHandler(RequestHandler):
    ''' Registration Code '''

    def initialize(self, dbsession):
        self.dbsession = dbsession
        self.form = Form(
            username="Please enter an username",
            pass1="Please enter a password",
            pass2="Please confirm your password",
        )

    def get(self, *args, **kwargs):
        ''' Renders the registration page '''
        self.render("public/registration.html", errors=None)

    def post(self, *args, **kwargs):
        ''' Attempts to create an username, with shitty form validation '''
        if self.form.validate(self.request.arguments):
            config = ConfigManager.Instance()
            if User.by_name(self.request.arguments['username'][0]) != None:
                self.render('public/registration.html',
                            errors=['username name already taken'])
            elif not self.request.arguments['pass1'][0] == self.request.arguments['pass2'][0]:
                self.render(
                    'public/registration.html', errors=['Passwords do not match'])
            elif len(self.request.arguments['pass1'][0]) < 8:
                self.render('public/registration.html',
                            errors=['Passwords must be at least 8 characters'])
            else:
                self.create_user(self.request.arguments['username'][0],  self.request.arguments['pass1'][0])
                self.redirect("/login")
        elif 0 < len(self.form.errors):
            self.render('public/registration.html', errors=self.form.errors)
        else:
            self.render('public/registration.html', errors=['Unknown error'])

    def create_user(self, username, password):
        ''' Creates a user in the database '''
        user = User(
            name=unicode(username),
        )
        self.dbsession.add(user)
        self.dbsession.flush()
        user.password = password
        self.setup_new_weapon(user)
        self.setup_new_armor(user)
        self.dbsession.add(user)
        self.dbsession.flush()

    def setup_new_weapon(self, user):
        weapon = Weapon(
            user_id = user.id,
            name="Dagger",
            description="Slightly better than a butter knife",
            required_level=0,
            damage=10,
            advanced=False,
            classification="Sword",
            rating=10,
            avatar="/static/images/weapons/dagger.png",
            equiped = True,
        )
        self.dbsession.add(weapon)

    def setup_new_armor(self, user):
        armor = Armor(
            user_id = user.id,
            name="Simple Robe",
            description="Weak cloth to cover your disgusting naked body...",
            required_level=0,
            classification="Light Armor",
            rating=10,
            avatar="/static/images/armor/simple_robe.png",
            equiped = True,
        )
        self.dbsession.add(armor)


class AboutHandler(RequestHandler):

    def get(self, *args, **kwargs):
        ''' Renders the about page '''
        self.render('public/about.html')


class LogoutHandler(RequestHandler):

    def get(self, *args, **kwargs):
        ''' Clears cookies and session data '''
        session_manager = SessionManager.Instance()
        session_manager.remove_session(self.get_secure_cookie('auth'))
        self.clear_all_cookies()
        self.redirect("/")