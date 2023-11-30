from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.button import Button

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

class Time(Popup):
    pass


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
    def __init__(self, **kw):
        super().__init__(**kw)

        self.days = {
            'Lunes': False,
            'Martes': False,
            'Miercoles': False,
            'Jueves': False,
            'Viernes': False,
            'Sabado': False,
            'Domingo': False,
        }
    
    def on_enter(self):
        Clock.schedule_once(self.precfg)
    
    def precfg(self, x):
        # config_data = GET CONFIG FROM SOMEWHERE
        config_data = {'days':['Lunes', 'Miercoles', 'Domingo'], 'start':'20:30', 'end':'20:45'}
        if 'days' in config_data:
            for day in config_data['days']:
                mth = self.get_btn(day)
                if mth:
                    mth.background_color = [0.52, 0.95, 0.61, 1]
                    self.days[day] = True

        if 'start' in config_data:
            hrs = config_data['start'].split(':')[0]
            mins = config_data['start'].split(':')[1]
            self.ids.start_hrs.text = hrs
            self.ids.start_mins.text = mins

        if 'end' in config_data:
            hrs = config_data['end'].split(':')[0]
            mins = config_data['end'].split(':')[1]
            self.ids.end_hrs.text = hrs
            self.ids.end_mins.text = mins

    def get_btn(self, day):
        grid = self.ids.btns
        for widget in grid.children:
            if widget.text == day:
                return widget
        return False

    def toggle(self, button):
        dia = button.text
        if not self.days[dia]:
            self.days[dia] = True
            button.background_color = (0.52, 0.95, 0.61, 1)
        else:
            self.days[dia] = False
            button.background_color = (0.85, 0.85, 0.85, 1)  # Cambiar a color original

    def save(self):
        days = [dia for dia, valor in self.days.items() if valor]
        start = f'{self.ids.start_hrs.text}:{self.ids.start_mins.text}'
        end = f'{self.ids.end_hrs.text}:{self.ids.end_mins.text}'
        data = {'days':days, 'start':start, 'end':end}
        print(data)

class Datos(Screen):
    pass     
class Historial(Screen):
    pass     



class FdCyTApp(App):
    def build(self):
        return Builder.load_file("./main.kv")


if __name__ == '__main__':
    FdCyTApp().run()