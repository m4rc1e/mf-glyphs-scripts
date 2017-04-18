import math

VERT_KEYS = [
    'typoAscender',
    'typoDescender',
    'typoLineGap',
    'winAscent',
    'winDescent',
    'hheaAscender',
    'hheaDescender',
    'hheaLineGap',
]


def shortest_tallest_glyphs(font, *args):
    '''find the tallest and shortest glyphs in all masters from a list.
    If no list is given, search all glyphs.'''
    lowest = 0.0
    highest = 0.0

    masters_count = len(font.masters)

    if args:
        glyphs = [font.glyphs[i] for i in args]
    else:
        glyphs = font.glyphs

    for glyph in glyphs:
        for i in range(masters_count):
            glyph_ymin = glyph.layers[i].bounds[0][-1]
            glyph_ymax = glyph.layers[i].bounds[-1][-1] + glyph.layers[i].bounds[0][-1]
            if glyph_ymin < lowest:
                lowest = glyph_ymin
            if glyph_ymax > highest:
                highest = glyph_ymax

    return int(math.ceil(lowest)), int(math.ceil(highest))
