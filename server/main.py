from flask import Flask
from modules.views import Home, Login, Aspersores, TyC, Horarios
from modules.db import SQLdb

class Listener:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = SQLdb()

    def rules(self):
        self.app.add_url_rule('/', view_func=Home.as_view('home'))
        self.app.add_url_rule('/login', view_func=Login.as_view('login'))
        self.app.add_url_rule('/asp', view_func=Aspersores.as_view('asp'))
        self.app.add_url_rule('/tyc', view_func=TyC.as_view('tyc'))
        self.app.add_url_rule('/horarios', view_func=Horarios.as_view('horarios'))


    def run(self):
        self.db.create_tbls()
        self.rules()
        self.app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == '__main__':
    Listener().run()