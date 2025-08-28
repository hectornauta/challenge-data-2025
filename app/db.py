import sqlite3

def get_connection():
    conn = sqlite3.connect('data/db/db_challenge.db')
    return conn