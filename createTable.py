#!/usr/bin/python3

import mariadb
from flask import Flask, request
import sys

app = Flask(__name__)

class DatabaseManager(object):
    def __init__(self, table):
        try:
            self.conn = mariadb.connect(
                user="devs",
                password="P@5s",
                host="",
                port=3306,
                database=table)
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

def callDB():#db="IA_Track"):
    try:
        #dbmgr.query("USE " + db + ";")
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
            creator_id int not null,
            name varchar(255)
        );
        """)
        dbmgr.query("""
        CREATE TABLE if not exists music (
            id INT PRIMARY KEY AUTO_INCREMENT not null,
            party_id int not null,
            id_music varchar(255),
            music_name varchar(255),
            author_name varchar(255),
            album_name varchar(255)
        );
        """)

        all = selectall(dbmgr, "users")
        return all

    except Exception as e:
        print(e)
        dbmgr.rollback()
        # raise e

@app.route('/insert')
def testInsertUser():
    data =                             [("Phil",  "Plante", "phil.plante@gmail.com", None,  "@s89D@s",     False,   28)]
    dbmgr.querymany("""INSERT INTO users(forname, name,     email,                   photo, spotify_token, premium, age)
                                  VALUES(?,       ?,        ?,                       ?,     ?,             ?,       ?);""", data)

@app.route('/')
def hello():
    #data = {"name": "Jean", "forname": "Bitch", "spotify_token":"random", "email": "wesh" }
    #total = callDB() 
    total = addToTableUsers(name="Jean", forname= "Bitch", spotify_token=None, email= "wesh", age=11)
    print("DEBUG: ",total)
    return total

def createPlaylist(party_id):
    data = [
        ("Fuego", "Alok", "Fuego"),
        ("Au soleil", "Jenifer", "Jenifer"),
        ("Old Town Road", "Lil Nas X", "7 EP"),
        ("Bad boy", "Marwa Loud", "Loud")
    ]
    dbmgr.querymany("""Insert Into music (party_id,       music_name, author_name, album_name)
                                  VALUES ("""+party_id+", ?,          ?,           ?);", data)

@app.route('/playlist', methods = ['POST', 'GET'])
def getPlaylist():
    if request.method == 'POST':
        spotify_token = request.form['spotify_token']
        party_id = request.form['party_id']
    elif request.method == 'GET':
        spotify_token = request.args.get('spotify_token')
        party_id = request.args.get('party_id')
    else:
        print("Error: Not POST nor GET")
        return "Method Not Allowed", 405

    if (not spotify_token or not party_id):
        # print("Error: Bad Request")
        # return "Bad Request", 400
        spotify_token = "123456"
        party_id = 1
    
    #createPlaylist(party_id)

    all = ""
    for music in dbmgr.query("""Select music_name, author_name, album_name FROM music where party_id = ?;""", (party_id,)):
        print(music)
        all += str(music)
    print("ALL:", all)
    return all


#####                                     Select * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users' and TABLE_SCHEMA = 'IA_Track';

#+---------------+--------------+------------+---------------+------------------+----------------+-------------+-----------+--------------------------+------------------------+-------------------+---------------+--------------------+--------------------+-------------------+---------------------+------------+----------------+---------------------------------+----------------+--------------+-----------------------+
#| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME   | ORDINAL_POSITION | COLUMN_DEFAULT | IS_NULLABLE | DATA_TYPE | CHARACTER_MAXIMUM_LENGTH | CHARACTER_OCTET_LENGTH | NUMERIC_PRECISION | NUMERIC_SCALE | DATETIME_PRECISION | CHARACTER_SET_NAME | COLLATION_NAME    | COLUMN_TYPE         | COLUMN_KEY | EXTRA          | PRIVILEGES                      | COLUMN_COMMENT | IS_GENERATED | GENERATION_EXPRESSION |
#+---------------+--------------+------------+---------------+------------------+----------------+-------------+-----------+--------------------------+------------------------+-------------------+---------------+--------------------+--------------------+-------------------+---------------------+------------+----------------+---------------------------------+----------------+--------------+-----------------------+
#| def           | IA_Track     | users      | id            |                1 | NULL           | NO          | int       |                     NULL |                   NULL |                10 |             0 |               NULL | NULL               | NULL              | int(11)             | PRI        | auto_increment | select,insert,update,references |                | NEVER        | NULL                  |
#| def           | IA_Track     | users      | forname       |                2 | NULL           | YES         | varchar   |                      255 |                    255 |              NULL |          NULL |               NULL | latin1             | latin1_swedish_ci | varchar(255)        |            |                | select,insert,update,references |                | NEVER        | NULL                  |
#| def           | IA_Track     | users      | name          |                3 | NULL           | YES         | varchar   |                      255 |                    255 |              NULL |          NULL |               NULL | latin1             | latin1_swedish_ci | varchar(255)        |            |                | select,insert,update,references |                | NEVER        | NULL                  |
#| def           | IA_Track     | users      | email         |                4 | NULL           | YES         | varchar   |                      255 |                    255 |              NULL |          NULL |               NULL | latin1             | latin1_swedish_ci | varchar(255)        |            |                | select,insert,update,references |                | NEVER        | NULL                  |
#| def           | IA_Track     | users      | photo         |                5 | NULL           | YES         | blob      |                    65535 |                  65535 |              NULL |          NULL |               NULL | NULL               | NULL              | blob                |            |                | select,insert,update,references |                | NEVER        | NULL                  |
#| def           | IA_Track     | users      | spotify_token |                6 | NULL           | YES         | varchar   |                      255 |                    255 |              NULL |          NULL |               NULL | latin1             | latin1_swedish_ci | varchar(255)        |            |                | select,insert,update,references |                | NEVER        | NULL                  |
#| def           | IA_Track     | users      | premium       |                7 | 0              | NO          | tinyint   |                     NULL |                   NULL |                 3 |             0 |               NULL | NULL               | NULL              | tinyint(1)          |            |                | select,insert,update,references |                | NEVER        | NULL                  |
#| def           | IA_Track     | users      | age           |                8 | NULL           | YES         | tinyint   |                     NULL |                   NULL |                 3 |             0 |               NULL | NULL               | NULL              | tinyint(3) unsigned |            |                | select,insert,update,references |                | NEVER        | NULL                  |
#+---------------+--------------+------------+---------------+------------------+----------------+-------------+-----------+--------------------------+------------------------+-------------------+---------------+--------------------+--------------------+-------------------+---------------------+------------+----------------+---------------------------------+----------------+--------------+-----------------------+


def getInfoTable(table):
    ret = dbmgr.query("Select COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + table + "' and TABLE_SCHEMA = 'IA_Track';")
    mustHave = []
    for must in ret:
        mustHave += [must[0]] # Change [0] if it's not just COLUMN_NAME
    return mustHave

def addToTable(table, mustInTable, *args, **kwargs):
    keys = ""
    values = ""
    for key,value in (kwargs.items()):
        print(key, ":", value)
        
        if (key not in mustInTable):
            print("ERROR:", key, "not in table's columns!")
            return
        if (value == None):
            value = "NULL"
        else:
            value = "'" + str(value) + "'"
        if (keys):
            keys += ", " + key
            values += ", " + value
        else:
            keys += key
            values += value
    #dbmgr.query("INSERT INTO users("+keys+") VALUES ("+values+");")




def addToTableUsers(*args, **kwargs):
    table = "users"
    mustInTable = getInfoTable(table)
    if (mustInTable):
        addToTable(table, mustInTable, *args, **kwargs)
    return "addToTableUsers"

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

