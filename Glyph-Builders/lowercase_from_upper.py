#MenuTitle: Generate lowercase from uppercase
"""
Generate lowercase a-z from uppercase A-Z

TODO (M Foley) Generate all lowercase glyphs, not just a-z
"""

font = Glyphs.font
glyphs = list('abcdefghijklmnopqrstuvwxyz')
masters = font.masters

for glyph_name in glyphs:
    glyph = GSGlyph(glyph_name)
    glyph.updateGlyphInfo()
    font.glyphs.append(glyph)
    
    for idx,layer in enumerate(masters):
        comp_name = glyph_name.upper()
        component = GSComponent(comp_name, (0,0))
        glyph.layers[idx].components.append(component)

Glyphs.redraw()
