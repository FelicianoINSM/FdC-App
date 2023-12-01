import sqlite3 as sql
import random

class SQLdb:
    def con(self):
        con = sql.connect('./server/server.db')
        cur = con.cursor()
        return con, cur

    def create_tbls(self):
        con, cur = self.con()
        cur.execute('''CREATE TABLE IF NOT EXISTS day_info (
                    temp REAL,
                    hum REAL,
                    last TEXT    
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS historial (
                    fecha DATE,
                    hora_inicio TIME,
                    hora_fin TIME,
                    humedad INTEGER,
                    litros INTEGER
        )''')

    def setup(self):
        con, cur = self.con()
        cur.execute('INSERT INTO day_info (temp, hum, last) VALUES (0, 0, "Undefined")')
        fechas = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
        for fecha in fechas:
            hora = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
            numero = random.randint(10, 100)
            valores = (fecha, hora, hora, numero, numero)
            cur.execute('INSERT INTO historial (fecha, hora_inicio, hora_fin, humedad, litros) VALUES (?, ?, ?, ?, ?)', valores)
        con.commit()
        cur.close()

    
    def get_day_info(self):
        con, cur = self.con()
        cur.execute('SELECT * FROM day_info')
        data = cur.fetchall()
        return data[0]

    def get_history(self):
        con, cur = self.con()
        cur.execute('SELECT * FROM historial')
        data = cur.fetchall()
        print(data)
        return data

    def upd_day_info(self, data):
        con, cur = self.con()
        cur.execute('UPDATE day_info SET temp = ?, hum = ?, last = ?', (data[0], data[1], data[2]))
        con.commit()
        cur.close()

# if __name__ == '__main__':
#     db = SQLdb()
#     db.create_tbls()
#     db.get_history()