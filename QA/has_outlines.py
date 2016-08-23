'''
Check if glyphs are missing outlines or composites.
Only works on glyphs which have unicodes
'''
import unicodedata as uni

IGNORE_GLYPHS_OUTLINE = [
	'uni0000'	
]

def check(font):
	print '***Check Glyphs have outlines or components***'
	masters = font.masters
	for i, master in enumerate(masters):
		for glyph in font.glyphs:

			if str(glyph.category) != 'Separator' and glyph.name not in IGNORE_GLYPHS_OUTLINE:
				if len(glyph.layers[i].paths) == 0:
					if len(glyph.layers[i].components) == 0:
	 					print 'ERROR: %s %s should have outlines or components' % (master.name, glyph.name)


if __name__ == '__main__':
	font = Glyphs.font
	check(font)
