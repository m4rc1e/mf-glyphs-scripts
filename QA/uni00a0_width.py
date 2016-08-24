# -*- coding: utf-8 -*-
'''
Set nbspace to same width as space
'''
def check(font, masters, fix=False):
    print '***Checking space and nbspace have same width***'
    for id in range(len(masters)):
        if font.glyphs['nbspace'].layers[id].width != font.glyphs['space'].layers[id].width:
            print 'ERROR: nbspace and space are not same width\n'
        else:
            print 'PASS: nbspace and space are same width\n'

        if fix:
            font.glyphs['nbspace'].layers[id].width = font.glyphs['space'].layers[id].width
            print 'Now equal widths! space=%s, 00A0=%s' %(
            font.glyphs['space'].layers[id].width,
            font.glyphs['nbspace'].layers[id].width
            )


if __name__ == '__main__':
    font = Glyphs.font
    masters = font.masters
    check(font, masters)
