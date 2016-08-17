#MenuTitle: Check Font
import vanilla
import os
import sys
import yaml
import re

sys.path.append('/Users/marc/Library/Application Support/Glyphs/Scripts/mf-glyphs-scripts')
import find_duplicate_glyphs
from test_gf_spec import check_family_name
'''

Check family for GlyphsApp
~~~~~~~~~~~~~~~~~~~~~~~~~~


Check selected family passes the following:

Meta Data:
- Check fsType is 0 (installable)
- Check vendorID is present
- Font upm is 1000
- Check license url
- Check license
- Check non ASCII characters are not in Font Name


Glyphs:
- No duplicate Glyphs
- Check names
- nbspace and space share the same width


Vertical Metrics:
- Check font passes legacy 125pc upm rule
- Check old fonts pass Khaled's schema
- Check new fonts pass Kalapi's schema
- Check each master and instance share the same Metrics


Designer Proofing:
- Generate Metrics report
- Generate GPOS report
'''

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

		# Check 
		self.w.button = vanilla.Button((14, self.leading+40, 300, 20), "Check", callback=self.buttonCallback)
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

	if 'name' in kwargs and kwargs['name'].get() == 1:
		check_family_name(font.familyName)

	print '***Check Meta Data***'
	for key in qa_spec:
		font_attrib = font_field(font, key)
		check_field(key, qa_spec[key], font_attrib)
		else:
			print ('ERROR YML DOC: Attribute %s does not exist for font' % key)


if __name__ == '__main__':
	main_glyphs()