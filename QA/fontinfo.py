import re


def check_field(key, yml, font, fix=False):
    '''Check if a font's attribute matches the yml document'''
    if 'any' in str(yml):
        print 'PASS: font %s has attribute\n' % key
    elif yml != font:
        print 'ERROR: font %s is not equal to yml %s\n' % (key, key)
    else:
        print 'PASS: font %s is equal to yml %s\n' % (key, key)
    if fix:
        font = yml


def font_field(font, key):
    '''Check font has key'''
    if hasattr(font, key):
        return getattr(font, key)
    if key in font.customParameters:
        return font.customParameters[key]
    return None


def check_family_name(fontname):
    '''Check if family name has non ascii characters as well as dashes, number
    and diacritics as well.'''
    print('***Check family name has only ASCII characters***')
    try:
        fontname.decode('ascii')
        illegal_char_check = re.search(r'[\-\\/0-9]+', fontname)
        if illegal_char_check:
            print('ERROR: Font family "%s", contains numbers, slashes or dashes.' % fontname)
            return False
    except UnicodeDecodeError:
        print('ERROR: Font family name %s, has non ascii characters' % fontname)
        return False
    print('PASS: Family name is correct\n')
    return True


def panose(font):
    '''Panose number should not be set to an absolute if the font has
    instances/weights'''
    print '***Check Panose Assignment***'
    if font.masters > 1 and 'panose' in font.customParameters:
        print 'ERROR: Panose should be unique for each weight instance\n'
    else:
        print 'PASS: Panose is not set as an absolute for family\n'
