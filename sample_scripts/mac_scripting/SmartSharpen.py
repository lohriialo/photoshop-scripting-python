# Smart Sharpen via do_javascript (Action Manager parity on macOS).

from ps_connect import photoshop, sample_file

ps = photoshop()
ps.open(sample_file("Layer Comps.psd"))

# ExtendScript Action Manager — same IDs as Windows SmartSharpen.py
jsx = """
var id = stringIDToTypeID("smartSharpen");
var d = new ActionDescriptor();
d.putEnumerated(stringIDToTypeID("presetKind"), stringIDToTypeID("presetKindType"), stringIDToTypeID("presetKindCustom"));
d.putUnitDouble(charIDToTypeID("Amnt"), charIDToTypeID("#Prc"), 300);
d.putUnitDouble(charIDToTypeID("Rds "), charIDToTypeID("#Pxl"), 2.0);
d.putUnitDouble(stringIDToTypeID("noiseReduction"), charIDToTypeID("#Prc"), 20);
d.putEnumerated(charIDToTypeID("blur"), stringIDToTypeID("blurType"), charIDToTypeID("GsnB"));
executeAction(id, d, DialogModes.NO);
"""
ps.do_javascript(jsx)
print("Smart Sharpen applied")
