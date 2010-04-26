from bgl import *
import blf

from bgui.Widget import *

class LabelWidget(Widget):
	"""Widget for displaying text"""

	def __init__(self, parent, name, text="", font=None,pt_size = 30, size=[0, 0], pos=[0, 0], options=BGUI_DEFUALT):
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

		Widget.__init__(self, parent, name, size, pos, options)

		self.fontid = blf.load(font) if font else 0

		self.pt_size = pt_size

		self.text = text

	def _draw(self):
		"""Display the text"""

		blf.size(self.fontid, self.pt_size, 72)
		blf.position(self.fontid, self.position[0], self.position[1] -self.pt_size, 0)
		blf.draw(self.fontid, self.text)