from bgl import *
import blf

from .widget import *

class Label(Widget):
	"""Widget for displaying text"""
	theme_section = 'Label'
	theme_options = {'Font': '',
					 'Color': (1, 1, 1, 1),
					 'Size': 30
				}

	def __init__(self, parent, name, text="", font=None, pt_size=None, color=None,
				pos=[0, 0], sub_theme='', options=BGUI_DEFAULT):
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param text: the text to display (this can be changed later via the text property)
		:param font: the font to use
		:param pt_size: the point size of the text to draw (defaults to 30 if None)
		:param color: the color to use when rendering the font
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options

		"""
		Widget.__init__(self, parent, name, None, [0,0], pos, sub_theme, options)
		
		if font:
			self.fontid = blf.load(font)
		else:
			font = self.theme['Font']
			self.fontid = blf.load(font) if font else 0

		if pt_size:
			self.pt_size = pt_size
		else:
			self.pt_size = self.theme['Size']
		
		if color:
			self.color = color
		else:
			self.color = self.theme['Color']

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
		
	@property
	def pt_size(self):
		"""The point size of the label's font"""
		return self._pt_size
	
	@pt_size.setter
	def pt_size(self, value):
		# Normalize the pt size (1000px height = 1)
		if self.system.normalize_text:
			self._pt_size = int(value * (self.system.size[1]/1000))
		else:
			self._pt_size = value

	def _draw(self):
		"""Display the text"""

		blf.size(self.fontid, self.pt_size, 72)
		
		glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])

		for i, txt in enumerate([i for i in self._text.split('\n')]):
			blf.position(self.fontid, self.position[0], self.position[1] - (self.size[1]*i), 0)
			blf.draw(self.fontid, txt.replace('\t', '    '))
			
		Widget._draw(self)
		