# This script compares the app.foregroundColor
# to the app.backgroundColor.

from appscript import app

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

if ps.foreground_color() == ps.background_color():
    print("They're Equal")
else:
    print("NOT Equal")
