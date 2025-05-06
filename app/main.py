import sys
from pathlib import Path
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from app.views import LogScreen, CalendarView, HomeScreen, AnalyticsScreen

import logging
import os
import platform
import traceback

if platform.system() == 'Android':
    from kivy.android import get_external_storage_path
    from jnius import autoclass

    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    package_name = PythonActivity.mActivity.getPackageName()
    log_dir = os.path.join(get_external_storage_path(), 'Android', 'data', package_name, 'files')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'app.log')
    logging.basicConfig(filename=log_path, level=logging.DEBUG)

    logging.debug('App started')
else:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('App started (non-Android platform)')


class GutHealthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(LogScreen(name='log'))
        sm.add_widget(CalendarView(name='calendar'))
        sm.add_widget(AnalyticsScreen(name='analytics'))
        return sm

def main():
    GutHealthApp().run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("Unhandled exception occurred:")
        logging.error(traceback.format_exc())
        raise