import re

def check_family_name(fontname):
    '''Check if family name has non ascii characters as well as
    dashes, numbers and diacritics as well.'''
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