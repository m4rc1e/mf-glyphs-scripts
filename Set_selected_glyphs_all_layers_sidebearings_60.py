#MenuTitle: Set all selected glyphs sidebearings to +60, all layers
# -*- coding: utf-8 -*-
'''
Set sidebearings of selected glyphs to +60, every layer!
'''

R_BEARING = 60
L_BEARING = 60


def main():
    # Set metrics of each layer to generic amount:
    glyphs = Glyphs.font.selection
    masters = Glyphs.font.masters
    for glyph in glyphs:
        for i in range(len(masters)):
            glyph.layers[i].RSB = R_BEARING
            glyph.layers[i].LSB = L_BEARING
    print('metrics updated')


if __name__ == '__main__':
    main()
