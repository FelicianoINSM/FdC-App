import sqlite3 as sql
import json

class SQLdb:
    def con(self):
        con = sql.connect('./server/server.db')
        cur = con.cursor()
        return con, cur

    def create_tbls(self):
        con, cur = self.con()
        cur.execute('''CREATE TABLE IF NOT EXISTS horarios (
                    days TEXT,
                    start TIME,
                    end TIME    
        )''')

    def setup(self, cfg):
        con, cur = self.con()
        cur.execute('INSERT INTO horarios (days, start, end) VALUES (?, ?, ?)', (cfg['days'], cfg['start'], cfg['end'], ))
        con.commit()
        cur.close()
    
    def get_horarios(self):
        con, cur = self.con()
        cur.execute('SELECT * FROM horarios')
        data = cur.fetchall()
        return data
    
    def edit_horarios(self, cfg):
        con, cur = self.con()
        cur.execute('UPDATE horarios SET days = ?, start = ?, end = ?', (json.dumps(cfg['days']), cfg['start'], cfg['end'], ))
        con.commit()
        cur.close()

# if __name__ == '__main__':
#     db = SQLdb()
#     db.create_tbls()
#     db.setup({'days':json.dumps(['Lunes', 'Miercoles', 'Domingo']), 'start':'20:30', 'end':'20:45'})