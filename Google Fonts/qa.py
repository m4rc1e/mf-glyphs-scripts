#MenuTitle: QA
# -*- coding: utf-8 -*-
"""
Check GF upstream repositories pass GF checklist,
https://github.com/googlefonts/gf-docs/blob/master/ProjectChecklist.md
"""
import unittest
from unittest import TestProgram
import os
import urllib
from urllib import urlopen
from fontTools.ttLib import TTFont
import csv
from StringIO import StringIO
from zipfile import ZipFile
import re
from vertmetrics import VERT_KEYS, shortest_tallest_glyphs
from datetime import datetime
import shutil
import tempfile

API_URL_PREFIX = 'https://fonts.google.com/download?family='
UPSTREAM_REPO_URLS = 'http://tinyurl.com/kd9lort'

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

SOURCES_FOLDER = 'sources'
FONTS_FOLDER = 'fonts'


STYLE_NAMES = [
    'Thin',
    'ExtraLight',
    'Light',
    'Regular',
    'Medium',
    'SemiBold',
    'Bold',
    'ExtraBold',
    'Black',
    'Thin',
    'ExtraLight',
    'Light',
    'Regular',
    'Medium',
    'SemiBold',
    'Bold',
    'ExtraBold',
    'Black',
    'Thin Italic',
    'ExtraLight Italic',
    'Light Italic',
    'Italic',
    'Medium Italic',
    'SemiBold Italic',
    'Bold Italic',
    'ExtraBold Italic',
    'Black Italic',
    'Thin Italic',
    'ExtraLight Italic',
    'Light Italic',
    'Regular Italic',
    'Medium Italic',
    'SemiBold Italic',
    'Bold Italic',
    'ExtraBold Italic',
    'Black Italic',
]


def _font_family_url(family_name):
    '''Create the url to download a font family'''
    family_name = str(family_name).replace(' ', '%20')
    url = '%s%s' % (API_URL_PREFIX, family_name)
    return url


def url_200_response(family_name):
    """Return a zipfile containing a font family hosted on fonts.google.com"""
    family_url = _font_family_url(family_name)
    request = urlopen(family_url)
    if request.getcode() == 200:
        return request
    else:
        return False


def fonts_from_zip(zipfile):
    '''return a list of fontTools.ttLib TTFont objects'''
    ttfs = []
    for file_name in zipfile.namelist():
        if 'ttf' in file_name:
            ttfs.append(TTFont(zipfile.open(file_name)))
    return ttfs


def get_repos_doc():
    """return Google Repo doc"""
    handle = urllib.urlopen(UPSTREAM_REPO_URLS)
    ss = StringIO(handle.read())
    reader = csv.DictReader(ss)
    return reader


class TestGlyphsFiles(unittest.TestCase):
    """Class loads/generates necessary files for unit tests."""
    @classmethod
    def setUpClass(cls):
        cls.fonts = Glyphs.fonts

        cls._repos_doc = None
        cls._remote_font = None
        cls._ttfs = None
        cls._temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        """Remove the temporarily generated folder and its files"""
        shutil.rmtree(cls._temp_dir)

    @property
    def remote_font(self):
        """If the family already exists on Google Fonts, download and
        parse the ttfs into a GSFont object, else return None"""
        if not self._remote_font:
            remote_fonts = url_200_response(self.fonts[0].familyName)
            if remote_fonts:
                family_zip = ZipFile(StringIO(remote_fonts.read()))
                return fonts_from_zip(family_zip)
        return None

    @property
    def repos_doc(self):
        """Return a csv DictReader object of the GF_Repo doc"""
        if not self._repos_doc:
            self._repos_doc = get_repos_doc()
        return self._repos_doc

    @property
    def ttfs(self):
        """Return the generated .ttfs from the open .glyphs files"""
        if not self._ttfs:
            for font in self.fonts:
                for instance in font.instances:
                    instance.generate(Format='ttf', FontPath=self._temp_dir)
        self._ttfs = [TTFont(os.path.join(self._temp_dir, f)) for f
                      in os.listdir(self._temp_dir) if f.endswith('.ttf')]
        return self._ttfs


class TestFontInfo(TestGlyphsFiles):

    def test_copyright(self):
        """Copyright string matches specification:

        https://github.com/googlefonts/gf-docs/blob/master/ProjectChecklist.md#ofltxt

        The string must include the git repo url.
        """
        
        repo_git_url = None
        for font in self.fonts:
            if not repo_git_url:
                for row in self.repos_doc:
                    if row['family'] == font.familyName:
                        repo_git_url = str(row['upstream'])
                        break

            family_copyright_pattern = r'Copyright [0-9]{4} The %s Project Authors \(%s\)' % (
                font.familyName, repo_git_url
            )

            copyright_search = re.search(family_copyright_pattern, font.copyright)
            self.assertIsNotNone(
                copyright_search,
                'font.copyright is incorrect. It must contain or be:\n' + \
                'Copyright %s The %s Project Authors (%s)' %(
                    datetime.now().year,
                    font.familyName,
                    repo_git_url,
                )
            )

    def test_style_names(self):
        """Instance names must be in STYLE_NAMES"""
        for font in self.fonts:
            instances = font.instances
            family_styles = set([i.name for i in instances])
            for style in family_styles:
                self.assertIn(style, STYLE_NAMES)

    def test_license_url(self):
        for font in self.fonts:
            self.assertEqual(
                font.customParameters['licenseURL'],
                LICENSE_URL,
                "font.customParameters['licenseURL'] must be '%s'" % LICENSE_URL
            )

    def test_license(self):
        for font in self.fonts:
            self.assertEqual(
                font.customParameters['license'],
                LICENSE,
                "font.customParameters['license'] must be '%s'" % LICENSE
            )


class TestMultipleGlyphsFileConsistency(unittest.TestCase):
    """Families are often split into multiple .glyphs files.

    Make sure certain attributes share the same values"""
    def setUp(self):
        self.fonts = Glyphs.fonts

    def test_files_share_same_attributes(self):
        for font1 in self.fonts:
            for font2 in self.fonts:
                for attrib in FONT_ATTRIBS:
                    self.assertEqual(
                        getattr(font1, attrib),
                        getattr(font2, attrib),
                        "%s %s %s not equal to %s %s %s" % (
                            font1,
                            attrib,
                            getattr(font1, attrib),
                            font2,
                            attrib,
                            getattr(font2, attrib)
                        )
                    )

    def test_font_customParameters_are_equal(self):
        for font1 in self.fonts:
            for font2 in self.fonts:
                for param in font1.customParameters:
                    self.assertEqual(
                        font1.customParameters[param.name],
                        font2.customParameters[param.name],
                        '%s %s %s is not equal to %s %s %s' % (
                            font1,
                            param.name,
                            font1.customParameters[param.name],
                            font2,
                            param.name,
                            font2.customParameters[param.name],
                        )
                    )


class TestRegressions(TestGlyphsFiles):
    """If the family already exists on fonts.google.com, download and compare
    the data against the generated .ttf instances from the .glyphs file."""
    def _get_font_styles(self, fonts):
        """Get the Win style name for each font"""
        styles = []
        for font in fonts:
            name = font['name'].getName(2, 3, 1, 1033)
            enc = name.getEncoding()
            styles.append(str(name).decode(enc))
        return set(styles)

    def _hash_fonts(self, ttfs):
        styles = self._get_font_styles(ttfs)
        return dict(zip(styles, ttfs))


    def test_missing_glyphs(self):
        """Family updates should include the same glyphs as the
        previous release."""
        if self.remote_font:
            local_fonts = self._hash_fonts(self.ttfs)
            remote_fonts = self._hash_fonts(self.remote_font)
            shared_styles = set(local_fonts.keys()) & set(remote_fonts.keys())

            for style in shared_styles:
                local_glyphs = set(local_fonts[style].getGlyphSet().keys())
                remote_glyphs = set(remote_fonts[style].getGlyphSet().keys())

                missing = remote_glyphs - local_glyphs
                self.assertEqual(
                    missing,
                    set([]),
                    '%s is missing [%s]' % (
                        style,
                        ', '.join(missing)
                    )
                )

    def test_missing_instances(self):
        """Family updates must include the same instances as the previous
        release."""
        if self.remote_font:
            local_styles = self._get_font_styles(self.ttfs)
            remote_styles = self._get_font_styles(self.remote_font)
            missing = remote_styles - local_styles
            self.assertEqual(missing, set([]),
                            'Font is missing instances [%s] are all .glyphs file open?' % ', '.join(missing))

    def test_version_number_has_advanced(self):
        """If the family has a version number lower than the family being
        served on fonts.google.com, it may mean the repository is based on
        older sources. Authors need to investigate if they are working from
        the correct source.

        If the version number is the same and changes have occured, the
        version number needs bumping"""
        if self.remote_font:
            local_version = max([f['head'].fontRevision for f in self.ttfs])
            remote_version = max([f['head'].fontRevision for f in self.remote_font])
            self.assertGreater(
                local_version,
                remote_version,
                "Font Version, %s is not greater than previous release, %s" % (
                        local_version, remote_version
                    )
                )

    def test_vert_metrics_visually_match(self):
        """Vertical metrics must visually match the version hosted
        on fonts.google.com.

        If the hosted family doesn't have the fsSelection bit 7 enabled,
        we can use this to our advantage. By setting this bit, the typo
        metrics are used instead of the win metrics. This allows us to
        add taller scripts, without affecting the line leading. The win
        metrics can then be set freely. This scenario is common when 
        upgrading legacy families.

        If both the hosted family and the local family have fsSelection
        bit 7 enabled, the typo and hhea values must be the same. The win
        values can be changed freely to accomodate the families bbox ymin
        and ymax values to avoid clipping."""
        if self.remote_font:
            local_fonts = self._hash_fonts(self.ttfs)
            remote_fonts = self._hash_fonts(self.remote_font)
            shared_styles = set(local_fonts.keys()) & set(remote_fonts.keys())

            for style in shared_styles:
                l_font = local_fonts[style]
                r_font = remote_fonts[style]

                # Check if Use Typo metrics bit 7 is enabled
                # https://www.microsoft.com/typography/OTSpec/os2.htm#fss
                l_use_typo_metrics = l_font['OS/2'].fsSelection & 0b10000000
                r_use_typo_metrics = r_font['OS/2'].fsSelection & 0b10000000

                l_upm = l_font['head'].unitsPerEm
                r_upm = r_font['head'].unitsPerEm

                if r_use_typo_metrics and l_use_typo_metrics:
                    self.assertEqual(
                        l_font['OS/2'].sTypoAscender, 
                        int(r_font['OS/2'].sTypoAscender / float(r_upm) * l_upm),
                        "Local %s typoAscender %s is not equal to remote %s typoAscender %s" % (
                            style,
                            l_font['OS/2'].sTypoAscender,
                            int(r_font['OS/2'].sTypoAscender / float(r_upm) * l_upm),
                        )
                    )
                    self.assertEqual(
                        l_font['OS/2'].sTypoDescender, 
                        int(r_font['OS/2'].sTypoDescender / float(r_upm) * l_upm),
                        "Local %s typoDescender %s is not equal to remote %s typoDescender %s" % (
                            style,
                            l_font['OS/2'].sTypoDescender,
                            int(r_font['OS/2'].sTypoDescender / float(r_upm) * l_upm),
                        )
                    )
                    self.assertEqual(
                        l_font['OS/2'].sTypoLineGap, 
                        int(r_font['OS/2'].sTypoLineGap / float(r_upm) * l_upm),
                        "Local %s typoLineGap %s is not equal to remote %s typoLineGap %s" % (
                            style,
                            l_font['OS/2'].sTypoLineGap,
                            int(r_font['OS/2'].sTypoLineGap / float(r_upm) * l_upm),
                        )
                    )
                elif l_use_typo_metrics and not r_use_typo_metrics:
                    self.assertEqual(
                        l_font['OS/2'].sTypoAscender,
                        int(r_font['OS/2'].usWinAscent / float(r_upm) * l_upm),
                        "Local %s typoAscender %s is not equal to remote %s winAscent %s" % (
                            style,
                            l_font['OS/2'].sTypoAscender,
                            int(r_font['OS/2'].usWinAscent / float(r_upm) * l_upm),
                        )
                    )
                    self.assertEqual(
                        l_font['OS/2'].sTypoDescender,
                        - int(r_font['OS/2'].usWinDescent / float(r_upm) * l_upm),
                        "Local %s typoDescender %s is not equal to remote %s winDescent %s" % (
                            style,
                            l_font['OS/2'].sTypoDescender,
                            - int(r_font['OS/2'].usWinDescent / float(r_upm) * l_upm),
                        )
                    )
                    self.assertEqual(
                        l_font['OS/2'].sTypoLineGap,
                        0,
                        "Local %s typoLineGap %s is not equal to 0" % (
                            style,
                        )
                    )

                self.assertEqual(
                    l_font['hhea'].ascent, 
                    int(r_font['hhea'].ascent / float(r_upm) * l_upm),
                    "Local %s hheaAscender %s is not equal to remote %s hheaAscender %s" % (
                        style,
                        l_font['hhea'].ascent, 
                        int(r_font['hhea'].ascent / float(r_upm) * l_upm),
                    )
                )
                self.assertEqual(
                    l_font['hhea'].descent, 
                    int(r_font['hhea'].descent / float(r_upm) * l_upm),
                    "Local %s hheaDescender %s is not equal to remote %s hheaDescender %s" % (
                        style,
                        l_font['hhea'].descent,
                        int(r_font['hhea'].descent / float(r_upm) * l_upm),
                    )
                )
                self.assertEqual(
                    l_font['hhea'].lineGap,
                    int(r_font['hhea'].lineGap / float(r_upm) * l_upm),
                    "Local %s hheaLineGap %s is not equal to remote %s hheaLineGap %s" % (
                        style,
                        l_font['hhea'].lineGap,
                        int(r_font['hhea'].lineGap / float(r_upm) * l_upm),
                    )
                )


class TestVerticalMetrics(TestGlyphsFiles):
    
    def test_family_has_use_typo_metrics_enabled(self):
        for font in self.fonts:
            self.assertEqual(
                font.customParameters['Use Typo Metrics'],
                True,
                "Use font.customParameters['Typo Metrics'] must be enabled"
            )

    def test_family_share_same_metric_values(self):
        if not self.remote_font:
            font_master1_params = self.fonts[0].masters[0].customParameters

            for font in self.fonts:
                for master in font.masters:
                    for param in master.customParameters:
                        if param.name in VERT_KEYS:
                            self.assertEqual(
                                font_master1_params[param.name],
                                master.customParameters[param.name],
                                '%s %s %s is not equal to %s' % (
                                    master.name,
                                    param.name,
                                    master.customParameters[param.name],
                                    font_master1_params[param.name],
                                )
                            )
        else:
            pass

    def test_win_ascent_and_win_descent_equal_bbox(self):
        """MS recommends OS/2's win Ascent and win Descent must be the ymax
        and ymin of the bbox"""
        family_ymax_ymin = []
        for font in self.fonts:
            ymin, ymax = shortest_tallest_glyphs(font)
            family_ymax_ymin.append(ymin)
            family_ymax_ymin.append(ymax)

        ymax = max(family_ymax_ymin)
        ymin = min(family_ymax_ymin)

        for font in self.fonts:
            for master in font.masters:
                win_ascent = master.customParameters['winAscent']
                win_descent = master.customParameters['winDescent']
                self.assertEqual(
                    int(win_ascent),
                    ymax,
                    "%s winAscent %s is not equal to %s" % (
                        master.name,
                        win_ascent,
                        ymax)
                )
                # ymin is abs because win descent is a positive integer
                self.assertEqual(
                    int(win_descent),
                    abs(ymin),
                    "%s winDescent %s is not equal to %s" % (
                        master.name,
                        win_descent,
                        ymin)
                )


class TestRepositoryStructure(TestGlyphsFiles):
    """Repositories must conform to the following tree:

        .
    ├── AUTHORS.txt
    ├── CONTRIBUTORS.txt
    ├── DESCRIPTION.en_us.html
    ├── FONTLOG.txt
    ├── METADATA.pb
    ├── OFL.txt
    ├── README.md
    ├── fonts
    │   └── ttf
    │       ├── Inconsolata-Bold.ttf
    │       └── Inconsolata-Regular.ttf
    └── sources
        └──  Inconsolata.glyphs

    """
    def test_repo_in_gf_upstream_repos_doc(self):
        """Check the repository has been recorded in the GF Upstream doc,
        http://tinyurl.com/kd9lort"""
        found = False
        for font in self.fonts:
            for row in self.repos_doc:
                if row['family'] == font.familyName:
                    found = True
            self.assertEqual(
                True,
                found, 
                'Family is not listed in GF Master repo doc, %s' % UPSTREAM_REPO_URLS
            )

    def test_fonts_dir_exists(self):
        abs_fonts_folder = os.path.join(project_dir, FONTS_FOLDER)
        self.assertEquals(
            True,
            os.path.isdir(abs_fonts_folder),
            "'%s' folder is missing or named incorrectly" % abs_fonts_folder
        )

    def test_sources_dir_exists(self):
        abs_sources_folder = os.path.join(project_dir, SOURCES_FOLDER)
        self.assertEquals(
            True,
            os.path.isdir(abs_sources_folder),
            "'%s' folder is missing or named incorrectly" % abs_sources_folder
        )

    def test_contributors_file_exists(self):
        self.assertIn(
            'CONTRIBUTORS.txt',
            os.listdir(project_dir),
            "'CONTRIBUTORS.txt' is missing in parent directory")

    def test_authors_file_exists(self):
        self.assertIn(
            'AUTHORS.txt', 
            os.listdir(project_dir),
            "'AUTHORS.txt' is missing in parent directory")


if __name__ == '__main__':
    Glyphs.showMacroWindow()
    __glyphsfile = Glyphs.font.filepath
    project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__glyphsfile), '..')
    )
    if len(set([f.familyName for f in Glyphs.fonts])) == 1:
        TestProgram(argv=['--verbose'], exit=False)
    else:
        print 'Test one family at a time'
