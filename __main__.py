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


from libs.ConsoleColors import *
from libs.ConfigManager import ConfigManager
from sys import argv
from handlers import start_game
from models import __create__, boot_strap


def serve():
    '''
    serves the application
    ----------------------
    '''
    start_game()

def create():
    print(INFO + 'Creating the database ... ')
    __create__()
    if len(argv) == 3 and argv[2] == 'bootstrap':
        print(INFO + 'Bootstrapping the database ... ')
        boot_strap()

options = {
    'serve': serve,
    'create': create,
}

if argv[1] in options.keys():
    options[argv[1]]()
