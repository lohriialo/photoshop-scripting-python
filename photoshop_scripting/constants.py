"""
Common Photoshop COM enum values used across samples and tools.

Values match the Photoshop object model (Ps* enums). Prefer these named
constants over magic integers in scripts.
"""

from __future__ import annotations

from enum import IntEnum


class DialogModes(IntEnum):
    """PsDialogModes — app.displayDialogs"""

    ALL = 1
    ERROR = 2
    NO = 3


class Units(IntEnum):
    """PsUnits — Preferences.RulerUnits"""

    PIXELS = 1
    INCHES = 2
    CM = 3
    MM = 4
    POINTS = 5
    PICAS = 6
    PERCENT = 7


class TypeUnits(IntEnum):
    """PsTypeUnits — Preferences.TypeUnits"""

    PIXELS = 1
    MM = 4
    POINTS = 5


class LayerKind(IntEnum):
    """PsLayerKind"""

    NORMAL = 1
    TEXT = 2
    SOLID_FILL = 3
    GRADIENT_FILL = 4
    PATTERN_FILL = 5
    LEVELS = 6
    CURVES = 7
    COLOR_BALANCE = 8
    BRIGHTNESS_CONTRAST = 9
    HUE_SATURATION = 10
    SELECTIVE_COLOR = 11
    CHANNEL_MIXER = 12
    GRADIENT_MAP = 13
    INVERSION = 14
    THRESHOLD = 15
    POSTERIZE = 16
    SMART_OBJECT = 17
    PHOTO_FILTER = 18
    EXPOSURE = 19
    LAYER_3D = 20
    VIDEO = 21
    BLACK_AND_WHITE = 22
    VIBRANCE = 23
    COLOR_LOOKUP = 24


class DocumentMode(IntEnum):
    """PsDocumentMode — Documents.Add color mode"""

    GRAYSCALE = 1
    RGB = 2
    CMYK = 3
    LAB = 4
    BITMAP = 5
    INDEXED_COLOR = 6
    MULTI_CHANNEL = 7
    DUOTONE = 8


class DocumentFill(IntEnum):
    """PsDocumentFill"""

    WHITE = 1
    BACKGROUND = 2
    TRANSPARENT = 3


class SelectionType(IntEnum):
    """PsSelectionType"""

    REPLACE = 1
    EXTEND = 2
    DIMINISH = 3
    INTERSECT = 4


class ResampleMethod(IntEnum):
    """PsResampleMethod"""

    NO = 1
    NEAREST_NEIGHBOR = 2
    BILINEAR = 3
    BICUBIC = 4
    BICUBIC_SHARPER = 5
    BICUBIC_SMOOTHER = 6
    BICUBIC_AUTOMATIC = 7
    AUTOMATIC = 8
    PRESERVE_DETAILS = 9


class StrokeLocation(IntEnum):
    """PsStrokeLocation"""

    INSIDE = 1
    CENTER = 2
    OUTSIDE = 3


class BlendMode(IntEnum):
    """Common PsBlendMode / color blend values used in samples"""

    NORMAL = 2
    DISSOLVE = 3
    DARKEN = 4
    MULTIPLY = 5
    COLOR_BURN = 6
    LINEAR_BURN = 7
    LIGHTEN = 8
    SCREEN = 9
    COLOR_DODGE = 10
    LINEAR_DODGE = 11
    OVERLAY = 12
    SOFT_LIGHT = 13
    HARD_LIGHT = 14
    VIVID_LIGHT = 15
    LINEAR_LIGHT = 16
    PIN_LIGHT = 17
    DIFFERENCE = 18
    EXCLUSION = 19
    HUE = 20
    SATURATION = 21
    COLOR = 22
    LUMINOSITY = 23


class SaveOptions(IntEnum):
    """PsSaveOptions — Document.Close"""

    PROMPT = 1
    SAVE_CHANGES = 2
    DO_NOT_SAVE = 3


class AnchorPosition(IntEnum):
    """PsAnchorPosition — ResizeCanvas / transforms"""

    TOP_LEFT = 1
    TOP_CENTER = 2
    TOP_RIGHT = 3
    MIDDLE_LEFT = 4
    MIDDLE_CENTER = 5
    MIDDLE_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_CENTER = 8
    BOTTOM_RIGHT = 9


class ExtensionType(IntEnum):
    """PsExtensionType — SaveAs lowercase/uppercase extension"""

    LOWERCASE = 2
    UPPERCASE = 3


class ExportType(IntEnum):
    """PsExportType"""

    ILLUSTRATOR_PATHS = 1
    SAVE_FOR_WEB = 2


# Backward-compatible aliases matching older sample naming
psDisplayNoDialogs = DialogModes.NO
psPixels = Units.PIXELS
psInches = Units.INCHES
psTextLayer = LayerKind.TEXT
psNewRGB = DocumentMode.RGB
psWhite = DocumentFill.WHITE
psReplaceSelection = SelectionType.REPLACE
psOutsideStroke = StrokeLocation.OUTSIDE
psVividLightBlend = BlendMode.VIVID_LIGHT
psAutomatic = ResampleMethod.AUTOMATIC
psDoNotSaveChanges = SaveOptions.DO_NOT_SAVE
