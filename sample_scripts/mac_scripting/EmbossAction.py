# Emboss filter via do_javascript Action Manager (macOS).

from ps_connect import photoshop, sample_file

ps = photoshop()
ps.open(sample_file("Layer Comps.psd"))
jsx = """
var d = new ActionDescriptor();
d.putInteger(charIDToTypeID("Angl"), 120);
d.putInteger(charIDToTypeID("Hght"), 10);
d.putInteger(charIDToTypeID("Amnt"), 100);
executeAction(charIDToTypeID("Embs"), d, DialogModes.NO);
"""
ps.do_javascript(jsx)
print("Emboss applied")
