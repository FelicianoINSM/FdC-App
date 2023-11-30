from flask.views import MethodView
from flask import request
from .scripts import get_config

class Home(MethodView):
    def get(self):
        return 'Hola Mundo'
    
    def post(self):
        data = request.get_json()
        return data

    
