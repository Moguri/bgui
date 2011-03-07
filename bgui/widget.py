"""

This module defines the following constants:

*Widget options*
  * BGUI_NONE = 0
  * BGUI_CENTERX = 1
  * BGUI_CENTERY = 2
  * BGUI_NORMALIZED = 4
  * BGUI_THEMED = 8
  * BGUI_NO_FOCUS = 16
  * BGUI_CACHE = 32

  * BGUI_DEFAULT = BGUI_NORMALIZED | BGUI_THEMED
  * BGUI_CENTERED = BGUI_CENTERX | BGUI_CENTERY

*Widget overflow*
  * BGUI_OVERFLOW_NONE = 0
  * BGUI_OVERFLOW_HIDDEN = 1
  * BGUI_OVERFLOW_REPLACE = 2
  * BGUI_OVERFLOW_CALLBACK = 3

*Mouse event states*
  * BGUI_MOUSE_NONE = 0
  * BGUI_MOUSE_CLICK = 1
  * BGUI_MOUSE_RELEASE = 2
  * BGUI_MOUSE_ACTIVE = 4
"""

from .key_defs import *
from collections import OrderedDict

# Widget options
BGUI_NONE = 0
BGUI_CENTERX = 1
BGUI_CENTERY = 2
BGUI_NORMALIZED = 4
BGUI_THEMED = 8
BGUI_NO_FOCUS = 16
BGUI_CACHE = 32

BGUI_DEFAULT = BGUI_NORMALIZED | BGUI_THEMED
BGUI_CENTERED = BGUI_CENTERX | BGUI_CENTERY

# Widget overflow
BGUI_OVERFLOW_NONE = 0
BGUI_OVERFLOW_HIDDEN = 1
BGUI_OVERFLOW_REPLACE = 2
BGUI_OVERFLOW_CALLBACK = 3

# Mouse event states
BGUI_MOUSE_NONE = 0
BGUI_MOUSE_CLICK = 1
BGUI_MOUSE_RELEASE = 2
BGUI_MOUSE_ACTIVE = 4

class Widget:
	"""The base widget class"""
	
	theme_section = 'Widget'
	theme_options = {}

	def __init__(self, parent, name, aspect=None, size=[0, 0], pos=[0, 0], sub_theme='',
			options=BGUI_DEFAULT):
		"""The Widget constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		aspect -- constrain the widget size to a specified aspect ratio
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""
		
		self.name = name
		self.options = options
		
		# Store the system so children can access theming data
		self.system = parent.system
		
		if self.system.theme and options & BGUI_THEMED and self.theme_section != Widget.theme_section:
			if sub_theme:
				self.theme_section += ':'+sub_theme
		
			if self.system.theme.supports(self):
				self.theme = self.system.theme
			else:
				print("Theming is enabled, but the current theme does not support", self.theme_section)
				self.theme = None
		else:
			self.theme = None
		
		self._hover = False
		self.frozen = False
		
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
		self._position = [None]*4
		self._update_position(size, pos)	
		
		if aspect:
			size = [self.size[1]*aspect, self.size[1]]
			if self.options & BGUI_NORMALIZED:
				size = [size[0]/self.parent.size[0], size[1]/self.parent.size[1]]
			self._update_position(size, self._base_pos)
	
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
		self._size = [width, height]
		# The "private" position returned by setter
		self._position = [x, y]
		
		# OpenGL starts at the bottom left and goes counter clockwise
		self.gl_position = [
					[x, y],
					[x+width, y],
					[x+width, y+height],
					[x, y+height]
				]
				
		# Update any children
		for widget in self.children.values():
			widget._update_position(widget._base_size, widget._base_pos)
				
	@property
	def position(self):
		"""The text to display"""
		return self._position
		
	@position.setter
	def position(self, value):
		self._update_position(self._base_size, value)
		
	@property
	def size(self):
		"""The text to display"""
		return self._size
		
	@size.setter
	def size(self, value):
		self._update_position(value, self._base_pos)

	def _handle_mouse(self, pos, event):
		"""Run any event callbacks"""
		# Don't run if we're not visible or frozen
		if not self.visible or self.frozen: return
		
		if self.on_hover:
			self.on_hover(self)
		
		if event == BGUI_MOUSE_CLICK and self.on_click:
			self.on_click(self)
		elif event == BGUI_MOUSE_RELEASE and self.on_release:
			self.on_release(self)
		elif event == BGUI_MOUSE_ACTIVE and self.on_active:
			self.on_active(self)
			
		# Update focus
		if event == BGUI_MOUSE_CLICK and not self.system.lock_focus and not self.options & BGUI_NO_FOCUS:
			self.system.focused_widget = self
				
		self._hover = True
			
		# Run any children callback methods
		for widget in [self.children[i] for i in self.children]:
			if (widget.gl_position[0][0] <= pos[0] <= widget.gl_position[1][0]) and \
				(widget.gl_position[0][1] <= pos[1] <= widget.gl_position[2][1]):
					widget._handle_mouse(pos, event)
			else:
				widget._hover = False
				
	def _handle_key(self, key, is_shifted):
		"""Handle any keyboard input"""
		pass

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

		widget._cleanup()
		
		del self.children[widget.name]

	def _draw(self):
		"""Draws the widget and the widget's children"""

		# This base class has nothing to draw, so just draw the children

		for child in self.children:
			if self.children[child].visible:
				self.children[child]._draw()
			