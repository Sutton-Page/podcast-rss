import sqlite3
from sqlite3 import Error

db_path = "db//podcast.db"

schema = "db_schema.sql"

db = sqlite3.connect(db_path)

script = open(schema,"r").read()

db.executescript(script)

db.close()

            
