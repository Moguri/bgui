from bgl import *

from .Widget import *
from .Frame import *
from .Label import *

class FrameButton(Widget):
	"""A clickable frame-based button."""
	theme_section = 'FrameButton'
	theme_options = {'Color', 'BorderSize', 'BorderColor'}
	
	def __init__(self, parent, name, base_color=(.4,.4,.4,1), text="", font=None,
					pt_size=30, aspect=None, size=[1,1], pos=[0,0], sub_theme='', options=BGUI_DEFAULT):
		"""The Button constructor.
		
		Arguments:
		
		parent -- the widget's parent
		name -- the name of the widget
		base_color -- the color of the button
		text -- the text to display (this can be changed later via the text property)
		font -- the font to use
		pt_size -- the point size of the text to draw
		aspect -- constrain the widget size to a specified aspect ratio
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options
		
		"""
		
		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)
		
		self.frame = Frame(self, name + '_frame', size=[1,1], pos=[0,0], options=BGUI_DEFAULT & ~BGUI_THEMED)
		self.label = Label(self, name + '_label', text, font, pt_size, pos=[0,0], options=BGUI_DEFAULT | BGUI_CENTERED)
		
		if self.theme:
			self.base_color = [float(i) for i in self.theme.get(self.theme_section, 'Color').split(',')]
			self.frame.border = float(self.theme.get(self.theme_section, 'BorderSize'))
			self.frame.border_color = [float(i) for i in self.theme.get(self.theme_section, 'BorderColor').split(',')]
		else:
			self.base_color = base_color
			self.frame.border = 1
			self.frame.border_color = (0,0,0,1)
			
		self.light = [
			self.base_color[0] + 0.15,
			self.base_color[1] + 0.15,
			self.base_color[2] + 0.15,
			self.base_color[3]]
		self.dark = [
			self.base_color[0] - 0.15,
			self.base_color[1] - 0.15,
			self.base_color[2] - 0.15,
			self.base_color[3]]
		self.frame.colors = [self.dark, self.dark, self.light, self.light]
		
	@property
	def text(self):
		return self.label.text
	
	@text.setter
	def text(self, value):
		self.label.text = value
		
	@property
	def color(self):
		return self.base_color
		
	@color.setter
	def color(self, value):
		self.base_color = value
		self.light = [
			self.base_color[0] + 0.15,
			self.base_color[1] + 0.15,
			self.base_color[2] + 0.15,
			self.base_color[3]]
		self.dark = [
			self.base_color[0] - 0.15,
			self.base_color[1] - 0.15,
			self.base_color[2] - 0.15,
			self.base_color[3]]
		self.frame.colors = [self.dark, self.dark, self.light, self.light]
		
		
	def _handle_mouse(self, pos, event):
		"""Extend function's behaviour by altering the frame's color based
		on the event
		"""
		if self.frozen:
			return
		
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
		
		# Reset the button's color
		self.frame.colors = [self.dark, self.dark, self.light, self.light]
