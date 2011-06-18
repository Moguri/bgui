from bgl import *
from .widget import *

class Frame(Widget):
	"""Frame for storing other widgets"""
	theme_section = 'Frame'
	theme_options = {'Color1', 'Color2', 'Color3', 'Color4', 'BorderSize', 'BorderColor'}
	
	def __init__(self, parent, name, border=None, aspect=None, size=[1, 1], pos=[0, 0],
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
		
		theme = self.theme[self.theme_section] if self.theme else None
		
		if theme:
			self.colors = [
					theme['Color1'],
					theme['Color2'],
					theme['Color3'],
					theme['Color4']
					]
					
			self.border_color = theme['BorderColor']
		else:
			self.colors = (
				(1, 1, 1, 1),
				(0, 0, 1, 1),
				(0, 0, 1, 1),
				(0, 0, 1, 1),
				)
				
			self.border_color = (0.0, 0.0, 0.0, 1.0)
			
		if border:
			self.border = border
		elif theme:
			self.border = theme['BorderSize']
		else:
			# Default to 0
			self.border = 0
		
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
			