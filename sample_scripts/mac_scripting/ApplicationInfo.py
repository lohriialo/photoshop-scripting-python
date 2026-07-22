# Application object properties via appscript.

from ps_connect import photoshop

ps = photoshop()
print("Name:", ps.name())
print("Version:", ps.version())
try:
    print("Front document count:", len(ps.documents()))
except Exception as exc:
    print("documents:", exc)
