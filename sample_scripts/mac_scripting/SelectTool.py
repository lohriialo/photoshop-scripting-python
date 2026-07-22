# Read the current tool ID string.

from ps_connect import photoshop

ps = photoshop()
print(ps.current_tool())
