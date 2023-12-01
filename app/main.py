from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from os import listdir
from kivy.clock import Clock
import requests
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.popup import Popup

import os

dir= os.getcwd()


class Server:
    def day(self):
        url = 'http://127.0.0.1:8080/day'
        response = requests.get(url)
        return response.text
    
    def historial(self):
        url = 'http://127.0.0.1:8080/hist'
        response = requests.get(url)
        return response.text

class CustomPopup(Popup):
    def __init__(self, text, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        self.ids.pop_label.text = text


class DropDownItem(GridLayout):
    def __init__(self, obj_info, **kwargs):
        super(DropDownItem, self).__init__(cols=5, height=40, **kwargs)

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


class Datos(Screen):
    def on_enter(self):
        Clock.schedule_once(self.setup)

    def setup(self, dt):
        info = eval(Server().day())
        self.ids.temp.text = f"{info['temp']} °C"
        self.ids.hum.text = f"{info['hum']} %"
        self.ids.last.text = f"{info['last']} hs"

    def pop_pregunta(self):
        popup = CustomPopup("Aquí se mostrarán los datos de temperatura, la humedad del suelo y el último riego de nuestro sistema. Esto le permitirá evaluar la información para tomar decisiones sobre el manejo del sistema.") 
        popup.open()


class Historial(Screen):
   
    def pop_pregunta(self):
        popup = CustomPopup("Aquí veremos los riesgos que se han ido haciendo a lo largo del tiempo. Se mostrarán, la fecha, el horario que se estableció esta sesión, la humedad final del momento y cuánta agua se utilizó en esta sesión.") 
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
        self.canvas = FigureCanvasKivyAgg(self.fig, size_hint=(1, 10))
        box.add_widget(self.canvas)
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