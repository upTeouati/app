[app]
title = Screen Viewer
package.name = screenviewer
package.domain = org.screenviewer
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.0,kivymd==1.1.1,websockets==10.0,pillow==9.0.0,android
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.0
fullscreen = 0
android.permissions = INTERNET
android.arch = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.gradle_dependencies = org.tensorflow:tensorflow-lite:+
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
