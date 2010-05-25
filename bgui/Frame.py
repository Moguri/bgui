from bgl import *
from bgui.Widget import *

class Frame(Widget):
	"""Frame for storing other widgets"""
	
	def __init__(self, parent, name, size=[1, 1], pos=[0, 0], options=BGUI_DEFAULT):
		"""
		"""
		
		Widget.__init__(self, parent, name, size, pos, options)
		
	def _draw(self):
		"""Draw the window"""
		
		colors = (
			(1, 1, 1, 1),
			(0, 0, 1, 1),
			(0, 0, 1, 1),
			(0, 0, 1, 1),
			)
			
		glBegin(GL_QUADS)
		for i in range(4):
			glColor4f(colors[i][0], colors[i][1], colors[i][2], colors[i][3])
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()
		
		Widget._draw(self)
			