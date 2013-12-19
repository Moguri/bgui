from .gl_utils import *
from .widget import Widget, BGUI_DEFAULT


class Frame(Widget):
	"""Frame for storing other widgets"""
	theme_section = 'Frame'
	theme_options = {
				'Color1': (0, 0, 0, 0),
				'Color2': (0, 0, 0, 0),
				'Color3': (0, 0, 0, 0),
				'Color4': (0, 0, 0, 0),
				'BorderSize': 0,
				'BorderColor': (0, 0, 0, 1),
				}

	def __init__(self, parent, name=None, border=None, aspect=None, size=[1, 1], pos=[0, 0],
				sub_theme='', options=BGUI_DEFAULT):
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param border: the size of the border around the frame (0 for no border)
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the width and height
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options

		"""

		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)

		#: The colors for the four corners of the frame.
		self.colors = [
				self.theme['Color1'],
				self.theme['Color2'],
				self.theme['Color3'],
				self.theme['Color4']
				]

		#: The color of the border around the frame.
		self.border_color = self.theme['BorderColor']
		
		#: The size of the border around the frame.
		if border is not None:
			self.border = border
		else:
			self.border = self.theme['BorderSize']

	def _draw(self):
		"""Draw the frame"""

		# Enable alpha blending
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		# Enable polygon offset
		glEnable(GL_POLYGON_OFFSET_FILL)
		glPolygonOffset(1.0, 1.0)

		glBegin(GL_QUADS)
		for i in range(4):
			glColor4f(self.colors[i][0], self.colors[i][1], self.colors[i][2], self.colors[i][3])
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()

		glDisable(GL_POLYGON_OFFSET_FILL)

		# Draw an outline
		if self.border > 0:
			# border = self.border/2
			r, g, b, a = self.border_color
			glColor4f(r, g, b, a)
			glPolygonMode(GL_FRONT, GL_LINE)
			glLineWidth(self.border)

			glBegin(GL_QUADS)
			for i in range(4):
				glVertex2f(self.gl_position[i][0], self.gl_position[i][1])

			glEnd()

			glLineWidth(1.0)
			glPolygonMode(GL_FRONT, GL_FILL)

		Widget._draw(self)
