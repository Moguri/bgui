from configparser import SafeConfigParser

class Theme(SafeConfigParser):
	def __init__(self, file):
		
		SafeConfigParser.__init__(self)
		
		self.path = file
		
		if file:
			self.read(file+'/theme.cfg')
		
	def supports(self, widget):
		"""Checks to see if the theme supports a given widget.
		
		:param widget: the widget to check for support
		
		"""
		
		# First we see if we have the right section
		if not self.has_section(widget.theme_section):
			return False
		
		# Then we see if we have the required options
		for opt in widget.theme_options:
			if not self.has_option(widget.theme_section, opt):
				return False
			
		# All looks good, return True
		return True
		