from bgl import *
from .Widget import *

class Frame(Widget):
	"""Frame for storing other widgets"""
	
	def __init__(self, parent, name, size=[1, 1], pos=[0, 0], options=BGUI_DEFAULT):
		"""
		"""
		
		Widget.__init__(self, parent, name, size, pos, options)
		
		self.colors = (
			(1, 1, 1, 1),
			(0, 0, 1, 1),
			(0, 0, 1, 1),
			(0, 0, 1, 1),
			)
		
	def _draw(self):
		"""Draw the window"""
		
		# Enable alpha blending
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
			
		glBegin(GL_QUADS)
		for i in range(4):
			glColor4f(self.colors[i][0], self.colors[i][1], self.colors[i][2], self.colors[i][3])
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()
		
		Widget._draw(self)
			