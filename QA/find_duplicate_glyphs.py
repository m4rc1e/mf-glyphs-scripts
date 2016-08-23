'''
Find duplicate glyphs in selected font
'''
from collections import Counter


def find(font_glyphs):
    '''Check if there are duplicate glyphs'''
    print '***Find Duplicate glyphs in selected font***'
    glyphs_count = Counter(font_glyphs)
    if len(set(glyphs_count.values())) >= 2:
        for glyph in glyphs_count:
            if glyphs_count[glyph] >= 2:
                print 'ERROR: %s duplicated' % glyph
    else:
        print 'PASS: No duplicate glyphs\n'


if __name__ == '__main__':
    font = Glyphs.font
    find([g.name for g in font.glyphs])
