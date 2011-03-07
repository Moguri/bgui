from bgl import *
import blf

from .widget import *

class Label(Widget):
	"""Widget for displaying text"""
	theme_section = 'Label'
	theme_options = {'Font', 'Color'}

	def __init__(self, parent, name, text="", font=None, pt_size=30, color=None,
				pos=[0, 0], sub_theme='', options=BGUI_DEFAULT):
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param text: the text to display (this can be changed later via the text property)
		:param font: the font to use
		:param pt_size: the point size of the text to draw
		:param color: the color to use when rendering the font
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options

		"""
		Widget.__init__(self, parent, name, None, [0,0], pos, sub_theme, options)

		if font:
			self.fontid = blf.load(font)
		elif self.theme:
			self.fontid = blf.load(self.theme.get(self.theme_section, 'Font'))
		else:
			self.fontid = 0
		
		# Normalize the pt size (1000px height = 1)
		if self.system.normalize_text:
			self.pt_size = int(pt_size * (self.system.size[1]/1000))
		else:
			self.pt_size = pt_size
		
		if color:
			self.color = color
		elif self.theme:
			# self.color = (1, 1, 1, 1)
			# self.color = list(self.theme.get(Label.theme_section, 'Color'))
			self.color = [float(i) for i in self.theme.get(self.theme_section, 'Color').split(',')]
		else:
			# default to white
			self.color = (1, 1, 1, 1)

		self.text = text

	@property
	def text(self):
		"""The text to display"""
		return self._text
		
	@text.setter
	def text(self, value):
		blf.size(self.fontid, self.pt_size, 72)
		size = list(blf.dimensions(self.fontid, value))
		
		if self.options & BGUI_NORMALIZED:
			size[0] /= self.parent.size[0]
			size[1] /= self.parent.size[1]

		self._update_position(size, self._base_pos)

		self._text = value

	def _draw(self):
		"""Display the text"""

		blf.size(self.fontid, self.pt_size, 72)
		
		glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])

		for i, txt in enumerate([i for i in self._text.split('\n')]):
			blf.position(self.fontid, self.position[0], self.position[1] - (self.size[1]*i), 0)
			blf.draw(self.fontid, txt.replace('\t', '    '))
			
		Widget._draw(self)
		