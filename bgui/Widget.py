from .KeyDefs import *
from collections import OrderedDict

# Widget options
BGUI_NONE = 0
BGUI_CENTERX = 1
BGUI_CENTERY = 2
BGUI_NORMALIZED = 4
BGUI_THEMED = 8

BGUI_DEFAULT = BGUI_NORMALIZED | BGUI_THEMED
BGUI_CENTERED = BGUI_CENTERX | BGUI_CENTERY

# Mouse event states
BGUI_MOUSE_NONE = 0
BGUI_MOUSE_CLICK = 1
BGUI_MOUSE_RELEASE = 2
BGUI_MOUSE_ACTIVE = 4

class Widget:
	"""The base widget class"""
	
	theme_section = 'Widget'
	theme_options = {}

	def __init__(self, parent, name, size=[0, 0], pos=[0, 0],
			options=BGUI_DEFAULT):
		"""The Widget constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""
		
		self.name = name
		self.options = options
		
		# Store the system so children can access theming data
		self.system = parent.system
		
		if self.system.theme and options & BGUI_THEMED and self.theme_section != Widget.theme_section:
			if self.system.theme.supports(self):
				self.theme = self.system.theme
			else:
				print("Theming is enabled, but the current theme does not support", self.__class__.__name__)
				self.theme = None
		else:
			self.theme = None
		
		self._active = False
		
		# The widget is visible by default
		self.visible = True
		
		# Event callbacks
		self.on_click = None
		self.on_release = None
		self.on_hover = None
		self.on_active = None

		# Setup the parent
		parent._attach_widget(self)
		self.parent = parent

		# A dictionary to store children widgets
		self.children = OrderedDict()

		# Setup the widget's position
		self.position = [None]*4
		self._update_position(size, pos)
	
	def __del__(self):
		self._cleanup()
		
	def _cleanup(self):
		"""Override this if needed"""
		for child in self.children:
			self.children[child]._cleanup()

	def _update_position(self, size, pos):
		self._base_size = size[:]
		self._base_pos = pos[:]

		if self.options & BGUI_NORMALIZED:
			pos[0] *= self.parent.size[0]
			pos[1] *= self.parent.size[1]

			size[0] *= self.parent.size[0]
			size[1] *= self.parent.size[1]

		if self.options & BGUI_CENTERX:
			pos[0] = self.parent.size[0]/2 - size[0]/2

		if self.options & BGUI_CENTERY:
			pos[1] = self.parent.size[1]/2 - size[1]/2

		x = pos[0] + self.parent.position[0]
		y = pos[1] + self.parent.position[1]
		width = size[0]
		height = size[1]
		self.size = [width, height]
		# The "friendly" position
		self.position = [x, y]
		
		# OpenGL starts at the bottom left and goes counter clockwise
		self.gl_position = [
					[x, y],
					[x+width, y],
					[x+width, y+height],
					[x, y+height]
				]

	def _handle_mouse(self, pos, event):
		"""Run any event callbacks"""
		# Don't run if we're not visible
		if not self.visible: return
		
		if event == BGUI_MOUSE_CLICK and self.on_click:
			self.on_click(self)
		elif event == BGUI_MOUSE_RELEASE and self.on_release:
			self.on_release(self)
		elif event == BGUI_MOUSE_ACTIVE and self.on_active:
			self.on_active(self)
		elif event == BGUI_MOUSE_NONE and self.on_hover:
			self.on_hover(self)
			
		self._active = True
			
		# Run any children callback methods
		for widget in [self.children[i] for i in self.children]:
			if (widget.gl_position[0][0] <= pos[0] <= widget.gl_position[1][0]) and \
				(widget.gl_position[0][1] <= pos[1] <= widget.gl_position[2][1]):
					widget._handle_mouse(pos, event)
			else:
				widget._active = False
			
	def _handle_key(self, key, is_shifted):
		"""Handle any keyboard input"""
		# Don't run if we're not visible
		if not self.visible: return
		
		# We don't actually do anything in this base class, just handle the children

		for widget in [self.children[i] for i in self.children]:
			if widget._active:
				widget._handle_key(key, is_shifted)

	def _attach_widget(self, widget):
		"""Attaches a widget to this widget"""

		if not isinstance(widget, Widget):
			raise TypeError("Expected a Widget object")

		if widget in self.children:
			raise ValueError("%s is already attached to this widget" %s (widget.name))

		self.children[widget.name] = widget
		
	def _remove_widget(self, widget):
		"""Removes the widget from this widget's children"""
		
		for child in widget.children:
			widget.children[child]._cleanup()
		
		del self.children[widget.name]

	def _draw(self):
		"""Draws the widget and the widget's children"""

		# This base class has nothing to draw, so just draw the children

		for child in self.children:
			if self.children[child].visible:
				self.children[child]._draw()