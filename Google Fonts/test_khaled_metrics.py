#MenuTitle: Test vertical metrics match Khaled's approach
# -*- coding: utf-8 -*-
'''
Check family metrics following Khaleds schema. This shoud be used
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

import os
import operator


GLYPHS_VERT_KEYS = [
    # Glyphsapp custom parameter fields for instance vertical metrics
    'typoAscender',
    'typoDescender',
    'typoLineGap',
    'winAscent',
    'winDescent',
    'hheaAscender',
    'hheaDescender',
    'hheaLineGap',
]

OPERATORS = {
    '>=': operator.ge,
    '==': operator.eq,
    '<=': operator.le
}

LINE_GAP = 0


def shortest_tallest_glyphs(font, *args):
    '''find the tallest and shortest glyphs in all masters.'''
    lowest = 0.0
    highest = 0.0
    highest_name = ''
    lowest_name = ''

    masters_count = len(font.masters)

    if args:
        glyphs = [font.glyphs[i] for i in args]
    else:
        glyphs = font.glyphs

    for glyph in glyphs:
        for i in range(masters_count):
            glyph_ymin = glyph.layers[i].bounds[0][-1]
            glyph_ymax = glyph.layers[i].bounds[-1][-1] + glyph.layers[i].bounds[0][-1]
            if glyph_ymin < lowest:
                lowest = glyph_ymin
            if glyph_ymax > highest:
                highest = glyph_ymax

    return lowest, highest


def ascender_descender(font):
    '''Return the tallest and shallowest ascender and descender from all family masters'''
    ascender = 0.0
    descender = 0.0
    for master in font.masters:
        if master.ascender > ascender:
            ascender = master.ascender
        if master.descender < descender:
            descender = master.descender
    return ascender, descender


def vert_keys(font):
    '''Check whether the .glyphs has the correct vertical metrics parameters
    for each instance.'''
    no_errors = True

    for master in font.masters:
        print('***Check %s instance has mandatory metric attributes***' % master.name)
        for key in GLYPHS_VERT_KEYS:
            if master.customParameters[key] is not None:
                print 'PASS: %s exists' % (key)
            else:
                print('ERROR: %s needed' % (key))
                no_errors = False
    return no_errors


def vert_metrics_match(font):
    '''Check all instances share the same vertical metrics.'''
    master_metrics = {}
    for i, master in enumerate(font.masters):
        master_metrics[i] = {}
        for key in GLYPHS_VERT_KEYS:
            master_metrics[i][key] = float(master.customParameters[key])

    # Compare each instance against the first
    for key in master_metrics:
        for field in master_metrics[key]:
            if master_metrics[key][field] != master_metrics[0][field]:
                print('ERROR: instances do not share same metrics')
                return False
    print('PASS: All instances share same metics')
    return True


def compare(arg1_name, arg1_val, op, arg2_name, arg2_val):
    '''Compare two arguements.'''
    if OPERATORS[op](arg1_val, arg2_val):
        print('PASS: %s %s is %s to %s %s' %
              (arg1_name, arg1_val, op, arg2_name, arg2_val))
    else:
        print('ERROR: %s %s is not %s to %s %s' %
              (arg1_name, arg1_val, op, arg2_name, arg2_val))


def main_glyphsapp():
    print('***KHALED METRICS SCHEME***\n')
    font = Glyphs.font
    ymin, ymax = shortest_tallest_glyphs(font)
    family_ascender, family_descender = ascender_descender(font)

    vmetric_fields = vert_keys(font)

    print('\n***Instances share same vertical metrics***')
    consistent_vert_instances = vert_metrics_match(font)

    if vmetric_fields and consistent_vert_instances:
        master = font.masters[0]
        vmfield = master.customParameters

        print("\n***Check vertical metrics match***")

        compare('Win Ascent', vmfield['winAscent'], '>=', 'yMax', ymax)
        compare('Win Descent', vmfield['winDescent'], '>=', 'yMin', abs(ymin)) # abs so its positive integer

        compare('Typo Ascender', vmfield['typoAscender'], '==', 'hhea Ascender', vmfield['hheaAscender'])
        compare('Typo Descender', vmfield['typoDescender'], '==', 'hhea Descender', vmfield['hheaDescender'])
        compare('Typo Ascender', vmfield['typoAscender'], '>=', 'Family Ascender', family_ascender)
        compare('Typo Descender', vmfield['typoDescender'], '<=', 'Family Descender', family_descender)

        compare('Typo Line Gap', vmfield['typoLineGap'], '==', 'No Line Gap', LINE_GAP)
        compare('hhea Line Gap', vmfield['hheaLineGap'], '==', 'No Line Gap', LINE_GAP)
    else:
        print('\nERROR: Add all Vertical metrics fields for each instance first \
              and check each instance has same metrics')


if __name__ == '__main__':
    try:
        __glyphsfile__ = Glyphs.font.filepath
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__glyphsfile__), '..'))
        main_glyphsapp()
    except NameError:
        print 'Glyphsapp only for now'
