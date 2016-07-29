#MenuTitle: Mark glyphs which exist in open fonts
# -*- coding: utf-8 -*-

__doc__ =
'''Mark glyphs in the selected font which exist in all opened fonts'''
from copy import copy

all_glyphs = set()
for i, font in enumerate(Glyphs.fonts):
    for glyph in font.glyphs:
        all_glyphs.add(glyph.name)

shared_glyphs = copy(all_glyphs)
for font in font_glyphs:
    shared_glyphs.intersection_update(font_glyphs[font])

# current font is the font which is top most selected in the ui
current_font = Glyphs.fonts[0]

for name in shared_glyphs:
    current_font.glyphs[name].color = 4
