#MenuTitle: QA
from os.path import basename
from urllib import urlopen
from utils import logger
from fontTools.ttLib import TTFont

from StringIO import StringIO
from zipfile import ZipFile
import re
from vertmetrics import VERT_KEYS, shortest_tallest_glyphs, VERT_TYPO_KEYS
from testfuncs import (
    compare,
    consistent,
    leftover,
    enabled,
    contains,
    regex_contains,
    exists,
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

WEIGHT_MAP = {
    'Light': 300,
    'Regular': 400,
    'Medium': 500,
    'Bold': 700,
}

LICENSE = '%s%s%s' % (
    'This Font Software is licensed under the SIL Open Font License, ',
    'Version 1.1. This license is available with a FAQ at: ',
    'http://scripts.sil.org/OFL'
)

LICENSE_URL = 'http://scripts.sil.org/OFL'

SOURCES_FOLDER = 'sources'
FONTS_FOLDER = 'fonts'


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


class TTF2Glyph(object):
    """Convert ttfs into in memory .glyph file.

    This shouldn't be a class but comparing the same object types is
    far easier."""
    def __init__(self, ttfs, weights):
        self.ttfs = ttfs
        self.weights = weights
        versions = [f['head'].fontRevision for f in ttfs]
        self.version = flatten(versions, '>')
        self.versionMajor, self.versionMinor = (
            map(int, str(self.version).split('.'))
        )
        self.customParameters = {}
        self.instances = []
        self.masters = []
        self.glyphs = {}

        if 192 in [int(f['OS/2'].fsSelection) for f in ttfs]:
            self.customParameters['Use Typo Metrics'] = True
        else:
            self.customParameters['Use Typo Metrics'] = False

        for ttf in self.ttfs:
            for glyph in ttf['glyf'].keys():
                nice_glyph_name = Glyphs.niceGlyphName(glyph)
                # no point attempting to convert TT to PS
                self.glyphs[nice_glyph_name] = None

            instance = GSInstance()
            instance.name = str(ttf['name'].getName(2, 1, 0, 0))
            self.instances.append(instance)

            # Create Masters
            try:
                if WEIGHT_MAP[instance.name] in self.weights:
                    master = GSFontMaster()
                    master.weightValue = ttf['OS/2'].usWeightClass
                    master.customParameters['winAscent'] = ttf['OS/2'].usWinAscent
                    master.customParameters['winDescent'] = ttf['OS/2'].usWinDescent
                    master.customParameters['typoAscender'] = ttf['OS/2'].sTypoAscender
                    master.customParameters['typoDescender'] = ttf['OS/2'].sTypoDescender
                    master.customParameters['typoLineGap'] = ttf['OS/2'].sTypoLineGap
                    # hhea table
                    master.customParameters['hheaAscender'] = ttf['hhea'].ascent
                    master.customParameters['hheaDescender'] = ttf['hhea'].descent
                    master.customParameters['hheaLineGap'] = ttf['hhea'].lineGap
                    self.masters.append(master)
            except KeyError:
                all


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

        logger.test('Glyph set consistency')
        for font1 in fonts:
            for font2 in fonts:
                if font1 != font2:
                    font1_glyphset = set(font1.glyphs.keys())
                    font2_glyphset = set(font2.glyphs.keys())
                    leftover(basename(font1.filepath), font1_glyphset,
                             basename(font2.filepath), font2_glyphset)

        if not remote_fonts:
            logger.test("Vertical metrics are consistent")
            for key in VERT_KEYS:
                fonts_masters_vert_values = font_masters_attrib(fonts, key)
                consistent(key, fonts_masters_vert_values)
    else:
        logger.info("1 glyphs file only, skipping consistency")

    if remote_fonts:
        logger.header1("Performing regression tests")
        family_zip = ZipFile(StringIO(remote_fonts.read()))
        ttfs = fonts_from_zip(family_zip)

        remote_glyphs = TTF2Glyph(ttfs, [400, 600, 700]) # fix

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

        local_vmetrics = [m.customParameters for m in fonts[0].masters]
        remote_vmetrics = [m.customParameters for m in remote_glyphs.masters]

        local_vmetrics_same = is_same([i.values() for i in local_vmetrics])
        remote_vmetrics_same = is_same([i.values() for i in remote_vmetrics])
        if remote_vmetrics_same:
            logger.info('Remote metrics are family consistent')
            remote_vmetrics = [remote_vmetrics[0] for i in
                               range(len(local_vmetrics))]
        if local_vmetrics_same:
            logger.info('Local metrics are family consistent')
            local_vmetrics = [local_vmetrics[0] for i in
                              range(len(local_vmetrics))]

        if remote_vmetrics_same and local_vmetrics_same:
            remote_vmetrics = [remote_vmetrics[0]]
            local_vmetrics = [local_vmetrics[0]]

        if fonts[0].customParameters['Use Typo Metrics'] and not \
                remote_glyphs.customParameters['Use Typo Metrics']:
            logger.info('Use Typo Metrics enabled locally')
            logger.info('Comparing local Typo against remote Win')
            for r, l in zip(remote_vmetrics, local_vmetrics):
                for l_key, r_key in VERT_TYPO_KEYS:
                    if l_key == 'typoDescender':
                        compare('Local %s' % l_key, abs(l[l_key]), '==',
                                'Remote %s' % r_key, abs(r[r_key]))
                    else:
                        compare('Local %s' % l_key, l[l_key], '==',
                                'Remote %s' % r_key, r[r_key])
                compare('Local typoLineGap', l['typoLineGap'], '==',
                        'Zero', 0)

        else:
            for l, r in zip(remote_vmetrics, local_vmetrics):
                for key in VERT_KEYS:
                    compare('Local %s' % key, l[key], '==',
                            'Remote %s' % key, r[key])

        logger.test('Missing glyphs')
        remote_glyphset = set(remote_glyphs.glyphs.keys())
        local_glyphset = set(fonts[0].glyphs.keys())
        logger.info('Old version has %s glyphs' % len(remote_glyphset))
        logger.info('New version has %s glyphs' % len(local_glyphset))
        leftover('Old version', remote_glyphset,
                 'New version', local_glyphset)

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

    logger.header1('Repository Structure')

    logger.test('Compulsory folders exist')
    abs_sources_folder = os.path.join(project_dir, SOURCES_FOLDER)
    exists('sources folder', os.path.isdir(abs_sources_folder))

    abs_fonts_folder = os.path.join(project_dir, FONTS_FOLDER)
    exists('fonts folder', os.path.isdir(abs_fonts_folder))

    logger.test('Compulsory files exist')

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
        try:
            __glyphsfile__ = Glyphs.font.filepath
            project_dir = os.path.abspath(
                os.path.join(os.path.dirname(__glyphsfile__), '..')
            )
        except NameError:
            project_dir = os.getcwd()
        main(local_fonts)
