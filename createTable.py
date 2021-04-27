#!/usr/bin/python3

import mariadb
from flask import Flask
import sys

app = Flask(__name__)
# In RAM
#conn = sqlite3.connect(':memory:', check_same_thread = False) # Pas ouf ... 
# In API.db
#conn = sqlite3.connect('API.db', check_same_thread = False) # Pas ouf ... 

class DatabaseManager(object):
    def __init__(self, table):
        try:
            self.conn = mariadb.connect(
                user="devs",
                password="P@5s",
                host="",
                port=3306)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.conn.autocommit = True # Turn to False for manual commit and rollback
        self.cur = self.conn.cursor()

    def query(self, *arg, **kwargs):
        self.cur.execute(*arg, **kwargs)
        return self.cur
    def querymany(self, *arg, **kwargs):
        self.cur.executemany(*arg, **kwargs)
        return self.cur
    def rollback(self): # Only for manual commit
        self.conn.rollback()

    def __del__(self):
        self.conn.close()

dbmgr = DatabaseManager("IA_Track")


def selectall(dbmgr, table="users"):
    all = ""
    for row in dbmgr.query("select * FROM " + table):
        all += str(row) + "\n"
        # print(row) # DEBUG
    return all

def callDB(table="IA_Track"):
    try:
        dbmgr.query("USE " + table + ";")
        dbmgr.query("""
        CREATE TABLE if not exists users (
            id INT PRIMARY KEY AUTO_INCREMENT not null,
            forname varchar(255),
            name varchar(255),
            email varchar(255),
            photo blob default null,
            spotify_token varchar(255),
            premium boolean not null default False,
            age tinyINT unsigned default null
        );
        """)
        dbmgr.query("""
        CREATE TABLE if not exists party (
            id INT PRIMARY KEY AUTO_INCREMENT not null,
            name varchar(255),
            creator_id int not null
        );
        """)

        #data =                             [("Phil",  "Plante", "phil.plante@gmail.com", None,  "@s89D@s",    False,   28)] 
        #dbmgr.querymany("""INSERT INTO users(forname, name,     email,                   photo, spotify_token, premium, age)
        #                              VALUES(?,       ?,         ?,                       ?,     ?,             ?,        ?);""", data)
        all = selectall(dbmgr, "users")
        return all

    except Exception as e:
        print(e)
        dbmgr.rollback()
        # raise e

@app.route('/')
def hello():
    total = callDB()
    print("DEBUG: ",total)
    return total

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

#def a():
#    print ("file")
#
#def call_a_after(f):
#  def decorate(*args, **kwargs):
#    ret = f(*args, **kwargs)
#    a()
#    return ret
#  return decorate
#
#@call_a_after
#def b(ahah,jpp, slt = ""):
#    print (ahah)  
#    print (jpp)  
#    print ("hello")  
#    return slt