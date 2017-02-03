#MenuTitle: Report inconsistent glyph nodes between two fonts

fonts = Glyphs.fonts


def glyphs_coords(glyph, master):
    points = []
    m = master.name
    for path in glyph.layers[m].paths:
        for node in path.nodes:
            points.append((
                node.position[0], node.position[1]
            ))
    return points


def main():
    Glyphs.showMacroWindow()
    inconsistent_glyphs = []
    font1 = fonts[0]
    font2 = fonts[1]

    masters = font1.masters
    if len(font1.masters) != len(font2.masters):
        print 'Fonts do not share same amount of masters, aborting!'
        return

    glyphset1 = set(font1.glyphs.keys())
    glyphset2 = set(font2.glyphs.keys())
    shared_glyphs = glyphset1 & glyphset2
    print 'Checking %s glyphs' % (len(shared_glyphs))
    if len(glyphset1) != len(glyphset2):
        print 'WARNING: [%s] is in either font1 or font2 but not both\n' % (
            ' ,'.join(glyphset1 ^ glyphset2)
        )
    for glyph in shared_glyphs:
        for m, master in enumerate(masters):
            glyph1 = glyphs_coords(font1.glyphs[glyph], master)
            glyph2 = glyphs_coords(font2.glyphs[glyph], master)

            if glyph1 != glyph2:
                inconsistent_glyphs.append((master.name, glyph))

    if inconsistent_glyphs:
        for master, glyph in inconsistent_glyphs:
            print 'ERROR: %s %s is not consistent with other font' % (
                master, glyph
            )
    else:
        print 'PASS: Shared glyphs have same point coordinates'

if __name__ == '__main__':
    if len(fonts) != 2:
        print 'ERROR: Open two files only!'
    else:
        main()
