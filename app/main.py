import sys
from pathlib import Path
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from app.views import LogScreen

class GutHealthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LogScreen(name='log'))
        return sm

def main():
    GutHealthApp().run()

if __name__ == "__main__":
    main()