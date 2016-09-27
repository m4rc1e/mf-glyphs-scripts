from collections import Counter
import unicodedata as uni

IGNORE_GLYPHS_OUTLINE = [
    'uni0000',
    'NULL',
]


def find_duplicates(font_glyphs):
    '''Check if there are duplicate glyphs'''
    print '**Find Duplicate glyphs in selected font**'
    glyphs_count = Counter(font_glyphs)
    if len(set(glyphs_count.values())) >= 2:
        for glyph in glyphs_count:
            if glyphs_count[glyph] >= 2:
                print 'ERROR: %s duplicated\n' % glyph
    else:
        print 'PASS: No duplicate glyphs\n'


def outlines_missing(font):
    '''Check if glyphs are missing outlines or composites.
    Only works on glyphs which have unicodes'''
    print '**Check Glyphs have outlines or components**'
    masters = font.masters

    for i, master in enumerate(masters):
        bad_glyphs = []
        for glyph in font.glyphs:

            if str(glyph.category) != 'Separator' and glyph.name not in IGNORE_GLYPHS_OUTLINE:
                if len(glyph.layers[i].paths) == 0:
                    if len(glyph.layers[i].components) == 0:
                        bad_glyphs.append(glyph.name)

        if bad_glyphs:
            for glyph in bad_glyphs:
                print "ERROR: %s master's %s should have outlines or components\n" % (master.name, glyph)            
        else:
            print "PASS: %s master's glyphs have components or outlines\n" % master.name

def find_duplicate_components(glyphs):
    '''Find duplicate components in the same glyph and share
    the same affine transformation.
    This happens when Glyphs generates a glyph like quotedblright.'''
    print '**Find duplicate components that share the same position/transformation.**'
    no_error = True
    for glyph in glyphs:
        for layer in glyph.layers:
            all_transformations = {}
            all_components = {}
            for component in layer.components:
                name = component.componentName
                if name not in all_components:
                    all_components[name] = []
                    all_transformations[name] = set()
                all_components[name].append(component)
                all_transformations[name].add(tuple(component.transform))
            for name, components in all_components.iteritems():
                transformations = all_transformations[name];
                if len(transformations) != len(components):
                    no_error = False
                    print ('ERROR: glyph {glyph} layer {layer}: {count_c} '
                        + 'components of {component} share {count_t} '
                        + 'transformations.\n    '
                        + 'All components of the same type must be positioned '
                        + 'differently.\n').format(
                                                glyph=glyph.name,
                                                layer=layer.name,
                                                count_c=len(components),
                                                component=name,
                                                count_t=len(transformations))
    if no_error:
        print 'PASS: no duplicate components share the same spot.\n'
