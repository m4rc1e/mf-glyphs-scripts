#MenuTitle: Fix fonts for GF spec
'''
Fix/add requirements from ProjectChecklist.md
'''

from datetime import datetime


def main():
    # Add README file if it does not exist

    font = Glyphs.font
    font.customParameters['license'] = 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL'
    font.customParameters['licenseURL'] = 'http://scripts.sil.org/OFL'
    font.customParameters['fsType'] = []
    font.customParameters['Use Typo Metrics'] = True

    # Delete panose constant for family. Panose should be unique for each instance
    if 'panose' in font.customParameters:
        del font.customParameters['panose']

    # Add http:// to manufacturerURL and designerURL if they don't exist
    if font.manufacturerURL:
        if not font.manufacturerURL.startswith('http://'):
            font.manufacturerURL = 'http://' + font.manufacturerURL
    else:
        print 'WARNING: manufacturerURL is missing'

    if font.designerURL:
        if not font.designerURL.startswith('http://'):
            font.designerURL = 'http://' + font.designerURL
    else:
        print 'WARNING: designerURL is missing'

    # Remove glyph order
    if 'glyphOrder' in font.customParameters:
        del font.customParameters['glyphOrder']

    masters = font.masters
    instances = font.instances

    # If nbspace does not exist, create it
    if not font.glyphs['nbspace'] or font.glyphs['uni00A0']:
        nbspace = GSGlyph()
        nbspace.name = 'nbspace'
        nbspace.unicode = unicode('00A0')
        font.glyphs.append(nbspace)

    # If CR does not exist, create it
    if not font.glyphs['CR'] or font.glyphs['uni000D']:
        cr = GSGlyph()
        cr.name = 'CR'
        cr.unicode = unicode('000D')
        font.glyphs.append(cr)

    # If NULL does not exist, create it
    if not font.glyphs['NULL'] or font.glyphs['.null']:
        null = GSGlyph()
        null.name = 'NULL'
        null.unicode = unicode('0000')
        font.glyphs.append(null)

    # fix width glyphs
    for i, master in enumerate(masters):
        # Set nbspace width so it matches space
        font.glyphs['nbspace'].layers[i].width = font.glyphs['space'].layers[i].width
        # Set NULL width so it is 0
        font.glyphs['NULL'].layers[i].width = 0
        # Set CR so width matches space
        font.glyphs['CR'].layers[i].width = font.glyphs['space'].layers[i].width

    # fix instance names to pass gf spec
    for i, instance in enumerate(instances):
        if 'Italic' in instance.name:
            instance.isItalic = True
            instance.linkStyle = instance.weight

        # Seperate Condensed weights into their own family
        if instance.width == 'Condensed':
            condensed_family_name = '%s %s' % (font.familyName, instance.width)
            instance.customParameters['familyName'] = condensed_family_name

        if instance.weight == 'Bold':
            instance.isBold = True
        else:
            instance.isBold = False

        # Change ExtraLight weight class from 250 to 275
        if instance.weight == 'ExtraLight':
            instance.customParameters['weightClass'] = 275

        # If Heavy exists, create a new font family for it
        if 'Heavy' in instance.name:
            instance.customParameters['familyName'] = '%s Heavy' % (font.familyName)
            instance.name = instance.name.replace('Heavy', 'Regular')
            instance.weight = 'Regular'

        if instance.name == 'Regular Italic':
            instance.name = 'Italic'


if __name__ == '__main__':
    main()
