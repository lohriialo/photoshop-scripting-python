# Compare foreground and background colours.

from ps_connect import photoshop

ps = photoshop()
fg = ps.foreground_color()
bg = ps.background_color()
# Equality depends on appscript colour records
try:
    equal = fg == bg
except Exception:
    equal = False
print("They're Equal" if equal else "NOT Equal")
