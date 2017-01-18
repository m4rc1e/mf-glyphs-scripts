#MenuTitle: Auto Vert Metrics
"""Warning: Do not use this for updating fonts

Apply auto vertical metrics based on legacy 125% rule and Khaled.

Glyphsapp by default, exports fonts vertical metrics as 120% of the upm. This
script will export the vertical metrics at 125% and feature no clipping on
MS applications.

The overall aim is to avoid clipping and make the appearance consistent across
all platforms.
"""
from fix_vmetrics_win_clipping import shortest_tallest_glyphs


def main():
    font = Glyphs.font
    Glyphs.showMacroWindow()
    new_win_desc, new_win_asc = shortest_tallest_glyphs(font)
    upm_125 = font.upm * 1.25

    for master in font.masters:
        vert = master.customParameters

        print 'Updating %s vertical metrics' % master.name
        asc = int(upm_125 * 0.75)
        desc = -int(upm_125 * 0.25)

        vert['typoAscender'] = asc
        vert['typoDescender'] = desc
        vert['typoLineGap'] = 0

        vert['winAscent'] = int(new_win_asc)
        vert['winDescent'] = int(abs(new_win_desc))

        vert['hheaAscender'] = asc
        vert['hheaDescender'] = desc
        vert['hheaLineGap'] = 0

    print 'Enabling Use Typo Metrics'
    font.customParameters['Use Typo Metrics'] = True

    print 'Done. Updated all masters vertical metrics'


if __name__ == '__main__':
    main()
