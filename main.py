from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import webbrowser
import time
from filesharer import FileShare
import requests

Builder.load_file('frontend.kv')


class CameraScreen(Screen):

    def start(self):
        self.ids.camera.play = True
        self.ids.button_camera.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        self.ids.camera.play = False
        self.ids.button_camera.text = 'Start Camera'
        self.ids.camera.texture = None

    def capture(self):
        current_time = time.strftime('%Y%m%d-%H%M%S')
        #Creamos self.filepath para que no sea una variable, sino un atributo
        #y así poder acceder a él en la función create_link()
        self.filepath = f'files/{current_time}.png'
        self.ids.camera.export_to_png(self.filepath)
        #cambia de pantalla
        self.manager.current = 'image_screen'
        #carga la imagen en la nueva pantalla
        self.manager.current_screen.ids.image.source = self.filepath


class ImageScreen(Screen):

    link_message = "Create a Link First"

    def create_link(self):
        #Accede al atributo filepath de CameraScreen.capture
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        filesharer = FileShare(filepath=file_path)
        self.url = filesharer.share()
        self.ids.link.text = self.url

    def copy_link(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message

class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
