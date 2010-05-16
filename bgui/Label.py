from bgl import *
import blf

from bgui.Widget import *

class Label(Widget):
	"""Widget for displaying text"""

	def __init__(self, parent, name, text="", font=None, pt_size=30, pos=[0, 0], options=BGUI_DEFUALT):
		"""The ImageWidget constructor

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

		size = [None] * 2

		self.fontid = blf.load(font) if font else 0
		blf.size(self.fontid, pt_size, 72)
		size[0], size[1] = blf.dimensions(self.fontid, text)

		if options & BGUI_NORMALIZED:
			size[0] /= parent.size[0]
			size[1] /= parent.size[1]

		Widget.__init__(self, parent, name, size, pos, options)

		self.pt_size = pt_size

		self._text = text

	def get_text(self):
		return self._text
	def set_text(self, value):
		size = [None] * 2
		size[0], size[1] = blf.dimensions(self.fontid, value)

		if self.options & BGUI_NORMALIZED:
			size[0] /= self.parent.size[0]
			size[1] /= self.parent.size[1]

		self._update_position(size, self._base_pos)

		self._text = value
	def del_text(self):
		del self._x

	def _draw(self):
		"""Display the text"""

		blf.size(self.fontid, self.pt_size, 72)

		for i, txt in enumerate([i for i in self._text.split('\n')]):
			blf.position(self.fontid, self.position[0], self.position[1] - (self.size[1]*(i+1)), 0)
			blf.draw(self.fontid, txt)

	text = property(get_text, set_text, del_text, "The text to display")