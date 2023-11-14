from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.clock import Clock

TyC = '''
- Obligación de Cuidado de las Instalaciones:

Cualquier daño o mal funcionamiento de las instalaciones debido a un uso negligente por parte del usuario o un descuido del mismo puede resultar en la terminación de su acceso al Programa. 

Si su problema es un error de la App, los desarrolladores estaremos abiertos a recibir críticas y a otorgar ayuda o mantenimiento si así fuese necesario. Los teléfonos de contacto están a su disposición si necesita contactarse con el soporte técnico de la aplicación

El usuario se compromete a utilizar el Programa de acuerdo con las leyes y regulaciones locales aplicables, tratando de no ocasionar ninguna colisión a propósito

- Uso Responsable:

El usuario se compromete a hacer uso del Programa de conformidad con todas las leyes y reglamentos establecidos por los desarrolladores .

Queda terminantemente prohibido el empleo del Programa con propósitos ilegales, incluyendo cualquier alteración no autorizada de las instalaciones de riego o un uso con intenciones de romper el sistema instalado.

- Derechos de Propiedad:

La totalidad de los derechos de propiedad intelectual relacionados con el Programa, abarcando el software, la interfaz de usuario y cualquier contenido proporcionado, ostentan un carácter de exclusividad en manos de los titulares del Programa.

- Modificaciones en los Términos y Condiciones:

El titular del Programa conserva el derecho de modificar estos términos y condiciones en cualquier momento. Las modificaciones surtirán efecto inmediatamente tras su publicación en el sitio web o la aplicación. Corresponde al usuario la responsabilidad de revisar con periodicidad los términos actualizados.

- Terminación:

El titular del Programa se reserva el derecho de suspender o poner fin al acceso del usuario al Programa en caso de incumplimiento de estos términos y condiciones o mal uso del mismo.
'''
USER = ''
PWD = ''

class CustomPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.tyc_label.text = TyC

class Login(Screen):
    def on_enter(self):
        Clock.schedule_once(self.pop)

    def pop(self, dt):
        popup = CustomPopup()
        popup.open()

    def check(self):
        in_user = self.ids.user.text
        in_pwd = self.ids.pwd.text
        if in_user == USER and in_pwd == PWD:
            App.get_running_app().root.current = "main"
        else:
            self.ids.warning.text = "Usuario o Contraseña INCORRECTOS!\nIntente ingresando los datos nuevamente."

class MainMenu(Screen):
    pass     

class Aspersores(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.condition = 0

    def on_enter(self):
        self.condition = 0
        Clock.schedule_once(self.state_check)

    def state_check(self, dn):
        match self.condition:
            case 0: 
                self.ids.state_lbl.text = 'Estado: [color=84F19C]APAGADO[/color]'
                self.ids.state_btn.text = 'Encender'
                self.ids.state_btn.disabled = False
            case 1: 
                self.ids.state_lbl.text = 'Estado: [color=FF5555]ENCENDIDO[/color]'
                self.ids.state_btn.text = 'Apagar'
                self.ids.state_btn.disabled = False
            case 2: 
                self.ids.state_lbl.text = 'Estado: [color=FFF355]ERROR[/color]'
                self.ids.state_btn.text = '...'
                self.ids.state_btn.disabled = True

    def change_state(self):
        self.condition += 1
        if self.condition > 2: self.condition = 0
        self.state_check('')

class Horarios(Screen):
    pass     
class Datos(Screen):
    pass     
class Historial(Screen):
    pass     



class FdCyTApp(App):
    def build(self):
        return Builder.load_file("./main.kv")


if __name__ == '__main__':
    FdCyTApp().run()