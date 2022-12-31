import sqlite3
import json
import pandas as pd

database = 'ToDo.db'

conn = sqlite3.connect(database, check_same_thread=False)
conn.execute('pragma foreign_keys=ON')

conn.execute('''CREATE TABLE if not exists Dailies
(id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
monday TEXT NOT NULL,
tuesday TEXT NOT NULL,
wednesday TEXT NOT NULL,
thursday TEXT NOT NULL,
friday TEXT NOT NULL,
saturday TEXT NOT NULL,
sunday TEXT NOT NULL);''')


