#MenuTitle: Generate Kern Report & Strings

'''Script outputs kerning table and generates proofable strings

To do:
    Support for non-Latin scripts.

Release history:
    2015/08/29:
    V0.001: This is the first release
'''

import GlyphsApp
import unicodedata as uni
import re

__ver__ = 0.1
__author__ = 'Marc Foley'


class KernData(object):
    '''Wrapper for Glyphsapp Kern table. The Glyph.font.kerningDict() dictionary is
    very difficult to work with.'''
    def __init__(self, font):

        self.font = font

        self.kern_table = self.font.kerningDict()

        #Unnesting font.kerningDict() it is a multi levelled beast!
        self.all_kerns = {}
        for step, glyph in enumerate(self.kern_table):
            c_layer = str(Glyphs.font.masters[step]).split('"')[1]
            self.all_kerns[c_layer] = []
            for left in self.kern_table[glyph]:
                for right in self.kern_table[glyph][left]:
                    self.all_kerns[c_layer].append(
                        (left, right, self.kern_table[glyph][left][right]))

    @property
    def table(self):
        '''Output unnested kern table'''
        return self.all_kerns

    @property
    def classes(self):
        '''return list of tuples (name, l_kern class, r_kern class)'''
        return [(glyph.name,
                glyph.leftKerningGroup,
                glyph.rightKerningGroup) for glyph in self.font.glyphs]

    def round_kerning(self):
            '''Round floats to integers for kerning pairs'''
            pass

def kern_report(kern):
    '''Output kerning table.'''

    text = []
    for layer in kern:
        pair = kern[layer]
        text.append(layer +' \n')
        for left, right, value in pair:
            text.append('%s,%s,%s\n' %(left, right, value))
    return ''.join(text)    


def designer_kern_strings(kern, font):
    '''Builds strings which are parsed according to their sub category.
    If the unicode name features "UPPER", it will be set with OO, HH.
    If the name has "Lower", oo, nn are used instead. Unfortuantely,
    this technique can only parse Latin, Greek and Cyrillic. I would
    like to make my own parser so we can support non-Latins'''
    text = []
    for layer in kern:
        pair = kern[layer]
        text.append('\n' + layer +'\n')

        for left, right, value in pair:
                #Truncate class to main class key e.g @mmk_l_r = r
            if '@' in left:
                l_kern = font.glyphs[left[7:].split('_')[0]]
            else:
                l_kern = font.glyphs[left]

            if '@' in right:
                r_kern = font.glyphs[right[7:].split('_')[0]]
            else:
                r_kern = font.glyphs[right]

            if l_kern != None and l_kern.unicode:
                if r_kern != None and r_kern.unicode:
                
                    try:
                        if 'Lowercase' in l_kern.subCategory:
                            l_pair = 'oo%s' % l_kern.string
                            l_pair2 = 'nn%s' % l_kern.string
                        else:
                            l_pair = 'OO%s' % l_kern.string
                            l_pair2 = 'HH%s' % l_kern.string
        
                        if 'Lowercase' in r_kern.subCategory:
                            r_pair = '%soo' % r_kern.string
                            r_pair2 = '%snn' % r_kern.string
                        else:
                            r_pair = '%sOO' % r_kern.string
                            r_pair2 = '%sHH' % r_kern.string
                    except:
                        AttributeError
                    string = '%s%s%s%s\n' %(l_pair, r_pair, l_pair2, r_pair2)
                    text.append(string)

    return ''.join(text).encode('utf-8')


def main():

    font = Glyphs.font
    kern = KernData(font)

    loc = re.split(r'\.ttf|\.otf', font.filepath)[0]

    report = open(loc + '_kern_report.txt', 'w')
    report.write(kern_report(kern.table))
    report.close()

    string = open(loc + '_kern_strings.txt', 'w')
    string.write(designer_kern_strings(kern.table, font))
    string.close()

    Message('Done', 'Reports & Strings saved to %s' %loc)


if __name__ == '__main__':

    if len(Glyphs.fonts) != 1:
        print 'Please only have one font open'
    else:
        main()
