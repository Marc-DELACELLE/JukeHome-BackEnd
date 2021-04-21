from flask import Flask
import sqlite3

app = Flask(__name__)
# In RAM
#conn = sqlite3.connect(':memory:', check_same_thread = False) # Pas ouf ... 
# In API.db
#conn = sqlite3.connect('API.db', check_same_thread = False) # Pas ouf ... 

class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def query(self, *arg, **kwargs):
        self.cur.execute(*arg, **kwargs)
        self.conn.commit()
        return self.cur
    def querymany(self, *arg, **kwargs):
        self.cur.executemany(*arg, **kwargs)
        self.conn.commit()
        return self.cur
    def __del__(self):
        self.conn.close()


def a():
    print ("file")

def call_a_after(f):
  def decorate(*args, **kwargs):
    ret = f(*args, **kwargs)
    a()
    return ret
  return decorate

@call_a_after
def b(ahah,jpp, slt = ""):
    print (ahah)  
    print (jpp)  
    print ("hello")  
    return slt

def selectall(dbmgr):
    for row in dbmgr.query("select name, age FROM users"):
        print("ROW:" ,row)

def callDB(db=":memory:"):
    try:
        dbmgr = DatabaseManager(db)
        dbmgr.query("""
        CREATE TABLE if not exists users(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT,
            age INTERGER
        )
        """)
        data =( 
        {"name" : "jean", "age" : 23},
        {"name" : "olivier", "age" : 30}
        )
        dbmgr.querymany("INSERT INTO users(name, age) VALUES(:name, :age)", data)
        selectall(dbmgr)
        #for row in dbmgr.query("select name, age FROM users"):
        #    print("ROW:" ,row)
        return "OK"

    except sqlite3.OperationalError:
        print('Erreur la table existe déjà')
    except Exception as e:
        print(e)
        conn.rollback()
        # raise e

@app.route('/')
def hello():
    total = callDB()
    print("TOTAL: ",total)
    return total
    return 'Hello, World!'

if __name__ == "__main__":
    #print(b(ahah="o",jpp="l", slt="salut"))
    app.run(host='0.0.0.0', port=8000)
    #conn.close()
