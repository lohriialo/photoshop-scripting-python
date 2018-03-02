import os
import sys
import shutil
from ctypes import windll

def is_cache():
    try:
        import comtypes.gen
    except ImportError:
        return
    return comtypes.gen.__path__[0]


def _remove(directory):
    shutil.rmtree(directory)
    print("Removed directory %s" % directory)


install_text = """\
When installing a new comtypes version, it is recommended to remove
the comtypes\gen directory and the automatically generated modules
it contains.  This directory and the modules will be regenerated
on demand.

Should the installer delete all the files in this directory?"""

deinstall_text = """\
The comtypes\gen directory contains modules that comtypes
automatically generates.

Should this directory be removed?"""

if len(sys.argv) > 1 and "-install" in sys.argv[1:]:
    title = "Install comtypes"
    text = install_text
else:
    title = "Remove comtypes"
    text = deinstall_text

if len(sys.argv) > 1 and "-silent" in sys.argv[1:]:
    silent = True
else:
    silent = False



IDYES = 6
IDNO = 7
MB_YESNO = 4
MB_ICONWARNING = 48
directory = is_cache()
if directory:
    if silent:
        _remove(directory)
    else:
        res = windll.user32.MessageBoxA(0, text, title,
                MB_YESNO|MB_ICONWARNING)
        if res == IDYES:
            _remove(directory)
        else:
            print("Directory %s NOT removed" % directory)
