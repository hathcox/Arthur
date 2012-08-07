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


import os
import sys
import getpass

from libs.ConsoleColors import *
from libs.ConfigManager import ConfigManager
from models import dbsession, User, Permission, ArmoryWeapon, ArmoryArmor


# Fills the database with some startup data.
config = ConfigManager.Instance()

if config.debug:
    password = 'nimda123'
else:
    sys.stdout.write(PROMPT + "New Admin ")
    sys.stdout.flush()
    password1 = getpass.getpass()
    sys.stdout.write(PROMPT + "Confirm New Admin ")
    sys.stdout.flush()
    password2 = getpass.getpass()
    if password1 == password2 and 12 <= len(password1):
        password = password1
    else:
        print WARN + 'Error: Passwords did not match, or were less than 12 chars'
        os._exit(1)

# User Account
user = User(
    name=unicode('admin'),
)
dbsession.add(user)
dbsession.flush()
user.password = password
dbsession.add(user)
dbsession.flush()
permission = Permission(
    name=unicode('admin'),
    user_id=user.id
)
dbsession.add(permission)
dbsession.flush()

##### BOOT STRAP ITEMS ##### 
weapon = ArmoryWeapon(
    name="Short Sword",
    description="A very short blade",
    required_level=0,
    cost=50,
    damage=20,
    advanced=False,
    classification="Sword",
    rating=20,
    avatar="/static/images/weapons/short_sword.png",
)
dbsession.add(weapon)
dbsession.flush()

weapon = ArmoryWeapon(
    name="Small Knife",
    description="Slightly better than a butter knife",
    required_level=0,
    cost=50,
    damage=10,
    advanced=False,
    classification="Sword",
    rating=10,
    avatar="/static/images/weapons/small_knife.png",
)
dbsession.add(weapon)
dbsession.flush()

armor = ArmoryArmor(
    name="Leather Straps",
    description="Weak armor",
    required_level=0,
    cost=50,
    classification="Light Armor",
    rating=10,
    avatar="/static/images/weapons/leather_straps.png",
)
dbsession.add(armor)
dbsession.flush()


#### CONSOLE #### 
if config.debug:
    environ = bold + R + "Developement boot strap" + W
    details = ", default admin password is '%s'." % password
else:
    environ = bold + "Production boot strap" + W
    details = '.'
print INFO + '%s completed successfully%s' % (environ, details)
