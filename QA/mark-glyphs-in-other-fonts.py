#MenuTitle: Mark glyphs which exist in open fonts
# -*- coding: utf-8 -*-

__doc__ = '''Mark glyphs in the selected font which exist in all opened fonts'''
from copy import copy

all_glyphs = set()
for i, font in enumerate(Glyphs.fonts):
    for glyph in font.glyphs:
        all_glyphs.add(glyph.name)

shared_glyphs = copy(all_glyphs)
for font in Glyphs.fonts:
    glyphs = set(g.name for g in font.glyphs)
    shared_glyphs.intersection_update(glyphs)

current_font = Glyphs.fonts[0]
for name in shared_glyphs:
    current_font.glyphs[name].color = 4
