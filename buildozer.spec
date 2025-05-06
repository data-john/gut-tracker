[app]
# (str) Title of your application
# This is the name of the app as it will appear on the device
# Example: title = My Application
title = Gut Health Tracker

# (str) Source code where the main.py is located
# Example: source.dir = .
source.dir = app

# (str) Package name
# This is the unique identifier for your app
# Example: package.name = com.example.myapp
package.name = com.john.guthealth

# (str) Version of your application
# Example: version = 1.0
version = 0.2.1

android.ndk_path = /home/john/.buildozer/android/platform/android-ndk-r25b
android.api = 31
android.minapi = 21

log_level = 2

permissions = android.permission.WRITE_EXTERNAL_STORAGE

requirements = kivy,matplotlib,pysqlcipher3,buildozer,setuptools,Cython,pyjnius,pytest,kivy_garden,kivy_garden.matplotlib,kivy_garden.graph