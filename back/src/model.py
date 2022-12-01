from db import db
import json

def databases():
    query = "SELECT datname FROM pg_database"

    rs = db.execute(query)  
    return [row for row in rs]

def users():
    query = "SELECT id, name FROM users"

    rs = db.execute(query) 
    return [row for row in rs]