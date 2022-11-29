from db import db
import json

def databases():
    query = "SELECT datname FROM pg_database"

    rs = db.execute(query)  
    result = []
    for (r) in rs:  
        result.append(r[0])
    
    return result 

def users():
    query = "SELECT name FROM users"

    rs = db.execute(query) 
    
    return json.dumps([(dict(row.items())) for row in rs])
