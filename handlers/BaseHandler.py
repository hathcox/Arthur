'''
Created on Mar 15, 2012

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
from tornado.web import RequestHandler

class DefaultHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("main.html")

    def post(self, *args, **kwargs):
        self.render("main.html")

class WelcomeHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("public/welcome.html")

    def post(self, *args, **kwargs):
        self.render("main.html")