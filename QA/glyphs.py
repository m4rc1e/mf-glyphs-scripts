from collections import Counter
import unicodedata as uni

IGNORE_GLYPHS_OUTLINE = [
    'uni0000',
]


def find_duplicates(font_glyphs):
    '''Check if there are duplicate glyphs'''
    print '***Find Duplicate glyphs in selected font***'
    glyphs_count = Counter(font_glyphs)
    if len(set(glyphs_count.values())) >= 2:
        for glyph in glyphs_count:
            if glyphs_count[glyph] >= 2:
                print 'ERROR: %s duplicated\n' % glyph
    else:
        print 'PASS: No duplicate glyphs\n'


def outlines_missing(font):
    '''Check if glyphs are missing outlines or composites.
    Only works on glyphs which have unicodes'''
    print '***Check Glyphs have outlines or components***'
    masters = font.masters

    for i, master in enumerate(masters):
        bad_glyphs = []
        for glyph in font.glyphs:

            if str(glyph.category) != 'Separator' and glyph.name not in IGNORE_GLYPHS_OUTLINE:
                if len(glyph.layers[i].paths) == 0:
                    if len(glyph.layers[i].components) == 0:
                        bad_glyphs.append(glyph.name)

        if bad_glyphs:
            for glyph in bad_glyphs:
                print "ERROR: %s master's %s should have outlines or components\n" % (master.name, glyph)            
        else:
            print "PASS: %s master's glyphs have components or outlines\n" % master.name


def uni00a0_width(font, masters, fix=False):
    '''Set nbspace to same width as space'''
    print '***Checking space and nbspace have same width***'
    for id, master in enumerate(masters):
        if font.glyphs['nbspace'].layers[id].width != font.glyphs['space'].layers[id].width:
            print 'ERROR: %s nbspace and space are not same width\n' % (master.name)
        else:
            print 'PASS: %s nbspace and space are same width\n' % (master.name)

        if fix:
            font.glyphs['nbspace'].layers[id].width = font.glyphs['space'].layers[id].width
            print 'Now equal widths! space=%s, 00A0=%s' %(
                font.glyphs['space'].layers[id].width,
                font.glyphs['nbspace'].layers[id].width
            )


if __name__ == '__main__':
    font = Glyphs.font
    find([g.name for g in font.glyphs])
