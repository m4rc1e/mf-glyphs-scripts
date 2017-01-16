#MenuTitle: Change metrics to stop win clipping
"""Update vertical metrics so glyphs do not appear
clipped in MS applications.

- Set the Typo values to the old Win Metrics
- Set the Win Metrics to the tallest / shortest glyph
- Retain the same hhea values but divide the line gap
  between the hhea Ascender and hhea Descender"""
import math

def shortest_tallest_glyphs(font, *args):
    '''find the tallest and shortest glyphs in all masters.'''
    lowest = 0.0
    highest = 0.0
    highest_name = ''
    lowest_name = ''

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

    return math.ceil(lowest), math.ceil(highest)


def main():
    font = Glyphs.font
    Glyphs.showMacroWindow()
    new_win_desc, new_win_asc = shortest_tallest_glyphs(font)

    if font.customParameters['Use Typo Metrics']:
        print 'ERROR: Use typo metrics flag already enabled'
        print 'Cannot do metrics acrobatics'
        return

    for master in font.masters:
        vert = master.customParameters

        print 'Updating %s Typo Metrics' % master.name
        vert['typoAscender'] = vert['winAscent']
        vert['typoDescender'] = -vert['winDescent']
        vert['typoLineGap'] = 0

        print 'Updating %s Win Metrics' % master.name
        vert['winAscent'] = int(new_win_asc)
        vert['winDescent'] = int(abs(new_win_desc))

        print 'Updating %s hhea metrics' % master.name
        hhea_add = vert['hheaLineGap'] / 2
        vert['hheaAscender'] = vert['hheaAscender'] + hhea_add
        vert['hheaDescender'] = vert['hheaDescender'] + hhea_add
        vert['hheaLineGap'] = 0

    print 'Enabling Use Typo Metrics'
    font.customParameters['Use Typo Metrics'] = True
    print 'Done: Metrics updated'


if __name__ == '__main__':
    main()
