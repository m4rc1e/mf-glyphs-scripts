#MenuTitle: Check Font
'''

Check family for GlyphsApp
~~~~~~~~~~~~~~~~~~~~~~~~~~


Check selected family passes qa.yml spec and common font errors.

Refer to README for further info.
'''
import vanilla
import os
import sys
import yaml
import re

sys.path.append('/Users/marc/Library/Application Support/Glyphs/Scripts/mf-glyphs-scripts')
import find_duplicate_glyphs
import has_outlines
import fix_uni00a0_width

from test_gf_spec import (
	check_family_name,
	check_license_string,
	check_family_fstype,
	check_vendor_id_string,
	check_family_upm,
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
		
		# Vertical Metrics
		self._heading('Vertical Metrics:')
		self._checkbox('metrics_fam_vals', "Instances/Masters have same values")
		self._checkbox('metrics_125', "Fonts pass legacy 125pc rule")
		self._checkbox("metrics_khaled", "Fonts pass Khaled's schema")
		self._checkbox("metrics_kalapi", "Fonts pass Kalapi's schema", value=False)

		# Check Glyphs
		self._heading('Glyphs:')
		self._checkbox('glyph_names', "Glyph names")
		self._checkbox('glyph_no_dups', "No duplicate glyphs")
		self._checkbox('glyph_nbspace_space', "nbspace and space are same width")
		self._checkbox('glyphs_missing_conts_or_comps', "Glyphs missing contours or components")

		# Check 
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


def check_field(key, yml, font, fix=False):
	'''Check if a font's attribute matches the yml document'''
	if 'any' in str(yml):
		print 'PASS: font %s has attribute' % key
	elif yml != font:
		print 'ERROR: font %s is not equal to yml %s' % (key, key)
	else:
		print 'PASS: font %s is equal to yml %s' % (key, key)
	if fix:
		font = yml


def font_field(font, key):
    '''Check font has key'''
	if hasattr(font, key):
		return getattr(font, key)
	if key in font.customParameters:
		return font.customParameters[key]
	return None


def main_glyphs():
	qa_spec = yaml.safe_load(open('/Users/marc/Library/Application Support/Glyphs/Scripts/mf-glyphs-scripts/QA/qa.yml', 'r'))
	ui = GlyphsUI(qa_spec)


def main(**kwargs):
	font = Glyphs.font

	qa_spec = yaml.safe_load(open('/Users/marc/Library/Application Support/Glyphs/Scripts/mf-glyphs-scripts/QA/qa.yml', 'r'))
	if 'glyph_no_dups' in kwargs and kwargs['glyph_no_dups'].get() == 1:
		find_duplicate_glyphs.find([g.name for g in font.glyphs])

	if 'check_family_name' in kwargs and kwargs['check_family_name'].get() == 1:
		check_family_name(font.familyName)

	print '***Check Meta Data***'
	for key in qa_spec:
		font_attrib = font_field(font, key)
		if font_attrib:
			check_field(key, qa_spec[key], font_attrib)
		else:
			print ('ERROR YML DOC: Attribute %s does not exist for font' % key)

	if 'glyphs_missing_conts_or_comps' in kwargs and kwargs['glyphs_missing_conts_or_comps'].get() == 1:
		has_outlines.check(font)

    if 'glyph_nbspace_space' in kwargs and kwargs['glyph_nbspace_space'].get() == 1:
        fix_uni00a0_width.check(font, font.masters)


if __name__ == '__main__':
	main_glyphs()
