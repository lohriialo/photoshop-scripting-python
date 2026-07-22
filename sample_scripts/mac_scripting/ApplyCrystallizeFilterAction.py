# Crystallize filter via Action Manager (macOS / JSX).

from ps_connect import photoshop, sample_file

ps = photoshop()
ps.open(sample_file("Layer Comps.psd"))
jsx = """
var d = new ActionDescriptor();
d.putInteger(charIDToTypeID("ClSz"), 25);
executeAction(charIDToTypeID("Crst"), d, DialogModes.NO);
"""
ps.do_javascript(jsx)
print("Crystallize applied (cell size 25)")
