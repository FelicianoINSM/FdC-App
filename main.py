from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from os import listdir
from kivy.clock import Clock

import os

dir= os.getcwd()

objetos_info = [
    {"title": "Objeto 1", "info": "Información del objeto 1."},
    {"title": "Objeto 2", "info": "Información del objeto 2."},
    {"title": "Objeto 3", "info": "Información del objeto 3."}
]

class DropDownItem(GridLayout):
    container_title = ObjectProperty() 
    container = ObjectProperty()
    title = StringProperty("")
    hidden = BooleanProperty(False)
    title_height = NumericProperty()

    def __init__(self, title="", title_height="50dp", info="", **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_y = None
        self.title = title
        self.title_height = title_height

        container_title = ToggleButton(height=title_height, size_hint_y=None, text=title)
        container_title.bind(state=self.on_drop_down)

        container = GridLayout(size_hint_y=None, cols=1)
        self.add_widget(container_title)
        self.add_widget(container)

        self.bind(minimum_height=self.setter("height"))
        self.bind(title=container_title.setter("text"))
        self.bind(title_height=container_title.setter("height"))
        container.bind(minimum_height=container.setter("height"))
        container.padding = ("10dp", "5dp", "10dp", "10dp")

        self.container = container
        self.container_title = container_title
        self.hidden = True

        # Información adicional del objeto
        info_label = Label(text=info, halign='left', markup=True)
        self.container.add_widget(info_label)

    def on_drop_down(self, obj, value):
        if value == "down":
            self.hidden = False
        else:
            self.hidden = True

    def on_hidden(self, obj, hidden):
        if hidden:
            self.container.opacity = 0
            self.container.size_hint = 0, 0
            self.container.size = 0, 0
            self.container.disabled = True
        else:
            self.container.opacity = 1
            self.container.size_hint = 1, None
            self.container.disabled = False
            self.container.height = self.container.minimum_height


class DropDownList(BoxLayout):
    container_layout = ObjectProperty(None)
    scroll_view = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10", "10"

        self.scroll_view = ScrollView()
        self.bind(size=self.scroll_view.setter("size"))
        self.add_widget(self.scroll_view)

        self.container_layout = GridLayout(cols=1, size_hint_y=None)
        self.container_layout.bind(minimum_height=self.container_layout.setter('height'))
        self.scroll_view.add_widget(self.container_layout)

        # Crear objetos DropDownItem con la información de la lista
        for obj_info in objetos_info:
            dropdown_item = DropDownItem(title=obj_info["title"], info=obj_info["info"])
            self.container_layout.add_widget(dropdown_item)


class Datos(Screen):
    pass

class Historial(Screen):
    pass

class Pregunta1(Screen):
    pass

class Pregunta2(Screen):
    pass

class Pregunta3(Screen):
    pass

class Pregunta4(Screen):
    pass

class Pregunta5(Screen):
    pass

class Pregunta6(Screen):
    pass

class Pregunta7(Screen):
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