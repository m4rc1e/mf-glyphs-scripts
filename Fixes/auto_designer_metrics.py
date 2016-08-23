#MenuTitle: Auto designer vert metrics
'''
Replace metrics with values calculated from key glyphs.
'''

font = Glyphs.font

ASC_G = 'l'
CAP_G = 'H'
XHEIGHT_G = 'x'
DESC_G = 'p'

masters = font.masters


for i,master in enumerate(masters):
    n_asc = font.glyphs[ASC_G].layers[master.id].bounds[-1][-1] - abs(font.glyphs[ASC_G].layers[master.id].bounds[0][-1])
    n_cap = font.glyphs[CAP_G].layers[master.id].bounds[-1][-1]
    n_xhe = font.glyphs[XHEIGHT_G].layers[master.id].bounds[-1][-1]
    n_desc = font.glyphs[DESC_G].layers[master.id].bounds[0][-1]
    
    master.ascender = n_asc
    master.capHeight = n_cap
    master.xHeight = n_xhe
    master.descender = n_desc
    
print 'Designer vertical metrics updated'
