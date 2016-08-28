'''Panose number should not be set to an absolute if the font has instances/weights'''


def check(font):
    print '***Check Panose Assignment***'
    if font.masters > 1 and 'panose' in font.customParameters:
        print 'ERROR: Panose should be unique for each weight instance\n'
    else:
        print 'PASS: Panose is not set as an absolute for family\n'
