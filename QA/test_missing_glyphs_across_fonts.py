#MenuTitle: Check glyphs match across open fonts
'''
Find missing glyphs across fonts
'''
def main():
    fonts = Glyphs.fonts
    glyphsets = {}
    try:
        for font in fonts:
            if font.instances[0].name not in glyphsets:
                glyphsets[font.instances[0].name] = set()
            
            print 'Name: %s, Glyphs: %s' % (font.instances[0].name, len(font.glyphs))
            for glyph in font.glyphs:
                glyphsets[font.instances[0].name].add(glyph.name)
        
        for font1 in glyphsets:
            for font2 in glyphsets:
                diff_glyphs = glyphsets[font1] - glyphsets[font2]
                print font1, '-', font2, diff_glyphs

    except AttributeError:
        print 'Font does not have any instances'
        raise
            
            
if __name__ == '__main__':
    main()
