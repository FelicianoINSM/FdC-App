from flask.views import MethodView
from .scripts import get_config



class HomeView(MethodView):
    def get(self):
        usr = get_config('user')
        pwd = get_config('password')
        text = f'User: {usr} <br/> Password: {pwd}'
        return text