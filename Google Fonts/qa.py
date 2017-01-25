#MenuTitle: QA
from urllib import urlopen
from utils import logger
from fontTools.ttLib import TTFont

from StringIO import StringIO
from zipfile import ZipFile
import re
from vertmetrics import VERT_KEYS, shortest_tallest_glyphs
from testfuncs import (
    compare,
    consistent,
    leftover,
    enabled,
    contains,
    regex_contains,
)

API_URL_PREFIX = 'https://fonts.google.com/download?family='


FONT_ATTRIBS = [
    'familyName',
    'upm',
    'designer',
    'designerURL',
    'copyright',
    'manufacturer',
    'manufacturerURL',
    'versionMajor',
    'versionMinor',
    'date',
]

LICENSE = '%s%s%s' % (
    'This Font Software is licensed under the SIL Open Font License, ',
    'Version 1.1. This license is available with a FAQ at: ',
    'http://scripts.sil.org/OFL'
)

LICENSE_URL = 'http://scripts.sil.org/OFL'


def font_family_url(family_name):
    '''Create the url to download a font family'''
    family_name = family_name.replace(' ', '%20')
    return '%s%s' % (API_URL_PREFIX, family_name)


def url_200_response(family_name):
    """Return a zipfile containing a font family hosted on fonts.google.com"""
    family_url = font_family_url(family_name)
    request = urlopen(family_url)
    if request.getcode() == 200:
        return request
    else:
        return False


def fonts_from_zip(zipfile):
    '''return a dict of fontTools TTFonts'''
    ttfs = []
    for file_name in zipfile.namelist():
        if 'ttf' in file_name:
            ttfs.append(TTFont(zipfile.open(file_name)))
    return ttfs


def normalize_ttf_metric_vals(upm, fonts, target_upm):
    """Convert a ttf's vertical metrics values to the equivilant values
    for the target_upm.

    e.g if font_upm=2048, asc=2100 & target upm1000:
            upm=1000, asc=1025
    """
    metrics = {}
    for font in fonts:
        metrics[font] = {}
        for vert_key in fonts[font]:
            metrics[font][vert_key] = int((float(fonts[font][vert_key]) / upm) * DFLT_UPM)
    return metrics


def is_italic(font):
    for master in font.masters:
        if 'Italic' in master.name:
            return True
    return False


def fonts_attrib(fonts, attrib):
    attribs = []
    for font in fonts:
        attribs.append(getattr(font, attrib))
    return attribs


def font_masters_attrib(fonts, key):
    attribs = []
    for font in fonts:
        for master in font.masters:
            attribs.append(master.customParameters[key])
    return attribs


def flatten(a, op='>'):
    val = None
    for i in a:
        if op == '>' and i > val:
            val = i
    return val


def ttfs_2_glyph(ttfs):
    """Convert ttfs into in memory .glyph file"""
    font = GSFont()
    versions = [f['head'].fontRevision for f in ttfs]
    version = flatten(versions, '>')
    font.versionMajor, font.versionMinor = map(int, str(version).split('.'))

    for ttf in ttfs:
        instance = GSInstance()
        instance.name = str(ttf['name'].getName(2, 1, 0, 0))

        instance.customParameters['winAscent'] = ttf['OS/2'].usWinAscent
        instance.customParameters['winDescent'] = ttf['OS/2'].usWinDescent
        instance.customParameters['typoAscender'] = ttf['OS/2'].sTypoAscender
        instance.customParameters['typoDescender'] = ttf['OS/2'].sTypoDescender
        instance.customParameters['typoLineGap'] = ttf['OS/2'].sTypoLineGap
        # hhea table
        instance.customParameters['hheaAscender'] = ttf['hhea'].ascent
        instance.customParameters['hheaDescender'] = ttf['hhea'].descent
        instance.customParameters['hheaLineGap'] = ttf['hhea'].lineGap

        font.instances.append(instance)
    return font


def is_same(a):
    if len(set(a)) == 1:
        return True
    return False


def main(fonts):
    # Check font already exists
    logger.header1("Checking availability on fonts.google.com")
    remote_fonts = url_200_response(fonts[0].familyName)
    if remote_fonts:
        logger.info('%s is on fonts.google.com' % fonts[0].familyName)
    else:
        logger.info('%s is not on fonts.google.com.' % fonts[0].familyName)

    logger.header1("Checking glyphs files consistency")
    if len(fonts) >= 2:

        logger.test("Attributes are consistent across glyphs files")
        for attrib in FONT_ATTRIBS:
            fonts_attrib_values = fonts_attrib(fonts, attrib)
            consistent(attrib, fonts_attrib_values)

        if not remote_fonts:
            logger.test("Vertical metrics are consistent")
            for key in VERT_KEYS:
                fonts_masters_vert_values = font_masters_attrib(fonts, key)
                consistent(key, fonts_masters_vert_values)
    else:
        logger.info("1 glyphs file only, skipping consistency")

    logger.header1("Performing regression tests")
    if remote_fonts:
        family_zip = ZipFile(StringIO(remote_fonts.read()))
        ttfs = fonts_from_zip(family_zip)
        remote_glyphs = ttfs_2_glyph(ttfs)

        logger.test('Version number has increased since previous release')
        remote_v_number = float('%s.%s' % (
            remote_glyphs.versionMajor,
            str(remote_glyphs.versionMinor).zfill(3)
        ))
        local_v_number = float('%s.%s' % (
            fonts[0].versionMajor,
            str(fonts[0].versionMinor).zfill(3)
        ))
        compare('Local Version', local_v_number, '>=',
                'Remote Version', remote_v_number)

        logger.test('Family contains same styles as hosted version')
        remote_styles = set([i.name for i in remote_glyphs.instances])
        local_styles = set([i.name for i in fonts[0].instances])
        leftover('Remote version styles', remote_styles,
                 'Local version styles', local_styles)

        logger.test('Vertical metrics visually match hosted version')
        remote_vmetrics = [m.customParameters for m
                           in remote_glyphs.instances]
        local_vmetrics = [m.customParameters for m
                          in fonts[0].masters]
        if is_same([i.values() for i in remote_vmetrics]) and \
           is_same([i.values() for i in local_vmetrics]):
            logger.info('Remote metrics are family consistent')
            logger.info('Local metrics are family consistent')

            local_vmetrics = local_vmetrics[0]
            remote_vmetrics = remote_vmetrics[0]

            local_typo = (
                local_vmetrics['typoAscender'] +
                abs(local_vmetrics['typoDescender']) +
                local_vmetrics['typoLineGap']
            )
            local_hhea = (
                local_vmetrics['hheaAscender'] +
                abs(local_vmetrics['hheaDescender']) +
                local_vmetrics['hheaLineGap']
            )
            local_win = (
                local_vmetrics['winAscent'] +
                local_vmetrics['winDescent']
            )
            remote_typo = (
                remote_vmetrics['typoAscender'] +
                abs(remote_vmetrics['typoDescender']) +
                remote_vmetrics['typoLineGap']
            )
            remote_hhea = (
                remote_vmetrics['hheaAscender'] +
                abs(remote_vmetrics['hheaDescender']) +
                remote_vmetrics['hheaLineGap']
            )
            remote_win = (
                remote_vmetrics['winAscent'] +
                remote_vmetrics['winDescent']
            )

            if fonts[0].customParameters['Use Typo Metrics']:
                logger.info('%s%s' % (
                    'Local has Use_Typo_Enabled, ',
                    'comparing local typo against remote win ascent'
                    )
                )
                compare('Local Typo', local_typo, '==',
                        'Remote winAscent', remote_win)
                compare('Local hhea', local_hhea, '==',
                        'Remote hhea', remote_hhea)
            else:
                compare('Local Typo', local_typo, '==',
                        'Remote Typo', remote_win)
                compare('Local hhea', local_hhea, '==',
                        'Remote hhea', remote_hhea)
                compare('Local win', local_win, '==',
                        'Remote win', remote_win)

    logger.header1('Checking vertical metrics')

    vmetrics = [m.customParameters for m in fonts[0].masters]

    logger.test('Use Typo Metrics is enabled')
    typo_metrics = fonts[0].customParameters['Use Typo Metrics']
    enabled('Use Typo Metrics', typo_metrics)

    logger.test('Win Ascent and Win Descent are bbox')
    if is_same([i.values() for i in vmetrics]):
        ymin, ymax = shortest_tallest_glyphs(fonts[0])
        logger.info('Vert metrics are family consistent')
        win_ascent = vmetrics[0]['winAscent']
        win_descent = vmetrics[0]['winDescent']
        compare('winDescent', win_descent, '==', 'yMin', abs(ymin))
        compare('winAscent', win_ascent, '==', 'yMax', ymax)

    if not remote_fonts:
        logger.test('Vert metrics are 120-125% of upm')
        # add test

    logger.header1("Copyright string")

    copyright = fonts[0].copyright
    logger.test("Copyright attribute matches pattern")
    logger.info("String must match following format:\n%s%s" % (
        "Copyright <yyyy> The <font-name> Project Authors ",
        "(https://github.com/author/font-project-name)"
        )
    )
    copyright_pattern = r'%s%s' % (
        r"Copyright [0-9]{4} The .* Project Authors",
        r" \(https\:\/\/github.com\/.*\/.*\)"
    )
    regex_contains('Copyright', copyright_pattern, copyright)

    logger.test("Copyright attribute contains github link")
    contains("https://github.com/", copyright)

    logger.test('Copyright attribute contains "Project Authors"')
    contains("Project Authors", copyright)

    logger.header1('Family metadata constants')

    font_params = fonts[0].customParameters
    logger.test('license matches constant')
    compare('Font license', font_params['license'], '==',
            'Constant license', LICENSE)

    logger.test('licenseURL matches constant')
    compare('Font licenseURL', font_params['licenseURL'], '==',
            'Constant licenseURL', LICENSE_URL)

    print logger
    logger.clear()


if __name__ == '__main__':
    Glyphs.showMacroWindow()
    local_fonts = Glyphs.fonts
    family_names = [f.familyName for f in local_fonts]

    if len(set(family_names)) != 1:
        logger.failed('Multiple families open!')
        logger.info('Test 1 family at a time')
    else:
        main(local_fonts)
