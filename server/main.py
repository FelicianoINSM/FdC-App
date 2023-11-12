from flask import Flask

class Listener:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/', methods=["GET"])
        def home():
            return 'Hi'

    def run(self):
        self.app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == '__main__':
    Listener().run()