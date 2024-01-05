from kivymd.app import MDApp
from kivy.lang import Builder #leer esestilo 
from kivy.uix.screenmanager import ScreenManager #para creacion de pantallas 
from kivy.uix.button import Label
from kivy.core.window import Window #inportar para configurar para el teclado del celular
import requests #para obtener y enviar datos a la base de datos 


Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'} #para confiugrar el teclado virtual del 'd' diracion, 't' tipo cel 
Window.softinput_mode= "below_target"#la forma y comportamiento del teclado

class Ui(ScreenManager): #hereda de screen manager donde sediseñan los widgets
    pass

class MainApp(MDApp):#creando el tema la app
    def build(self):
        self.theme_cls.theme_style ="Dark"
        self.theme_cls.primary_palette ="DeepOrange"
        Builder.load_file('style.kv')
        #la base de datos url y clave
        self.url = 'https://donbosco-9703d-default-rtdb.firebaseio.com/.json'
        self.key = 'jl1cuDRLbo2aC1GjeNZvGfOJ7zdD8uTsYmJHtXen'
        return Ui()
    
    def login_data(self):
        userx = self.root.ids.user.text
        passwordx = self.root.ids.password.text
        state = False
        data = requests.get(self.url + '?auth=' + self.key)

        for key, value in data.json().items():
            user_reg = value['User']
            password_reg = value ['Password']

            if userx == user_reg:
                if passwordx == password_reg:
                    state = True
                    self.root.ids.signal_login.text = ''#self.root.ids sirbe para llamar a un id del archivo kv
                    self.root.ids.user.text = ''
                    self.root.ids.password.text = ''
                else:
                    self.root.ids.signal_login.text = 'Contraseña incorrecta'
                    self.root.ids.user.text = ''
                    self.root.ids.password.text = ''
            else:
                self.root.ids.signal_login.text = 'Usuario incorrecta'
                self.root.ids.user.text = ''
                self.root.ids.password.text = ''
        return state
    
    def register_data(self):
        state = 'datos incorrectos'

        userx= self.root.ids.new_user.text
        password_one = self.root.ids.new_password.text
        password_two = self.root.ids.new_password_two.text

        data = requests.get(self.url + '?auth=' + self.key)

        if password_one != password_two:
            state = 'No coinciden las contraseñas'
        elif len(userx) <=4:
            state = 'Nombre muy corto'
        elif password_one == password_two and len(password_two)<=4:
            state = 'Contraseña muy corta'
        else:
            for key, value in data.json().items():
                user = value['User']
                if user == userx:
                    state = 'Este usuario ya existe'
                    break
                else:
                    state = 'Registrado correctamente'
                    data = {userx:{
                    'User': userx,
                    'Password':password_one
                    }}
                    requests.patch(url = self.url, json = data)
                    self.root.ids.signal_register.text = 'Registrado correctamente'

        self.root.ids.signal_register.text = state
        self.root.ids.new_user.text =''
        self.root.ids.new_password.text = ''
        self.root.ids.new_password_two.text = ''
        return state
    
    def clear_signal(self):
        self.root.ids.signal_register.text = ''
        self.root.ids.signal_login.text = ''

if __name__=="__main__":
    MainApp().run()