from appscript import app

ps = app(id="com.adobe.Photoshop", terms="sdef")

# i.e. 'marqueeRectTool', 'moveTool'
print(ps.current_tool())
