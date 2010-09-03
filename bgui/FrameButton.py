from bgl import *

from .Widget import *
from .Frame import *
from .Label import *

class FrameButton(Widget):
	
	"""A clickable frame-based button."""
	
	def __init__(self, parent, name, base_color=(.4,.4,.4,1), text="", font=None, pt_size=30, size=[1,1], pos=[0,0], options=BGUI_DEFAULT):
		"""The Button constructor.
		
		Arguments:
		
		parent -- the widget's parent
		name -- the name of the widget
		base_color -- the color of the button
		text -- the text to display (this can be changed later via the text property)
		font -- the font to use
		pt_size -- the point size of the text to draw
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options
		
		"""
		
		Widget.__init__(self, parent, name, size, pos, options)
		
		self.frame = Frame(self, name + '_frame', size=[1,1], pos=[0,0])
		self.label = Label(self, name + '_label', text, font, pt_size, pos=[0,0], options=BGUI_NORMALIZED | BGUI_CENTERED)
		
		self.base_color = base_color
		self.light = self.color = [
			self.base_color[0] + 0.15,
			self.base_color[1] + 0.15,
			self.base_color[2] + 0.15,
			self.base_color[3]]
		self.dark = self.color = [
			self.base_color[0] - 0.15,
			self.base_color[1] - 0.15,
			self.base_color[2] - 0.15,
			self.base_color[3]]
		self.frame.colors = [self.dark, self.dark, self.light, self.light]
		
	def _handle_mouse(self, pos, event):
		"""Extend function's behaviour by altering the frame's color based
		on the event
		"""
		
		light = self.light[:]
		dark = self.dark[:]
		
		# Lighten button when hovered over.
		if event == BGUI_MOUSE_NONE:
			for n in range(3):
				light[n] += .1
				dark[n] += .1
			self.frame.colors = [dark, dark, light, light]
			
		# Darken button when clicked.
		elif event == BGUI_MOUSE_ACTIVE:
			for n in range(3):
				light[n] -= .1
				dark[n] -= .1
			self.frame.colors = [light, light, dark, dark]
			
		Widget._handle_mouse(self, pos, event)
		
	def _draw(self):
		"""Draw the button"""
		
		# Draw the children before drawing an additional outline
		Widget._draw(self)
		
		# Draw a black outline
		glBegin(GL_LINE_LOOP)
		glColor4f(0,0,0,1)
		for i in range(4):
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()
		
		# Reset the button's color
		self.frame.colors = [self.dark, self.dark, self.light, self.light]