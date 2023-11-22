from flask import Flask
import sqlite3 as sql
from flask import request


class SQLdb:
    def __init__(self) -> None:
        pass

    def con(self):
        con = sql.connect('test.db')
        cur = con.cursor()
        return con, cur

    def create_tbls(self):
        con, cur = self.con()
        cur.execute('''CREATE TABLE IF NOT EXISTS test (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT    
        )''')

    def post(self, name):
        con, cur = self.con()
        cur.execute('INSERT INTO test (name) VALUES (?)', (name,))
        con.commit()
        cur.close()
        return 'Success'

    def get(self, x):
        con, cur = self.con()
        cur.execute('SELECT name FROM test WHERE id = ?', (x, ))
        data = cur.fetchall()[0][0]
        print(data)
        return data

class Listener:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = SQLdb()

        @self.app.route('/', methods=["GET"])
        def home():
            return 'Hi'
        
        @self.app.route('/test', methods=["POST"])
        def receive():
            data = request.get_json()
            x = data.get('id')
            return self.db.get(x)

    def run(self):
        self.db.create_tbls()
        self.app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == '__main__':
    Listener().run()