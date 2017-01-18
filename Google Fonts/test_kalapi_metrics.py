#MenuTitle: Test vertical metrics match Kalapi's approach
# -*- coding: utf-8 -*-
'''
Check family metrics following Kalapis schema. This shoud be used
for new fonts.

Proposed in https://groups.google.com/forum/#!topic/googlefonts-discuss/W4PHxnLk3JY,
Date: 2016/07/20

OS/2 sTypoAscender: highest extent of capital 'H' or lowercase ascender 'h', whichever is taller
OS/2 sTypoDescender: Font UPM - OS/2 sTypoAscender
OS/2 sTypoLineGap: 250 (to compensate for the 125% legacy)

OS/2 usWinAscent: == yMax (head table)
OS/2 usWinDescent: == yMin (head table)

hhea ascent: == OS/2 sTypoAscender
hhea descent: == OS/2 sTypoDescender
hhea linegap: == OS/2 sTypoLineGap
'''

import os
import operator
import math

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

LINE_GAP = 250


def shortest_tallest_glyphs(font, *args):
    '''find the tallest and shortest glyphs in all masters from a list.
    If no list is given, search all glyphs.'''
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

    return math.ceil(lowest), math.ceil(highest)


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
    print('***KALAPI METRICS SCHEME***\n')
    font = Glyphs.font
    Glyphs.showMacroWindow()
    ymin, ymax = shortest_tallest_glyphs(font)
    shortest_glyph, tallest_glyph = shortest_tallest_glyphs(font, 'h', 'H')
    family_ascender, family_descender = ascender_descender(font)

    vmetric_fields = vert_keys(font)
    if vmetric_fields:
        print('\n***Instances share same vertical metrics***')
        consistent_vert_instances = vert_metrics_match(font)
    else:
        print('\nERROR: Add all Vertical metrics fields')
        return

    if consistent_vert_instances:
        master = font.masters[0]
        vmfield = master.customParameters
    else:
        print('\nERROR: Check each instances have the same metrics')
        return

    print("\n***Check vertical metrics match***")

    compare('Win Ascent', vmfield['winAscent'], '>=', 'yMax', ymax)
    compare('Win Descent', vmfield['winDescent'], '>=', 'yMin', abs(ymin)) # abs so its a positive integer

    compare('Typo Ascender', vmfield['typoAscender'], '==', 'Tallest h or H', tallest_glyph)
    compare('Typo Descender', vmfield['typoDescender'], '==', 'UPM - Typo Asc', -(font.upm - vmfield['typoAscender']))

    compare('Typo Ascender', vmfield['typoAscender'], '==', 'hhea Ascender', vmfield['hheaAscender'])
    compare('Typo Descender', vmfield['typoDescender'], '==', 'hhea Descender', vmfield['hheaDescender'])

    compare('Typo Line Gap', vmfield['typoLineGap'], '==', 'Line Gap', LINE_GAP)
    compare('hhea Line Gap', vmfield['hheaLineGap'], '==', 'Line Gap', LINE_GAP)


if __name__ == '__main__':
    __glyphsfile__ = Glyphs.font.filepath
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__glyphsfile__), '..'))
    main_glyphsapp()
