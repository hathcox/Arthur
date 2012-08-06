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
   

this sets up sqlalchemy.
for more information about sqlalchemy check out <a href="http://www.sqlalchemy.org/">www.sqlalchemy.org</a>
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer
from sqlalchemy.orm import sessionmaker
from models.BaseGameObject import BaseObject

metadata = BaseObject.metadata

# set the connection string here
engine = create_engine('mysql://user:password@localhost/Arthur')
Session = sessionmaker(bind=engine, autocommit=True)

# import the dbsession instance to execute queries on your database
dbsession = Session(autoflush = True)

# import models.
from models.BaseObject import BaseObject

# calling this will create the tables at the database
__create__ = lambda: (setattr(engine, 'echo', True), metadata.create_all(engine))
