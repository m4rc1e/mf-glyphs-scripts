#MenuTitle: Generate Gpos Strings

'''Exports all single gpos combos e.g a+acutcomb

To do:
    Support for non-Latin scripts.

Release history:
    2015/08/29:
    V0.001: This is the first release'''

import GlyphsApp
import re

class AnchorData(object):
    '''Easier access for specific anchors. Heirachy for each
    dictionary as follows:

    {weight:
            glyph:
                    anchor.name = (x, y)}'''
    def __init__(self, font, truncate=False):
        self.font = font

        self.base_anchors = {}
        self.mark_anchors = {}
        self.lig_anchors = {}

        for glyph in self.font.glyphs:
            for layer in glyph.layers:

                if not layer.name in self.base_anchors:
                    self.base_anchors[layer.name] = {}
                    self.mark_anchors[layer.name] = {}
                    self.lig_anchors[layer.name] = {}

                if layer.anchors:
                    for anchor in layer.anchors:
                        anc_name = anchor.name
                        g_name = glyph.name
                        
                        a_x = anchor.position.x
                        a_y = anchor.position.y
                        
                        if truncate:
                            g_name = glyph.name.split('.')[0]
                            anc_name = anchor.name.split('.')[0]
                            
                        if anchor.name.startswith('_'):
                            if not glyph.name in self.mark_anchors[layer.name]:
                                self.mark_anchors[layer.name][g_name] = {}
                            self.mark_anchors[layer.name][g_name][anc_name] = (a_x, a_y)

                        elif '_' in anchor.name[1:]:
                            if not glyph.name in self.lig_anchors[layer.name]:
                                self.lig_anchors[layer.name][g_name] = {}
                            self.lig_anchors[layer.name][g_name][anc_name] = (a_x, a_y)

                        else:
                            if not glyph.name in self.base_anchors[layer.name]:
                                self.base_anchors[layer.name][g_name] = {}
                            self.base_anchors[layer.name][g_name][anc_name] = (a_x, a_y)

    @property
    def basemarks(self):
        'return basemarks for font e.g A'
        return self.base_anchors

    @property
    def accentmarks(self):
        'returns accent mark for font e.g acutecomb'
        return self.mark_anchors

    @property
    def ligmarks(self):
        'returns ligature marks e.g aLamAlif'
        return self.lig_anchors


def designer_gpos_strings(base, accent, font):
    '''Output strings based on Base glyph + Accent glyph. Unfortuantely, non-Latin
    support is flakey at best. Devanagari and complex GSUB scripts which rely on
    pres or liga OT features are not supported at the moment.'''
    text = []
    #loop through both base glyphs and accent glyphs
    for weight in base:
        text.append("\n" + weight + "\n")
        for glyph in base[weight]:
            for mark in accent[weight]:
                for b_anc in base[weight][glyph]:
                    for a_anc in accent[weight][mark]:
                        if b_anc == a_anc[1:]: #chops _top to top on mark glyphs
                            if font.glyphs[glyph].unicode:
                                if font.glyphs[mark].unicode:
                                    text.append('%s%s ' %(font.glyphs[glyph].string,
                                                        font.glyphs[mark].string))
    return ''.join(text).encode('utf-8')

def main():
    font = Glyphs.font
    anchor = AnchorData(font, truncate=True)

    loc = re.split(r'\.ttf|\.otf', font.filepath)[0]

    gpos = open(loc + '_gpos_strings.txt', 'w')
    gpos.write(designer_gpos_strings(anchor.basemarks, anchor.accentmarks, font))
    gpos.close()

    Message('Done', 'Strings saved to %s' %loc)

if __name__ == '__main__':

    if len(Glyphs.fonts) != 1:
        print 'Please only have one font open'
    else:
        main()
