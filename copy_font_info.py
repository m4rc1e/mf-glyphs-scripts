#MenuTitle: Copy font info from other font
'''
With two fonts open, copy font info from font in background
to selected font.
'''

CUSTOM_PARAMS = {
    "glyphOrdee",
    "Family Alignment Zones",
    "panose",
    "fsType",
    "unicodeRanges",
    "codePageRanges",
    "vendorID",
    "blueScale",
    "blueShift",
    "isFixedPitch",
    "trademark",
    "description",
    "sampleText",
    "license",
    "licenseURL",
    "versionString",
    "uniqueID",
    "ROS",
    "Make morx table",
    "EditView Line Height",
    "Compatible Name Table",
    "Name Table Entry",
    "GASP Table",
    "localizedFamilyName",
    "localizedDesigner",
    "TrueType Curve Error",
    "Use Typo Metrics",
    "Has WWS Names",
    "Use Extension Kerning",
    "Don't use Production Names",
    "makeOTF Argument",
    "note",
    "Disable Subroutines",
    "Disable Last Change",
    "Use Line Breaks",
}

def main():
    to_font = Glyphs.fonts[0]
    from_font = Glyphs.fonts[1]

    to_font.copyright = from_font.copyright
    to_font.designer = from_font.designer
    to_font.designerURL = from_font.designerURL
    to_font.manufacturer = from_font.manufacturer
    to_font.manufacturerURL = from_font.manufacturerURL
    to_font.versionMajor = from_font.versionMajor
    to_font.versionMinor = from_font.versionMinor
    to_font.date = from_font.date
    to_font.familyName = from_font.familyName

    for key in CUSTOM_PARAMS:
        if key in from_font.customParameters:
            to_font.customParameters[key] = from_font.customParameters[key]

    print 'family info copied'

if __name__ == '__main__':
    if len(Glyphs.fonts) != 2:
        print 'Please have two fonts open only!'
    else:
        main()
