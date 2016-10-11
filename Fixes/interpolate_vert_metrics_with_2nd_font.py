#MenuTitle: Interpolate Current Font Master's Vert Metrics between Secondary Font Master's Vert Metrics
from os.path import basename
import vanilla
"""
Interpolate the current font master's vertical metrics values against
background font.
"""

INTERPOLATE_KEYS = [
    "typoAscender",
    "typoDescender",
    "typoLineGap",
    "winAscent",
    "winDescent",
    "hheaAscender",
    "hheaDescender",
    "hheaLineGap",
    "smallCapHeight",
    "shoulderHeight",
    "vheaVertAscender",
    "vheaVertDescender",
    "vheaVertLineGap",
    "Preview Ascender",
    "Preview Descender"
]


class GlyphsUI(object):
        '''Dialog for entering interpolation value'''
        def __init__(self):
            self.w = vanilla.FloatingWindow((330, 110), "Interpolate Master's Vert Metrics")
            self.w.textBox = vanilla.TextBox((10, 10, -10, 17), "Enter value between 1.0 > 0.0")
            self.w.interpolation_value = vanilla.TextEditor((10, 30, -10, 17))
            self.w.ignore_win_metrics = vanilla.CheckBox((10, 50, 180, 20), 'Ignore Win Metrics',value=True)
            # Check button
            self.w.button = vanilla.Button((10, 80, -10, 17), "Interpolate", callback=self.buttonCallback)

            self.w.open()

        def buttonCallback(self, sender):
            main(**self.w.__dict__)
            self.w.close()


def main(**kwargs):
    fonts = Glyphs.fonts
    Glyphs.showMacroWindow()
    INTERPOLATION_VALUE = float(kwargs['interpolation_value'].get())
    if kwargs['ignore_win_metrics'].get() == 1:
        if 'winAscent' in INTERPOLATE_KEYS:
            INTERPOLATE_KEYS.remove('winAscent')
            INTERPOLATE_KEYS.remove('winDescent')

    selected_font = fonts[0]
    previous_font = fonts[1]

    selected_layer_metrics = {i.name: i.value for i in
        selected_font.selectedFontMaster.customParameters if i.name in INTERPOLATE_KEYS}

    previous_layer_metrics = {i.name: i.value for i in
        previous_font.selectedFontMaster.customParameters if i.name in INTERPOLATE_KEYS}

    diff_keys = set(selected_layer_metrics) - set(previous_layer_metrics)

    if diff_keys:
        print 'ERROR: Keys not equal, missing %s' % ', '.join(diff_keys)
    else:
        new_metrics = {}
        for key in selected_layer_metrics:
            if key in INTERPOLATE_KEYS:
                    s_val = selected_layer_metrics[key]
                    p_val = previous_layer_metrics[key]
                    if s_val < p_val:
                        smallest = s_val
                    else:
                        smallest = p_val

                    new_metrics[key] = int(abs(s_val - p_val) * INTERPOLATION_VALUE + smallest)

        for key in new_metrics:
            selected_font.selectedFontMaster.customParameters[key] = new_metrics[key]

        print 'Metrics are now %s between %s %s and %s %s' % (
            INTERPOLATION_VALUE,
            basename(selected_font.filepath),
            selected_font.selectedFontMaster.name,
            basename(previous_font.filepath),
            previous_font.selectedFontMaster.name,
            )


if __name__ == '__main__':
    if len(Glyphs.fonts) != 2:
        print 'ERROR: please have 2 fonts open only'
    else:
        GlyphsUI()
