#MenuTitle: Check Font
'''

Check family for GlyphsApp
~~~~~~~~~~~~~~~~~~~~~~~~~~

Check selected family passes qa.json spec and common font errors.

Refer to README for further info.
'''
import vanilla
import os
import sys
import glob
import sys
import json
import re

script_path = os.path.abspath('..')
if script_path not in sys.path:
    sys.path.append(script_path)
from QA import (
    glyphs,
    fontinfo,
    metrics,
)


__version__ = 0.1
__author__ = 'Marc Foley'


class GlyphsUI(object):
    '''Dialog for enabling/disabling checks'''
    def __init__(self, config_file):
        self.w = vanilla.FloatingWindow((330, 500), "QA Selected Font", minSize=(300,500), maxSize=(1000,700))
        self.leading = 14
        self.head_count = 0

        self._heading('Meta Data')
        # iterate over config file and add each entry
        for key in config_file:
            self._checkbox(key, '%s' % key)
        self._checkbox('check_family_name', "Check font name has ASCII chars only")
        self._checkbox('check_absolute_panose', "Check Panose is not assigned for all weights")
        
        # Vertical Metrics
        self._heading('Vertical Metrics:')
        self._checkbox('metrics_fam_vals', "Instances/Masters have same values")

        # Check Glyphs
        self._heading('Glyphs:')
        self._checkbox('glyph_no_dups', "No duplicate glyphs")
        self._checkbox('glyph_nbspace_space', "nbspace and space are same width")
        self._checkbox('glyphs_missing_conts_or_comps', "Glyphs missing contours or components")

        # Check button
        self.w.button = vanilla.Button((14, self.leading+40, 300, 20), "Check", callback=self.buttonCallback)
        # Resize window to fit all tests
        self.w.setPosSize((100.0, 100.0, 350.0, self.leading + 75))
        self.w.open()
    
    def _heading(self, title):
        self.leading += 20
        setattr(self.w, 'text%s' % self.head_count, vanilla.TextBox((14, self.leading, 300, 14), title, sizeStyle='small'))
        self.leading += 12
        self.head_count += 1
        setattr(self.w, 'rule%s' % self.head_count, vanilla.HorizontalLine((14, self.leading, 300, 14)))
        self.leading += 12
    
    def _checkbox(self, attr,  title, value=True):
        setattr(self.w, attr, vanilla.CheckBox((14, self.leading, 300, 20), title, value=value))
        self.leading += 20
        
    def buttonCallback(self, sender):
        main(**self.w.__dict__)


def main_glyphs():
    qa_spec = json.load(open(script_path + '/QA/qa.json', 'r'))
    ui = GlyphsUI(qa_spec)


def main(**kwargs):
    font = Glyphs.font

    qa_spec = json.load(open(script_path + '/QA/qa.json', 'r'))

    print '***Check Meta Data***'
    for key in qa_spec:
        font_attrib = fontinfo.font_field(font, key)
        if font_attrib:
            fontinfo.check_field(key, qa_spec[key], font_attrib)
        else:
            print ('ERROR YML DOC: Attribute %s does not exist for font\n' % key)

    if 'check_family_name' in kwargs and kwargs['check_family_name'].get() == 1:
        fontinfo.check_family_name(font.familyName)

    if 'check_absolute_panose' in kwargs and kwargs['check_absolute_panose'].get() == 1:
        fontinfo.panose(font)

    print "***Check Glyph's Data***"
    if 'glyphs_missing_conts_or_comps' in kwargs and kwargs['glyphs_missing_conts_or_comps'].get() == 1:
        glyphs.outlines_missing(font)

    if 'glyph_nbspace_space' in kwargs and kwargs['glyph_nbspace_space'].get() == 1:
        metrics.uni00a0_width(font, font.masters)

    if 'glyph_no_dups' in kwargs and kwargs['glyph_no_dups'].get() == 1:
        glyphs.find_duplicates([g.name for g in font.glyphs])

    print "***Check Vertical Metrics***"
    if 'metrics_fam_vals' in kwargs and kwargs['metrics_fam_vals'].get() == 1:
        metrics.synced('master', font.masters)
        metrics.synced('instance', font.instances)


if __name__ == '__main__':
    main_glyphs()
