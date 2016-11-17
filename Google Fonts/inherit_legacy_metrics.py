#MenuTitle: Inherit legacy vertical metrics
"""
Replace Master vertical metrics with values from fonts hosted on
fonts.google.com
"""
import urllib
from fontTools.ttLib import TTFont

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from glob import glob
import operator

API_URL_PREFIX = 'https://fonts.google.com/download?family='
FIX = True

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
    return [TTFont(zipfile.open(ttf)) for ttf in ttfs]


def normalize_ttf_metric_keys(fonts):
    '''Convert fontTools keys glyphsapp keys'''
    metrics = {}

    for font in fonts:
        # mac postscript name
        font_name = str(font['name'].getName(6, 1, 0, 0)).split('-')[-1]
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


def _master_name(master):
    if master.italicAngle != 0.0:
        return '%sItalic' % (master.weight)
    else:
        return '%s' % master.weight


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


def main():
    local_font = Glyphs.font

    remote_family_url = font_family_url(local_font.familyName)
    url = urlopen(remote_family_url)
    font_zipfile = ZipFile(StringIO(url.read()))

    remote_fonts = fonts_from_zip(font_zipfile)
    remote_upm = set(f['head'].unitsPerEm for f in remote_fonts)
    remote_upm = list(remote_upm)

    if len(remote_upm) == 1:
        remote_metrics = normalize_ttf_metric_keys(remote_fonts)
        remote_metrics = normalize_ttf_metric_vals(remote_upm[0], remote_metrics, local_font.upm)

        master_names_to_ids = {_master_name(m): m.id for m in local_font.masters}
        master_names = master_names_to_ids.keys()

        local_styles = [f.name for f in local_font.instances]
        remote_styles = remote_metrics.keys()
        sharedstyles = shared_styles(local_styles, remote_styles)

        font_master_mapping = fonts_to_masters(master_names, remote_metrics, sharedstyles)
        print '***Check vertical metrics match hosted version on fonts.google.com***'
        for master_name, font_name in font_master_mapping.items():
            local_master_metrics = local_font.masters[master_names_to_ids[master_name]].customParameters
            remote_font_metrics = remote_metrics[font_name]

            print '\nMaster: %s Font: %s ' % (master_name, font_name)
            for key in remote_metrics[font_name]:
                if FIX:
                    local_master_metrics[key] = remote_font_metrics[key]
                compare('local %s' % key, local_master_metrics[key], '==',
                        'remote %s' % key, remote_font_metrics[key], e_type='ERROR')

    else:
        print 'ERROR: remote fonts have multiple upms. Manual intervention needed'


if __name__ == '__main__':
    main()
