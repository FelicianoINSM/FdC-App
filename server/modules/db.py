import sqlite3 as sql

class SQLdb:
    def con(self):
        con = sql.connect('./server/server.db')
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