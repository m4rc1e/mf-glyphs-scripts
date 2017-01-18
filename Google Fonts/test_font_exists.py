#MenuTitle: Test font is on fonts.google.com
"""Test font family exists on fonts.google.com"""
from urllib import urlopen
from utils import logger


API_URL_PREFIX = 'https://fonts.google.com/download?family='


def font_family_url(family_name):
    '''Create the url to download a font family'''
    family_name = family_name.replace(' ', '%20')
    return '%s%s' % (API_URL_PREFIX, family_name)


def googlefonts_version(family_name):
    """Return a zipfile containing a font family hosted on fonts.google.com"""
    logger.test("Font is hosted on fonts.google.com")
    family_url = font_family_url(family_name)
    zipfile = urlopen(family_url)

    if zipfile.getcode() == 200:
        logger.passed('%s is on fonts.google.com' % family_name)
        return zipfile
    else:
        logger.failed('%s is not on fonts.google.com.' % family_name)
        return False


if __name__ == '__main__':
    logger.header1('Running %s' % __file__)
    font = Glyphs.font
    Glyphs.showMacroWindow()
    googlefonts_version(font.familyName)
    print logger
