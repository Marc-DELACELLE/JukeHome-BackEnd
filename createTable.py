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
                user="killb",
                password="@0Z",
                host="",
                port=3306,
                database=db)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
#        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def query(self, *arg, **kwargs):
        self.cur.execute(*arg, **kwargs)
        return self.cur
    def querymany(self, *arg, **kwargs):
        self.cur.executemany(*arg, **kwargs)
        return self.cur
    def rollback(self):
        self.conn.rollback()

    def __del__(self):
        self.conn.close()



def selectall(dbmgr):
    for row in dbmgr.query("select * FROM users;"):
        print(row)

def callDB(table="IA_Track"):
    try:
        dbmgr = DatabaseManager(db)
        dbmgr.query("""
        CREATE TABLE if not exists users(
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
        CREATE TABLE if not exists party(
            id INT PRIMARY KEY AUTO_INCREMENT not null,
            name varchar(255),
            creator_id int not null
        );
        """)

        #data = [("jean", 23), ("olivier", 30), ("tom", 31)] 
        #dbmgr.querymany("INSERT INTO users(name, age) VALUES(?, ?);", data)
        #selectall(dbmgr)
        return "OK"

    except Exception as e:
        print(e)
        dbmgr.rollback()
        # raise e

@app.route('/')
def hello():
    total = callDB()
    print("TOTAL: ",total)
    return total
    return 'Hello, World!'

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