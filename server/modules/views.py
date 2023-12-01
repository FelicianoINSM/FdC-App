from flask.views import MethodView
from flask import request, make_response
from .scripts import get_config, edit_config
from .db import SQLdb

class Home(MethodView):
    def get(self):
        return 'Hola Mundo'
    
    def post(self):
        data = request.get_json()
        return data
    
class Login(MethodView):
    def post(self):
        data = request.get_json()
        if data['usr'] == get_config('user') and data['pwd'] == get_config('password'):
            return make_response('', 200)
        else:
            return make_response('', 400)
        
class Aspersores(MethodView):
    def get(self):
        return {'state':get_config('state')}
    
    def post(self):
        data = request.get_json()
        try:
            new_state = data['state']
            edit_config('state', new_state)
            return make_response('', 200)
        except:
            return make_response('', 400)
    
class TyC(MethodView):
    def post(self):
        data = request.get_json()['tyc']
        try:
            edit_config('tyc', data)
            return make_response('', 200)
        except:
            return make_response('', 400)
    
    def get(self):
        return {'tyc':get_config('tyc')}

class Horarios(MethodView):
    def get(self):
        data = SQLdb().get_horarios()[0]
        ret = {'days':eval(data[0]), 'start':data[1], 'end':data[2]}
        return ret
    
    def post(self):
        data = request.get_json()
        try:
            SQLdb().edit_horarios(data)
            return make_response('', 200)
        except:
            return make_response('', 400)
