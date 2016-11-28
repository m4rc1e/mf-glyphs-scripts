#MenuTitle: Inherit legacy vertical metrics
"""
Replace Master vertical metrics with values from fonts hosted on
fonts.google.com
"""
import vanilla
import urllib
from fontTools.ttLib import TTFont

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from glob import glob
import operator

from test_kalapi_metrics import shortest_tallest_glyphs
script_path = os.path.abspath('..')
if script_path not in sys.path:
    sys.path.append(script_path)
from wrappers import GlyphsUI

API_URL_PREFIX = 'https://fonts.google.com/download?family='

FIX = True
FIX_WIN_METRICS = True
ASSIGN_FONT_TO_ALL_METRICS = False
ASSIGN_FONT = 'Regular'

OPERATORS = {
    '>=': operator.ge,
    '==': operator.eq,
    '<=': operator.le,
    '!=': operator.ne
}

DFLT_UPM = 1000

FONT_TO_MASTER_WEIGHT = {
    # Roman
    'Thin': 'Light',
    'ExtraLight': 'Light',
    'Light': 'Light',
    'Normal': 'Regular',
    'Regular': 'Regular',
    'Medium': 'Regular',
    'DemiBold': 'SemiBold',
    'SemiBold': 'SemiBold',
    'Bold': 'Bold',
    'UltraBold': 'Bold',
    'ExtraBold': 'Bold',
    'Black': 'Bold',
    'Heavy': 'Bold',
    # Italic
    'ThinItalic': 'Light',
    'ExtraLightItalic': 'Light',
    'LightItalic': 'Light',
    'NormalItalic': 'Regular',
    'Italic': 'Regular',
    'RegularItalic': 'Regular',
    'MediumItalic': 'Regular',
    'DemiBoldItalic': 'SemiBold',
    'SemiBoldItalic': 'SemiBold',
    'BoldItalic': 'Bold',
    'UltraBoldItalic': 'Bold',
    'ExtraBoldItalic': 'Bold',
    'BlackItalic': 'Bold',
    'HeavyItalic': 'Bold',
}

FONT_STYLE_ORDER = [
    # Roman
    'Thin',
    'ExtraLight',
    'Light',
    'Normal',
    'Regular',
    'Medium',
    'SemiBold',
    'DemiBold',
    'Heavy',
    'Black',
    'ExtraBold',
    'UltraBold',
    'Bold',
    # Italic
    'ThinItalic',
    'ExtraLightItalic',
    'LightItalic',
    'NormalItalic',
    'Italic',
    'RegularItalic',
    'MediumItalic',
    'SemiBoldItalic',
    'DemiBoldItalic',
    'HeavyItalic',
    'BlackItalic',
    'ExtraBoldItalic',
    'UltraBoldItalic',
    'BoldItalic',
]


class InheritMetricsUI(GlyphsUI):
    def __init__(self, fonts, title):
        GlyphsUI.__init__(self, title)

        self.fonts = fonts

        self._heading('Fix')
        self._checkbox('fix_metrics', 'Update vertical metrics', value=False)
        self._checkbox('fix_win', 'Update Win Ascent/Descent', value=False)

        self._heading('Inherit')
        self._checkbox('assign', 'Apply font to all masters', value=False)
        self._combobox('assign_font', [f for f in self.fonts])

        # Check button
        self.w.button = vanilla.Button((14, self.leading+40, 300, 20),
                                       "Check/Fix",
                                       callback=self.buttonCallback)
        # Resize window to fit all tests
        self.w.setPosSize((100.0, 100.0, 350.0, self.leading + 75))

    def buttonCallback(self, sender):
        main(self.fonts, **self.w.__dict__)


def font_family_url(family_name):
    '''Create the url to download a font family from fonts.google.com'''
    family_name = family_name.replace(' ', '%20')
    return '%s%s' % (API_URL_PREFIX, family_name)


def compare(arg1_name, arg1_val, op, arg2_name, arg2_val, e_type='ERROR'):
    '''Compare two arguements.'''
    if OPERATORS[op](arg1_val, arg2_val):
        print('PASS: %s %s is %s to %s %s' %
              (arg1_name, arg1_val, op, arg2_name, arg2_val))
    else:
        print('%s: %s %s is not %s to %s %s' %
              (e_type, arg1_name, arg1_val, op, arg2_name, arg2_val))


def fonts_from_zip(zipfile):
    '''return a list of fontTools TTFonts'''
    ttfs = []
    for file_name in zipfile.namelist():
        if 'ttf' in file_name:
            ttfs.append(file_name)
    return {ttf: TTFont(zipfile.open(ttf)) for ttf in ttfs}


def font_style(ps_name):
    if ps_name.split('-')[-1] not in FONT_STYLE_ORDER:
        return 'Regular'
    return ps_name.split('-')[-1]


def normalize_ttf_metric_keys(fonts):
    '''Convert fontTools keys glyphsapp keys'''
    metrics = {}

    for font in fonts:
        # mac postscript name
        font_name = font_style(str(font['name'].getName(6, 1, 0, 0)))
        metrics[font_name] = {}
        # OS/2
        metrics[font_name]['typoAscender'] = font['OS/2'].sTypoAscender
        metrics[font_name]['typoDescender'] = font['OS/2'].sTypoDescender
        metrics[font_name]['typoLineGap'] = font['OS/2'].sTypoLineGap
        metrics[font_name]['hheaLineGap'] = font['hhea'].lineGap
        metrics[font_name]['winAscent'] = font['OS/2'].usWinAscent
        metrics[font_name]['winDescent'] = font['OS/2'].usWinDescent
        # hhea
        metrics[font_name]['hheaAscender'] = font['hhea'].ascent
        metrics[font_name]['hheaDescender'] = font['hhea'].descent
    return metrics


def normalize_ttf_metric_vals(upm, fonts, target_upm):
    """Convert a ttf's vertical metrics values to the equivilant values for the target_upm

    e.g if font_upm=2048, asc=2100 & target upm1000:
            upm=1000, asc=1025
    """
    metrics = {}
    for font in fonts:
        metrics[font] = {}
        for vert_key in fonts[font]:
            metrics[font][vert_key] = int((float(fonts[font][vert_key]) / upm) * DFLT_UPM)
    return metrics


def shared_styles(styles, fonts):
    return [s for s in FONT_STYLE_ORDER if s in styles and s in fonts]


def fonts_to_masters(masters, remote_metrics, shared_styles):
    '''Link fonts to specific masters'''
    metrics = {}

    for font in shared_styles:
        if font in remote_metrics:
            if FONT_TO_MASTER_WEIGHT[font] not in metrics:
                metrics[FONT_TO_MASTER_WEIGHT[font]] = font

    # Return dict for only the masters available
    return {k: metrics[k] for k in metrics if k in masters}


def main_glyphs():
    local_font = Glyphs.font
    remote_family_url = font_family_url(local_font.familyName)
    url = urlopen(remote_family_url)

    font_zipfile = ZipFile(StringIO(url.read()))
    fonts = [f for f in font_zipfile.namelist() if 'ttf' in f]

    ui = InheritMetricsUI(fonts, 'Inherit vertical metrics from fonts.google.com')


def main(ui_fonts, **kwargs):
    local_font = Glyphs.font
    ymin, ymax = shortest_tallest_glyphs(local_font)
    remote_family_url = font_family_url(local_font.familyName)
    url = urlopen(remote_family_url)
    font_zipfile = ZipFile(StringIO(url.read()))

    remote_fonts = fonts_from_zip(font_zipfile)
    remote_upm = set(f['head'].unitsPerEm for f in remote_fonts.values())
    remote_upm = list(remote_upm)

    if len(remote_upm) == 1:
        remote_metrics = normalize_ttf_metric_keys(remote_fonts.values())
        remote_metrics = normalize_ttf_metric_vals(remote_upm[0], remote_metrics, local_font.upm)

        master_names_to_ids = {m.weight: m.id for m in local_font.masters}
        master_names = master_names_to_ids.keys()

        local_styles = [f.name.replace(' ', '') for f in local_font.instances]
        remote_styles = remote_metrics.keys()
        sharedstyles = shared_styles(local_styles, remote_styles)

        font_master_mapping = fonts_to_masters(master_names, remote_metrics, sharedstyles)

        print '***Check vertical metrics match hosted version on fonts.google.com***'
        for master_name, font_name in font_master_mapping.items():
            local_master_metrics = local_font.masters[master_names_to_ids[master_name]].customParameters
            remote_font_metrics = remote_metrics[font_name]

            print '\nMaster: %s Font: %s ' % (master_name, font_name)
            for key in remote_metrics[font_name]:
                compare('local %s' % key, local_master_metrics[key], '==',
                        'remote %s' % key, remote_font_metrics[key], e_type='ERROR')

                if kwargs['fix_metrics'].get() == 1 and \
                   local_master_metrics[key] != remote_font_metrics[key] and \
                   kwargs['assign'].get() == 0:
                    print 'FIXING: %s %s to %s' % (master_name, key, remote_font_metrics[key])
                    local_master_metrics[key] = remote_font_metrics[key]

                if kwargs['assign'].get() == 1:
                    sel_font = ui_fonts[kwargs['assign_font'].get()]
                    ps_name = remote_fonts[sel_font]['name'].getName(6, 1, 0, 0)
                    style = font_style(str(ps_name))

                if kwargs['fix_metrics'].get() == 1 and \
                   local_master_metrics[key] != remote_metrics[style][key] and \
                   kwargs['assign'].get() == 1:
                    print 'FIXING: %s %s to %s' % (master_name, key, remote_metrics[style][key])
                    local_master_metrics[key] = remote_metrics[style][key]

            if kwargs['fix_win'].get() == 1:
                print 'UPDATING: %s winAscent to %s' % (master_name, ymax)
                local_master_metrics['winAscent'] = ymax
                print 'UPDATING: %s winDescent to %s' % (master_name, ymin)
                local_master_metrics['winDescent'] = ymin
                local_font.customParameters['Use Typo Metrics'] = True

    else:
        print 'ERROR: remote fonts have multiple upms. Manual intervention needed'


if __name__ == '__main__':
    main_glyphs()
