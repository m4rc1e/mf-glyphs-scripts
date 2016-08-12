import vanilla

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


class UI(object):
	'''Dialog for enabling/disabling checks'''
	def __init__(self):
		self.w = vanilla.FloatingWindow((330, 500), "QA Selected Font", minSize=(300,500), maxSize=(1000,700))
		
		# Check Meta data
		self.w.text_1 = vanilla.TextBox((15-1, 12+2, 75, 14), "Meta Data:", sizeStyle='small')
		self.w.rule1 = vanilla.HorizontalLine((15-1, 26, 300, 14))
		self.w.fstype = vanilla.CheckBox((15-1, 38, 300, 20), 'Check fsType = 0 (installable)', value=True)
		self.w.vendor_id = vanilla.CheckBox((15-1, 58, 300, 20), 'Check vendorID exists', value=True)
		self.w.license = vanilla.CheckBox((15-1, 78, 300, 20), 'Check license is correct', value=True)
		self.w.license_url = vanilla.CheckBox((15-1, 98, 300, 20), 'Check license url is correct', value=True)
		self.w.name = vanilla.CheckBox((15-1, 118, 300, 20), 'Check font name has only ASCII chars', value=True)
		self.w.upm = vanilla.CheckBox((15-1, 138, 300, 20), 'Check font upm is 1000', value=True)

		# Check Vertical Metrics
		self.w.text_2 = vanilla.TextBox((15-1, 188, 300, 14), "Vertical Metrics:", sizeStyle='small')
		self.w.rule2 = vanilla.HorizontalLine((15-1, 202, 300, 14))
		self.w.metrics_fam_vals = vanilla.CheckBox((15-1, 214, 300, 20), "Check instances/masters have same values", value=True)
		self.w.metrics_125 = vanilla.CheckBox((15-1, 234, 300, 20), 'Check fonts pass 125% rule', value=True)
		self.w.metrics_khaled = vanilla.CheckBox((15-1, 254, 300, 20), "Check fonts pass Khaled's schema", value=True)
		self.w.metrics_kalapi = vanilla.CheckBox((15-1, 274, 300, 20), "Check fonts pass Kalapi's schema", value=False)

		# Check Glyphs
		self.w.text_3 = vanilla.TextBox((15-1, 324, 300, 14), "Glyphs:", sizeStyle='small')
		self.w.rule3 = vanilla.HorizontalLine((15-1, 338, 300, 14))
		self.w.glyph_names = vanilla.CheckBox((15-1, 350, 300, 20), "Check glyph names", value=True)
		self.w.glyph_no_dups = vanilla.CheckBox((15-1, 370, 300, 20), "Check no duplicate glyphs", value=True)
		self.w.glyph_nbspace_space = vanilla.CheckBox((15-1, 390, 300, 20), "Check nbspace and space are same width", value=True)
		self.w.button = vanilla.Button((15-1, 450, 300, 20), "Press me", callback=self.buttonCallback)
		self.w.open()
		
	def buttonCallback(self, sender):
		print "You pressed the button!"	
		



def main():
	ui = UI()
	ui.w.open()
# 	print ui.w.metrics_kalapi.get()


if __name__ == '__main__':
	main()
