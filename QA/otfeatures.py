import re


VIET_GLYPHS = [
    'idotaccent',
    'idotaccent',
    'idotaccent',
    'idotaccent',
    'periodcentered.loclCAT',
    'periodcentered.loclCAT',
    'idotaccent',
    'Scommaaccent',
    'scommaaccent',
    'Tcommaaccent',
    'tcommaaccent',
    'Scommaaccent',
    'scommaaccent',
    'Tcommaaccent',
    'tcommaaccent',
    'Aacute.loclVIT',
    'Agrave.loclVIT',
    'Eacute.loclVIT',
    'Egrave.loclVIT',
    'Iacute.loclVIT',
    'Igrave.loclVIT',
    'Oacute.loclVIT',
    'Ograve.loclVIT',
    'Uacute.loclVIT',
    'Ugrave.loclVIT',
    'Yacute.loclVIT',
    'Ygrave.loclVIT',
    'aacute.loclVIT',
    'agrave.loclVIT',
    'eacute.loclVIT',
    'egrave.loclVIT',
    'iacute.loclVIT',
    'igrave.loclVIT',
    'oacute.loclVIT',
    'ograve.loclVIT',
    'uacute.loclVIT',
    'ugrave.loclVIT',
    'yacute.loclVIT',
    'ygrave.loclVIT',
    'gravecomb.loclVIT',
    'acutecomb.loclVIT',
    'circumflexcomb.loclVIT',
    'brevecomb.loclVIT',
    'tildecomb.loclVIT'
]


def dynamic_fraction(font):
    '''If font has fivesuperior, there should be a dynamic fraction feature'''
    print '**Checking frac feature**'
    if 'fivesuperior' in font.glyphs:
        if font.features['frac']:
            if "'" in str(font.features['frac'].code):
                print 'PASS: Font has dynamic frac feature\n'
            else:
                print 'POSSIBLE ERROR: frac feature may not be dynamic\n'
        else:
            print 'ERROR: no frac OT feature\n'
    else:
        print 'PASS: font does not have 4-9 numerators glyphs, no'\
            'dynamic frac needed\n'


def vietnamese_locl(feature):
    '''Check if localised vietnamese glyphs are implemented'''
    print '**Checking for locl Vietnamese**'

    viet_subs = re.findall(r'(?<=by ).*(?<!;)', feature)
    missing_vietnamese_glyphs = set(VIET_GLYPHS) - set(viet_subs)

    if not missing_vietnamese_glyphs:
        print 'PASS: Localised Vietnamese glyphs exist'
    else:
        print 'ERROR: Locailised Vietnamese missing following glyphs:'
        for glyph in missing_vietnamese_glyphs:
            print '    %s' % glyph
        print '\n'
