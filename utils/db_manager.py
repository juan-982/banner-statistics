import sqlite3
import os

_DB_DIR = "db"
_DB_NAME = "banner.db"
DB_PATH = _DB_DIR + "/" + _DB_NAME

_SCRIPTS_DIR = "scripts"
_SCRIPTS = [
  "create_tables.sql",
]

def initialize():
    if not os.path.exists(_DB_DIR):
        os.makedirs(_DB_DIR)
        
    if not os.path.exists(DB_PATH):
        cursor = sqlite3.connect(DB_PATH).cursor()

        for script in _SCRIPTS:
            cursor.executescript(open(_SCRIPTS_DIR + "/" + script).read())
