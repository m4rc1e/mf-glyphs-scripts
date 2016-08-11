#MenuTitle: Set all masters uni00A0 width to Space width
# -*- coding: utf-8 -*-
'''
Set uni00A0 to same width as space
'''
def main():
    font = Glyphs.font
    masters = font.masters
    for id in range(len(masters)):
        font.glyphs['uni00A0'].layers[id].width = font.glyphs['space'].layers[id].width
        print 'Now equal widths! space=%s, 00A0=%s' %(
        font.glyphs['space'].layers[id].width,
        font.glyphs['uni00A0'].layers[id].width
        )

if __name__ == '__main__':
    main()
