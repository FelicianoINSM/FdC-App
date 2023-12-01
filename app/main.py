from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from os import listdir
from kivy.clock import Clock
import requests
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.popup import Popup

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

class Server:
    def __init__(self) -> None:
        self.address = 'http://192.168.35.116:8080'

    def login(self, usr, pwd):
        url = f'{self.address}/login'
        data = {'usr':usr, 'pwd':pwd}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True
        else:
            return False
    
    def asp_state(self):
        url = f'{self.address}/asp'
        response = requests.get(url).json()
        if response['state'] == 'on':
            return 1
        elif response['state'] == 'off':
            return 0
        else: 
            return 2
    
    def change_asp_state(self, new_state):
        url = f'{self.address}/asp'
        data = {'state':new_state}
        response = requests.post(url, json=data)
        return response.status_code
    
    def accept_tyc(self):
        url = f'{self.address}/tyc'
        data = {'tyc':'off'}
        response = requests.post(url, json=data)
        return response.status_code

    def get_tyc_state(self):
        url = f'{self.address}/tyc'
        response = requests.get(url)
        return eval(response.text)
    
    def get_horarios(self):
        url = f'{self.address}/horarios'
        response = requests.get(url)
        return eval(response.text)
    
    def edit_horarios(self, cfg):
        url = f'{self.address}/horarios'
        response = requests.post(url, json=cfg)
        return response.status_code
    
    def day(self):
        url = f'{self.address}/day'
        response = requests.get(url)
        return response.text
    
    def historial(self):
        url = f'{self.address}/hist'
        response = requests.get(url)
        return response.text
    
class CustomPopup(Popup):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.ids.tyc_label.text = text
    def accept(self):
        Server().accept_tyc()
        self.dismiss()

class PreguntaPopup(Popup):
    def __init__(self, text, **kwargs):
        super(PreguntaPopup, self).__init__(**kwargs)
        self.ids.pop_label.text = text

class DropDownItem(GridLayout):
    def __init__(self, obj_info, **kwargs):
        super(DropDownItem, self).__init__(padding=10, cols=5, height=40, **kwargs)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        for data in obj_info:
            label = Label(text=str(obj_info[data]), color=(1, 1, 1, 1))
            self.add_widget(label)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class DropDownScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(DropDownScrollView, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=dp(15), size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        data = eval(Server().historial())
        for i in data:
            item = DropDownItem(i)
            self.layout.add_widget(item)

        self.add_widget(self.layout)

class Login(Screen):
    def on_enter(self):
        Clock.schedule_once(self.pop)

    def pop(self, dt):
        if Server().get_tyc_state()['tyc'] == 'on':
            self.popup = CustomPopup(TyC)
            self.popup.open()

    def check(self):
        in_user = self.ids.user.text
        in_pwd = self.ids.pwd.text
        if Server().login(in_user, in_pwd):
            App.get_running_app().root.current = 'main'

class MainMenu(Screen):
    pass

class Aspersores(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.condition = Server().asp_state()

    def on_enter(self):
        Clock.schedule_once(self.state_check)

    def state_check(self, dn):
        match self.condition:
            case 0: 
                self.ids.state_lbl.text = 'Estado: [color=FF5555]APAGADO[/color]'
                self.ids.state_btn.text = 'Encender'
                self.ids.state_btn.disabled = False
            case 1: 
                self.ids.state_lbl.text = 'Estado: [color=84F19C]ENCENDIDO[/color]'
                self.ids.state_btn.text = 'Apagar'
                self.ids.state_btn.disabled = False
            case 2: 
                self.ids.state_lbl.text = 'Estado: [color=FFF355]ERROR[/color]'
                self.ids.state_btn.text = '...'
                self.ids.state_btn.disabled = True

    def change_state(self):
        match self.condition:
            case 0:
                Server().change_asp_state('on')
            case 1:
                Server().change_asp_state('off')
        self.condition = Server().asp_state()
        self.state_check('x')

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
        config_data = Server().get_horarios()
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
        Server().edit_horarios(data)

class Datos(Screen):
    def on_enter(self):
        Clock.schedule_once(self.setup)

    def setup(self, dt):
        info = eval(Server().day())
        self.ids.temp.text = f"{info['temp']} °C"
        self.ids.hum.text = f"{info['hum']} %"
        self.ids.last.text = f"{info['last']}"

    def pop_pregunta(self):
        popup = PreguntaPopup("Aquí se mostrarán los datos de temperatura, la humedad del suelo y el último riego de nuestro sistema. Esto le permitirá evaluar la información para tomar decisiones sobre el manejo del sistema.") 
        popup.open()


class Historial(Screen):
   
    def pop_pregunta(self):
        popup = PreguntaPopup("Aquí veremos los riesgos que se han ido haciendo a lo largo del tiempo. Se mostrarán, la fecha, el horario que se estableció esta sesión, la humedad final del momento y cuánta agua se utilizó en esta sesión.") 
        popup.open()
    pass



class Grafico(Screen):
   
    def build(self):
       
        layout = FloatLayout()
        b_volver = Button(text="VOLVER AL MENÚ", background_color=[190.86, 0.2, 0.2, 1],size_hint=(1, None),size=(100, 50), pos_hint={'center_x': 0.5 , 'center_y': 0.5})
        layout.add_widget(b_volver)

        b_preg= Button (text= "[b]?[/b]", markup= True , size_hint=(None, None), font_size= 50, size=(50, 50), background_color=[0.75, 0.75, 0.75, 1],pos_hint={'center_x': 0.96 , 'center_y': 10.5})
        layout.add_widget(b_preg)

        l_esc = Label(text='INSM', font_size='20sp',pos_hint={'center_x': 0.1 , 'center_y': 10.5})
        layout.add_widget(l_esc)


        self.fig, self.ax = plt.subplots(dpi=80, figsize=(7,5), facecolor='#404040')
        plt.xlim(-11, 11)
        plt.ylim(-8, 8)
        plt.grid (alpha=0.2)
        plt.title("Gráfico del Día",color='white',size=28,)
        plt.subplots_adjust(top=0.8) 


        self.ax.set_facecolor('#6E6D7000')

        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['left'].set_color('black')        

        
        self.ax.set_xlabel("Tiempo", color='white',  size=15)
        self.ax.set_ylabel("Humedad", color='white',  size = 15)
        self.ax.tick_params(color = 'black', labelcolor = 'white', direction='out', length=10, width=2) 
  

        box = BoxLayout( orientation = 'vertical', spacing=1)
        # self.canvas = FigureCanvasKivyAgg(self.fig, size_hint=(1, 10))
        # box.add_widget(self.canvas)
        box.add_widget(layout)
        
        return box
    
    
    def on_enter(self):
        Clock.schedule_once(self.change_screen)

    def change_screen(self, dt):
        try:
            files = listdir(dir)
            if "main.kv" in files:
                self.manager.current = "grafico"
            else:
                pass
        except Exception as e:
            print(e)

class FdCyTApp(App):
    def build(self):
        return Builder.load_file("./main.kv")

if __name__ == '__main__':
    FdCyTApp().run()