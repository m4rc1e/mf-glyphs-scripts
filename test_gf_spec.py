#MenuTitle: Test repo matches gf-checklist structure
'''
Check project fulfills Google Font project Spec.

'''
import os
import re

__author__ = 'Marc Foley'
__version__ = '0.001'

try:
    __glyphsfile__ = Glyphs.font.filepath
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__glyphsfile__), '..'))
except NameError:
    project_dir = os.getcwd()


PROJECT_FILES = {
    'licence': 'OFL.txt',
    'contributors': 'CONTRIBUTORS.txt',
    'trademark': 'TRADEMARKS.md',
    'readme': 'README.md',
    }

COMPULSORY_FOLDERS = [
    'sources',
    'fonts'
    ]

SETTINGS = {
    'upm': 1000,
    'fstype': 0,
}

LICENCE_META = 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL'
LICENCE_URL_META = 'http://scripts.sil.org/OFL'


def file_exists(proj_file, project_path):
    if proj_file in os.listdir(project_path):
        print('PASS: %s exists' % proj_file)
        return True
    else:
        print('ERROR: %s is missing' % proj_file)
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
            print('ERROR: %s folder missing' % f)
        else:
            print('PASS: %s folder exists' % f)


def check_ofl_matches_copyright_string(ofl, c_string):
    if c_string not in ofl.readlines()[0]:
        print('ERROR: First line of ofl does not match copyright')
        return False
    else:
        print('PASS: copyright matches')
        return True


def check_vender_id_string(family_vendor):
    if family_vendor:
        print 'PASS: font has vendorId'
        return True
    else:
        print 'POSSIBLE ERROR: font is missing vendorId'
        return False


def check_family_upm(family_upm):
    '''Check upm is 1000'''
    if int(family_upm) != SETTINGS['upm']:
        print 'POSSIBLE ERROR: Family upm is not equal to %s' % SETTINGS['upm']
        return False
    else:
        print('PASS: Family upm is equal to %s' % SETTINGS['upm'])
        return True


def check_family_name(fontname):
    '''Check if family name has non ascii characters as well as
    dashes, numbers and diacritics as well.'''
    try:
        fontname.decode('ascii')
        illegal_char_check = re.search(r'[\-\\/0-9]+', fontname)
        if illegal_char_check:
            print('ERROR: Font family "%s", contains numbers, slashes or dashes.' % fontname)
            return False
    except UnicodeDecodeError:
        print('ERROR: Font family name %s, has non ascii characters' % fontname)
        return False
    print('PASS: Family name is correct')
    return True


def check_license_string(family_license_string):
    if family_license_string == LICENCE_META:
        print('PASS: Family license string is correct')
        return True
    else:
        print('ERROR: Family license string is incorrect')
        return True


def check_license_url_string(family_license_url):
    if family_license_url == LICENCE_URL_META:
        print('PASS: Family license url is correct')
        return False
    else:
        print('ERROR: Family license url string is incorrect')
        return True


def check_family_fstype(font_fstype):
    # if font_fstype == SETTINGS['fstype']:
    #     print('PASS: Family fsType matches %s' % SETTINGS['fstype'])
    # else:
    #     print('ERROR: Family fsType does not match %s' % SETTINGS['fstype'])
    print('ERROR in GlyphsApp: Make sure fsType is installable (0 Ms Spec)')

def main():
    # Check project structure
    font = Glyphs.font
    file_exists(PROJECT_FILES['readme'], project_dir)
    file_exists(PROJECT_FILES['licence'], project_dir)
    file_exists(PROJECT_FILES['contributors'], project_dir)
    folders_exist(project_dir)

    if file_exists(PROJECT_FILES['licence'], project_dir):
        with open(os.path.join(project_dir, PROJECT_FILES['licence']), 'r') as ofl_file:
            check_ofl_matches_copyright_string(ofl_file, Glyphs.fonts[0].copyright)
    else:
        print('cannot check first line of OFL matches copyright string')

    if font.customParameters['trademark']:
        if file_exists(PROJECT_FILES['trademark'], project_dir):
            print 'PASS: Font has trademark and file is present'
        else:
            print 'POSSIBLE ERROR: Font has trademark but no %s' % PROJECT_FILES['trademark']

    if file_exists(PROJECT_FILES['trademark'], project_dir):
        if font.customParameters['trademark']:
            print 'PASS: Font has trademark and file is present'
        else:
            print 'POSSIBLE ERROR: %s file exists but font does not have trademark' % PROJECT_FILES['trademark']

    check_vender_id_string(font.customParameters['vendorID'])

    check_license_string(font.customParameters['license'])
    check_license_url_string(font.customParameters['licenseURL'])

    check_family_name(font.familyName)
    check_family_upm(font.upm)
    check_family_fstype(font.customParameters['fsType'])


if __name__ == '__main__':
    main()