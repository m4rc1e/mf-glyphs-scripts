#MenuTitle: Test each master has correct vertical metrics keys
"""
Each master needs the following customParameters

    typoAscender
    typoDescender
    typoLineGap

    winAscent
    winDescent

    hheaAscender
    hheraDescender

Keys are required in order to fulfill our different metrics schemas

"""
from vertmetrics import VERT_KEYS
from utils import logger


def master_vert_keys_missing(master):
    """Check master has the required metrics keys"""
    missing_keys = []
    for key in VERT_KEYS:
        if key not in master.customParameters:
            missing_keys.append(key)
    return missing_keys


def test_font_vert_keys(masters):
    """Check the font's masters has all the required metrics keys"""
    bad_masters = []

    logger.test("Font masters have all vertical metric keys")
    for master in masters:
        missing_keys = master_vert_keys_missing(master)
        if missing_keys:
            logger.failed('%s master missing keys:' % master.name)
            logger.bullets(missing_keys)
            bad_masters.append(master.name)
        else:
            logger.passed('%s master has all vert metrics keys' % master.name)

    if bad_masters:
        return False
    return True


if __name__ == '__main__':
    logger.header1('Running %s' % __file__)
    font = Glyphs.font
    Glyphs.showMacroWindow()
    test_font_vert_keys(font.masters)
    print logger
