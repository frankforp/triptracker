from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class TriptrackerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        # add widgets here

        return sm


sm = ScreenManager()

if __name__ == '__main__':
    TriptrackerApp().run()
