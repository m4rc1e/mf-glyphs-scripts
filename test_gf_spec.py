'''
Automate Google Font project Spec.

'''
import os
import re

try:
    __glyphsfile__ = Glyphs.fonts[0].filepath
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__glyphsfile__), '..'))
except NameError:
    project_dir = os.getcwd()


PROJECT_FILES = {
    'licence': 'OFL.txt',
    'contributors': 'CONTRIBUTORS.txt',
    'trademark': 'TRADEMARKS.md',
    }

COMPULSORY_FOLDERS = [
    'sources',
    'fonts'
    ]

SETTINGS = {
    'upm': 1000,
    'fstype': 4
}

LICENCE_META = 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL'
LICENCE_URL_META = 'http://scripts.sil.org/OFL'

def file_exists(proj_file, project_path):
    if proj_file in os.listdir(project_path):
        print('%s exists' % proj_file)
        return True
    else:
        print('%s is missing' % proj_file)
        return False


def folders_exist(directory):
    '''Check project has compulsory folders'''
    folders = []
    for f in os.listdir(directory):
        abs_file_path = os.path.join(directory, f)
        if os.path.isdir(abs_file_path):
            folders.append(f)

    for f in COMPULSORY_FOLDERS:
        if f not in folders:
            print('missing %s' % f)


def check_ofl_matches_copyright_string(ofl, c_string):
    if c_string in ofl.readlines()[0]:
        print('copyright matches')
    else:
        print('First line of ofl does not match copyright')


def is_source_file():
    '''Quickly check if .glyphs file in source folder is a source file.
    This method should be taken as a pinch of salt.'''
    pass


def check_family_vert_metrics():
    '''Check the family metrics follow Kalapi's schema.'''
    pass


def check_vender_id_string(family_vendor):
    if family_vendor


def check_gasp_table():
    pass


def check_family_fstype(family_fstype):
    '''Fs_type must be set to installable. In Glyphsapp api this is int 4, spec says 0'''
    if int(family_fstype) != SETTINGS['fstype']:
        print 'Change fsType to installable'
        return False
    return True


def check_family_upm(family_upm):
    '''Check upm is 1000'''
    if int(family_upm) != SETTINGS['upm']:
        print 'Family upm is not equal to %s' % SETTINGS['upm']
        return False
    return True


def check_family_name(fontname):
    '''Check if family name has non ascii characters as well as
    dashes, numbers and diacritics as well.'''
    try:
        fontname.decode('ascii')
        illegal_char_check = re.search(r'[\-\\/0-9]+', fontname)
        if illegal_char_check:
            print('Err: Font family "%s", contains numbers, slashes or dashes.' % fontname)
            return False
    except UnicodeDecodeError:
        print('Font family name %s, has non ascii characters' % fontname)
        return False
    return True


def check_license_string(family_license_string):
    if family_license_string is not LICENCE_META:
        print 'Family licence string is incorrect'
        return False
    return True


def check_license_url_string(family_license_url):
    if family_license_url is not LICENCE_URL_META:
        print 'Family licence url string is incorrect'
        return False
    return True







def main():
    # Check project structure
    file_exists(PROJECT_FILES['licence'], project_dir)
    file_exists(PROJECT_FILES['contributors'], project_dir)
    folders_exist(project_dir, COMPULSORY_FOLDERS)

    if file_exists(PROJECT_FILES['licence'], project_dir):
        with open(os.path.join(project_dir, PROJECT_FILES['licence']), 'r') as ofl_file:
            check_ofl_matches_copyright_string(ofl_file, Glyphs.fonts[0].copyright)
    else:
        print('cannot check first line of OFL matches copyright string')

    # Trademark check
    # check vendor
    # GASP table

    check_family_name(Glyphs.fonts[0].familyName)


if __name__ == '__main__':
    main()
