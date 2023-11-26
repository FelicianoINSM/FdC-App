from flask import Flask
from modules.views import HomeView
from modules.db import SQLdb

class Listener:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = SQLdb()

    def rules(self):
        self.app.add_url_rule('/', view_func=HomeView.as_view('home'))

    def run(self):
        self.db.create_tbls()
        self.rules()
        self.app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == '__main__':
    Listener().run()