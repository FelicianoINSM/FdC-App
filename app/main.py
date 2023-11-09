from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

USER = 'admin'
PWD = '1234'

class Funcs(Screen):
    pass

class MainMenu(Screen):
    pass

class Login(Screen):

    def check(self):
        in_user = self.ids.user.text
        in_pwd = self.ids.pwd.text
        if in_user == USER and in_pwd == PWD:
            App.get_running_app().root.current = "funcs"


        else:
            self.ids.warning.text = "Usuario o Contraseña INCORRECTOS\nIntente ingresando los datos nuevamente"
    def test(self):
        print(self.ids.pwd.height)

class FdCyTApp(App):
    def build(self):
        return Builder.load_file("./main.kv")


if __name__ == '__main__':
    FdCyTApp().run()