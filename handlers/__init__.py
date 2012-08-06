# -*- coding: utf-8 -*-
"""

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

-------
"""
import logging
import tornado.web
from tornado.web import Application
from tornado.web import StaticFileHandler 
from os import urandom, path
from base64 import b64encode
from handlers.BaseHandler import DefaultHandler
#Don't remove this comment, this is used as a pointhook to magically generate more handlers
#HANDLER_IMPORT_POINT_HOOK

logging.basicConfig(format = '[%(levelname)s] %(asctime)s - %(message)s', level = logging.DEBUG)

fileLogger = logging.FileHandler(filename = 'Arthur.log')
fileLogger.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(fileLogger)

application = Application([
        #Don't remove this comment, this is used as a pointhook to magically generate more handlers
        #HANDLER_APPLICATION_POINT_HOOK

        #Static Handlers - Serves static CSS, JavaScript and image files
        (r'/static/(.*)', StaticFileHandler, {'path': 'static'}),
      
        #This is the Default Handler generated for you!
      	(r'/(.*)', DefaultHandler)
],

    # Template directory
    template_path = 'templates',

    # Randomly generated secret key
    cookie_secret = b64encode(urandom(64)),

    # Debug mode
    debug = True,
    
    # Application version
    version = '0.0.1'
)

# Main entry point
def start_game():
     try:
          application.listen(8888)
          tornado.ioloop.IOLoop.instance().start()

     except KeyboardInterrupt:
          print "Shutting Down!"
