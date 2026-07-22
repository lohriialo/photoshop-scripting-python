# Read foreground colour components.

from ps_connect import photoshop

ps = photoshop()
fg = ps.foreground_color()
try:
    # Often a record with RGB fields
    print("Foreground:", fg)
except Exception as exc:
    print(exc)
