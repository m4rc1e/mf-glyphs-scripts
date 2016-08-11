#MenuTitle: Fix selected composite metrics
# -*- coding: utf-8 -*-
'''
Set selected glyphs metrics to parent glyph.

e.g:
    Aacute -> A
    Agrave, Acute -> A, A

This works by glyph names only. Can also do small caps.

Note: This is extremely ghetto.
'''
def main():
    align_dict = {}
    font = Glyphs.font
    glyphs = Glyphs.font.selection
    
    for glyph in glyphs:
        if '.sc' not in glyph.name:
            if str(glyph.name[0]) not in align_dict:
                align_dict[str(glyph.name[0])] = [glyph.name]
            else:
                align_dict[str(glyph.name[0])].append(glyph.name)
        else:
            if str(glyph.name[0] + '.sc') not in align_dict:
                align_dict[str(glyph.name[0] + '.sc')] = [glyph.name]
            else:
                align_dict[str(glyph.name[0] + '.sc')].append(glyph.name)
    
    # Set metrics to key
    masters = font.masters
    for parent in align_dict:
        for i in range(len(masters)):
            for glyph in align_dict[parent]:
                font.glyphs[glyph].layers[i].RSB = font.glyphs[parent].layers[i].RSB
                font.glyphs[glyph].layers[i].LSB = font.glyphs[parent].layers[i].LSB
    print('metrics updated')
    

if __name__ == '__main__':
    main()
