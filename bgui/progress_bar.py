from bgl import *
from .widget import Widget, BGUI_DEFAULT


class ProgressBar(Widget):
	"""A solid progress bar.
	Controlled via the 'percent' property which assumes percent as a 0-1 floating point number."""
	theme_section = 'ProgressBar'
	theme_options = {
				'FillColor1': (0.0, 0.42, 0.02, 1.0),
				'FillColor2': (0.0, 0.42, 0.02, 1.0),
				'FillColor3': (0.0, 0.42, 0.02, 1.0),
				'FillColor4': (0.0, 0.42, 0.02, 1.0),
				'BGColor1': (0, 0, 0, 1),
				'BGColor2': (0, 0, 0, 1),
				'BGColor3': (0, 0, 0, 1),
				'BGColor4': (0, 0, 0, 1),
				'BorderSize': 1,
				'BorderColor': (0, 0, 0, 1),
				}

	def __init__(self, parent, name, percent=1.0, sub_theme='', aspect=None, size=[1, 1], pos=[0, 0], options=BGUI_DEFAULT):
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param percent: the initial percent
		:param sub_theme: sub type of theme to use
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the width and height
		:param pos: a tuple containing the x and y position
		:param options: various other options
		"""

		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)

		theme = self.theme

		self.fill_colors = [
				theme['FillColor1'],
				theme['FillColor2'],
				theme['FillColor3'],
				theme['FillColor4'],
				]

		self.bg_colors = [
				theme['BGColor1'],
				theme['BGColor2'],
				theme['BGColor3'],
				theme['BGColor4'],
				]

		self.border_color = theme['BorderColor']
		self.border = theme['BorderSize']

		self._percent = percent

	@property
	def percent(self):
		return self._percent

	@percent.setter
	def percent(self, value):
		self._percent = max(0.0, min(1.0, value))

	def _draw(self):
		"""Draw the progress bar"""
		# Enable alpha blending
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		# Enable polygon offset
		glEnable(GL_POLYGON_OFFSET_FILL)
		glPolygonOffset(1.0, 1.0)

		mid_x = self.gl_position[0][0] + (self.gl_position[1][0] - self.gl_position[0][0]) * self._percent

		# Draw fill
		glBegin(GL_QUADS)
		glColor4f(self.fill_colors[0][0], self.fill_colors[0][1], self.fill_colors[0][2], self.fill_colors[0][3])
		glVertex2f(self.gl_position[0][0], self.gl_position[0][1])

		glColor4f(self.fill_colors[1][0], self.fill_colors[1][1], self.fill_colors[1][2], self.fill_colors[1][3])
		glVertex2f(mid_x, self.gl_position[1][1])

		glColor4f(self.fill_colors[2][0], self.fill_colors[2][1], self.fill_colors[2][2], self.fill_colors[2][3])
		glVertex2f(mid_x, self.gl_position[2][1])

		glColor4f(self.fill_colors[3][0], self.fill_colors[3][1], self.fill_colors[3][2], self.fill_colors[3][3])
		glVertex2f(self.gl_position[3][0], self.gl_position[3][1])
		glEnd()

		# Draw bg
		glBegin(GL_QUADS)
		glColor4f(self.bg_colors[0][0], self.bg_colors[0][1], self.bg_colors[0][2], self.bg_colors[0][3])
		glVertex2f(mid_x, self.gl_position[0][1])

		glColor4f(self.bg_colors[1][0], self.bg_colors[1][1], self.bg_colors[1][2], self.bg_colors[1][3])
		glVertex2f(self.gl_position[1][0], self.gl_position[1][1])

		glColor4f(self.bg_colors[2][0], self.bg_colors[2][1], self.bg_colors[2][2], self.bg_colors[2][3])
		glVertex2f(self.gl_position[2][0], self.gl_position[2][1])

		glColor4f(self.bg_colors[3][0], self.bg_colors[3][1], self.bg_colors[3][2], self.bg_colors[3][3])
		glVertex2f(mid_x, self.gl_position[3][1])
		glEnd()

		# Draw outline
		glDisable(GL_POLYGON_OFFSET_FILL)

		r, g, b, a = self.border_color
		glColor4f(r, g, b, a)
		glPolygonMode(GL_FRONT, GL_LINE)
		glLineWidth(self.border)

		glBegin(GL_QUADS)
		for i in range(4):
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])

		glEnd()

		glPolygonMode(GL_FRONT, GL_FILL)

		Widget._draw(self)
