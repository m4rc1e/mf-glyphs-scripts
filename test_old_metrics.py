import os

GLYPHS_VERT_KEYS = {
    # Glyphsapp custom parameter fields for instance vertical metrics
    'typo_asc': 'typoAscender',
    'typo_desc': 'typoDescender',
    'typo_line': 'typoLineGap',
    'win_asc': 'winAscent',
    'win_desc': 'winDescent',
    'hhea_asc': 'hheaAscender',
    'hhea_desc': 'hheaDescender',
    'hhea_line': 'hheaLineGap',
}

def get_family_ybounds(font):
    '''Glyphsapp does not proding the head tables bounding box info. We can make
    this ourselves by looping through each layer and finding the highest and lowerst
    glyph.'''
    lowest = 0.0
    highest = 0.0
    highest_name = ''
    lowest_name = ''

    masters_count = len(font.glyphs['A'].layers)

    for glyph in font.glyphs:
        for i in range(masters_count):
            glyph_ymin = glyph.layers[i].bounds[0][-1]
            glyph_ymax = glyph.layers[i].bounds[-1][-1] + glyph.layers[i].bounds[0][-1]
            if glyph_ymin < lowest:
                lowest = glyph_ymin
                lowest_name = glyph.name
            if glyph_ymax > highest:
                highest = glyph_ymax
                highest_name = glyph.name

    return lowest, highest


def get_glyphsapp_ascender_descender(font):
    '''Return the tallest and shallowest ascender and descender from all family masters'''
    ascender = 0.0
    descender = 0.0
    for master in font.masters:
        if master.ascender > ascender:
            ascender = master.ascender
        if master.descender < descender:
            descender = master.descender
    return ascender, descender


def check_glyphsapp_has_vert_keys(font):
    '''Check whether the .glyphs has the correct vertical metrics parameters
    for each instance.'''
    no_errors = True

    for instance in font.instances:
        print('***Check %s instance has mandatory metric attributes***' % instance.name)
        for key in GLYPHS_VERT_KEYS.values():
            if instance.customParameters[key] is not None:
                print 'PASS: %s exists' % (key)
            else:
                print('ERROR: %s needed' % (key))
                errors = False
    return no_errors


def check_khaled_vmetrics(
    os2_typo_ascender,
    os2_typo_descender,
    os2_linegap,
    os2_win_ascender,
    os2_win_descender,
    hhea_ascender,
    hhea_descender,
    hhea_linegap,
    ymin,
    ymax,
    viz_ascender,
    viz_descender
):
    '''Check family metrics following Khaleds schema. This shoud be used
    for old fonts.

    Proposed in https://groups.google.com/forum/#!topic/googlefonts-discuss/W4PHxnLk3JY,
    Date: 2016/07/20

    1) Set OS/2 Typo and hhea metrics to the values that gives the desired
   line spacing for *non Vietnamese text*.
    2) Set OS/2 fSelection “USE_TYPO_METRICS” bit.
    3) Set OS/2 Win metrics to big enough value to avoid any clipping.
    linegaps = 0
    os/2 win metrics should be at least the font bbox

    > I chatted with Kalapi about this and perhaps this is implicit in your
    > analysis: the typo and hhea metrics are 125 percent of the UPM, and linegaps are 0?

    If 125 percent UPM give the desired line spacing then yes, and yes 0 line gap.
    '''
    line_gap = 0

    print("***Check vertical metrics match Khaled's approach***")

    if os2_win_ascender >= ymax:
        print('PASS: OS/2 win ascent %s is greater or equal to ymax %s' %
              (os2_win_ascender, ymax))
    else:
        print('ERROR: OS/2 win ascent %s must be greater than or equal to %s' %
              (os2_win_ascender, ymax))

    if os2_win_descender >= abs(ymin):
        print('PASS: OS/2 win descender %s is less than or equal to %s' %
              (os2_win_descender, ymin))
    else:
        print('ERROR: OS/2 win descender %s must be greater than or equal to %s' %
              (os2_win_descender, abs(ymin)))

    if os2_typo_ascender == hhea_ascender:
        print('PASS: OS/2 Ascender %s matches hhea Ascender %s' %
              (os2_typo_ascender, hhea_ascender))
    else:
        print('ERROR: OS/2 Ascender %s does not match hhea Ascender %s' %
              (os2_typo_ascender, hhea_ascender))

    if os2_typo_descender == hhea_descender:
        print('PASS: OS/2 Descender %s matches hhea Descender %s' %
              (os2_typo_descender, hhea_descender))
    else:
        print('ERROR: OS/2 Descender %s does not match hhea Descender %s' %
              (os2_typo_descender, hhea_descender))

    if os2_linegap == line_gap or hhea_linegap == line_gap:
        print('PASS: linegaps are equal to %s' % line_gap)
    else:
        print('ERROR: linegaps are not equal to %s' % line_gap)

    if os2_typo_ascender >= viz_ascender:
        print('PASS: OS/2 Ascender %s is greater than or equal to Font Ascender %s' %
              (os2_typo_ascender, viz_ascender))
    else:
        print('ERROR: OS/2 Ascender %s is less than Font Ascender %s' %
              (os2_typo_ascender, viz_ascender))

    if os2_typo_descender <= viz_descender:
        print('PASS: OS/2 Descender %s is less than Font Descender %s' %
              (os2_typo_descender, viz_descender))
    else:
        print('ERROR: OS/2 Descender %s is greater than Font Descender %s' %
              (os2_typo_descender, viz_descender))


def main_glyphsapp():
    font = Glyphs.font

    ybounds = get_family_ybounds(font)
    ymax, ymin = ybounds[0], ybounds[1]

    family_asc_desc = get_glyphsapp_ascender_descender(font)
    family_ascender, family_descender = family_asc_desc[0], family_asc_desc[1]

    vmetric_check = check_glyphsapp_has_vert_keys(font)

    if vmetric_check:
        for instance in font.instances:
            check_khaled_vmetrics(
                instance.customParameters[GLYPHS_VERT_KEYS['typo_asc']],
                instance.customParameters[GLYPHS_VERT_KEYS['typo_desc']],
                instance.customParameters[GLYPHS_VERT_KEYS['typo_line']],
                instance.customParameters[GLYPHS_VERT_KEYS['win_asc']],
                instance.customParameters[GLYPHS_VERT_KEYS['win_desc']],
                instance.customParameters[GLYPHS_VERT_KEYS['hhea_asc']],
                instance.customParameters[GLYPHS_VERT_KEYS['hhea_desc']],
                instance.customParameters[GLYPHS_VERT_KEYS['hhea_line']],
                ymax,
                ymin,
                family_ascender,
                family_descender
            )
    else:
        print('ERROR: Add all Vertical metrics fields for each instance first')


if __name__ == '__main__':
    main_glyphsapp()
#     try:
#         __glyphsfile__ = Glyphs.font.filepath
#         project_dir = os.path.abspath(os.path.join(os.path.dirname(__glyphsfile__), '..'))
#         main_glyphsapp()
#     except NameError:
#         print 'Glyphsapp only for now'
