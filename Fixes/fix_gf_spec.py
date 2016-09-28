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
    font.customParameters['fsType'] = 0
    font.customParameters['Use Typo Metrics'] = True

    # Delete panose constant for family. Panose should be unique for each instance
    if 'panose' in font.customParameters:
        del font.customParameters['panose']

    # Add http:// to manufacturerURL and designerURL if they don't exist
    if not font.manufacturerURL.startswith('http://'):
        font.manufacturerURL = 'http://' + font.manufacturerURL

    if not font.designerURL.startswith('http://'):
        font.designerURL = 'http://' + font.designerURL

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
        if not instance.customParameters['compatibleFullName']:
            instance.customParameters['compatibleFullName'] = '%s %s' % (font.familyName, instance.name)

        # familyName Regular Italic -> familyName Italic
        if instance.customParameters['compatibleFullName'] == '%s Regular Italic' % (font.familyName):
            instance.customParameters['compatibleFullName'] = '%s Italic' % (font.familyName)

        if 'Italic' in instance.customParameters['compatibleFullName']:
            instance.isItalic = True
            instance.linkStyle = instance.weight

        # Seperate Condensed weights into their own family
        if instance.width == 'Condensed':
            condensed_family_name = '%s %s' % (font.familyName, instance.width)
            instance.customParameters['familyName'] = condensed_family_name
            instance.customParameters['compatibleFullName'] = '%s %s' % (condensed_family_name, instance.name)

        if instance.weight == 'Bold':
            instance.isBold = True
        else:
            instance.isBold = False


if __name__ == '__main__':
    main()
