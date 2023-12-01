from flask.views import MethodView
from flask import request, jsonify
from .scripts import get_config
from .db import SQLdb

class Home(MethodView):
    def get(self):
        return 'Hola Mundo'
    
    def post(self):
        data = request.get_json()
        return data
    
class DayInfo(MethodView):
    def get(self):
        data = SQLdb().get_day_info()
        temp, hum, last = data
        return jsonify({'temp':temp, 'hum':hum, 'last':last})
    
class Historial(MethodView):
    def get(self):
        data = SQLdb().get_history()
        ret = []
        for i in data:
            fecha, inicio, final, humedad, temperatura = i
            form = {'fecha':fecha, 'inicio':inicio, 'final':final, 'humedad':humedad, 'temperatura':temperatura}
            ret.append(form)
        return ret
