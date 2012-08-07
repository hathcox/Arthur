# -*- coding: utf-8 -*-
'''
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
import tornado.web


from libs.ConsoleColors import *
from libs.Memcache import FileCache
from libs.ConfigManager import ConfigManager
from tornado.web import Application
from models import dbsession
from modules.Menu import Menu
from os import urandom, path
from base64 import b64encode
from handlers.StaticFileHandler import StaticFileHandler
from PublicHandlers import *
from UserHandlers import *
from ErrorHandlers import *


config = ConfigManager.Instance()
application = Application([

        #Static Handlers - Serves static CSS, JavaScript and image files
        (r'/static/(.*)', StaticFileHandler, {'path': 'static/'}),
      
        # User Handlers
        (r'/user', WelcomeUserHandler, {'dbsession': dbsession}),

        # Public Handlers
        (r'/login', LoginHandler),
        (r'/registration', RegistrationHandler, {'dbsession': dbsession}),
        (r'/about', AboutHandler),
        (r'/', HomePageHandler),

        #This is the Default Handler generated for you!
      	(r'/(.*)', NotFoundHandler),
        ],

    # Template directory
    template_path='templates',

    # Randomly generated secret key
    cookie_secret=b64encode(urandom(64)),

    # Debug mode
    debug=config.debug,

    # Enable XSRF forms
    xsrf_cookies=True,

    # Recaptcha Settings
    recaptcha_enable=config.recaptcha_enable,
    recaptcha_private_key=config.recaptcha_private_key,

    # WebSocket Host IP Address
    ws_ip_address=config.websocket_host,
    ws_port=config.listen_port,

    # UI Modules
    ui_modules={"Menu": Menu},
    
    # Application version
    version='0.1'
)

# Main entry point
def start_game():
    try:
        print("\r" + INFO + "Starting web server; binding to port %d" % config.listen_port)
        application.listen(config.listen_port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        FileCache.flush()
        print("\r" + WARN + "Shutting everything!")
