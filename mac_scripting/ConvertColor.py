# Convert the foreground color to RGB.

from appscript import app, k

ps = app(id="com.adobe.Photoshop", terms="sdef")

fgColor = ps.foreground_color

# Unlike JavaScript and COM, we have to use a function to convert colors
fgRGBColor = fgColor.convert_color(to=k.RGB)
print(f"Red: {fgRGBColor[k.red]} Green: {fgRGBColor[k.green]} Blue: {fgRGBColor[k.blue]}")
