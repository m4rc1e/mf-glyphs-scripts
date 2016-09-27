def dynamic_fraction(font):
    '''If font has fivesuperior, there should be a dynamic fraction feature'''
    print '**Checking frac feature**'
    if 'fivesuperior' in font.glyphs:
        if font.features['frac']:
            if "'" in str(font.features['frac'].code):
                print 'PASS: Font has dynamic frac feature\n'
            else:
                print 'POSSIBLE ERROR: frac feature may not be dynamic\n'
        else:
            print 'ERROR: no frac OT feature\n'
    else:
        print 'PASS: font does not have 4-9 numerators glyphs, no'\
        'dynamic frac needed\n'
