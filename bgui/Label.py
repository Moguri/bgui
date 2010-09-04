from bgl import *
import blf

from .Widget import *

class Label(Widget):
	"""Widget for displaying text"""

	def __init__(self, parent, name, text="", font=None, pt_size=30, color=(1, 1, 1, 1), pos=[0, 0], options=BGUI_DEFAULT):
		"""The Label constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		text -- the text to display (this can be changed later via the text property)
		font -- the font to use
		pt_size -- the point size of the text to draw
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""
		Widget.__init__(self, parent, name, [0,0], pos, options)

		self.fontid = blf.load(font) if font else 0
		
		self.pt_size = pt_size
		
		self.color = color

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
		