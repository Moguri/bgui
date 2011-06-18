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
  
.. note::

	The Widget class should not be used directly in a gui, but should instead
	be subclassed to create other widgets.

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
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the wdith and height
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options

		"""
		
		self._name = name
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
		elif not hasattr(self, "theme"):
			self.theme = None
		
		self._hover = False
		self._frozen = False
		
		# The widget is visible by default
		self._visible = True
		
		# Event callbacks
		self._on_click = None
		self._on_release = None
		self._on_hover = None
		self._on_active = None

		# Setup the parent
		parent._attach_widget(self)
		self._parent = parent

		# A dictionary to store children widgets
		self._children = OrderedDict()

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

		if self.parent != self:
			x = pos[0] + self.parent.position[0]
			y = pos[1] + self.parent.position[1]
		else: # A widget should only be its own parent if it's the system...
			x = pos[0]
			y = pos[1]

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
	def name(self):
		"""The widget's name"""
		return self._name
		
	@name.setter
	def name(self, value):
		self._name = name
		
	@property
	def frozen(self):
		"""Whether or not the widget should accept events"""
		return self._frozen
	
	@frozen.setter
	def frozen(self, value):
		self._frozen = value
		
	@property
	def visible(self):
		"""Whether or not the widget is visible"""
		return self._visible
		
	@visible.setter
	def visible(self, value):
		self._visible = value
		
	@property
	def on_click(self):
		"""The widget's on_click callback"""
		return self._on_click
		
	@on_click.setter
	def on_click(self, value):
		self._on_click = value	
		
	@property
	def on_release(self):
		"""The widget's on_release callback"""
		return self._on_release
		
	@on_release.setter
	def on_release(self, value):
		self._on_release = value		
		
	@property
	def on_hover(self):
		"""The widget's on_hover callback"""
		return self._on_hover
		
	@on_hover.setter
	def on_hover(self, value):
		self._on_hover = value	
		
	@property
	def on_active(self):
		"""The widget's on_active callback"""
		return self._on_active
		
	@on_active.setter
	def on_active(self, value):
		self._on_active = value
		
	@property
	def parent(self):
		"""The widget's parent"""
		return self._parent
		
	@parent.setter
	def parent(self, value):
		self._parent = value
		self._update_position(self._base_size, self._base_value)
		
	@property
	def children(self):
		"""The widget's children"""
		return self._children
				
	@property
	def position(self):
		"""The widget's position"""
		return self._position
		
	@position.setter
	def position(self, value):
		self._update_position(self._base_size, value)
		
	@property
	def size(self):
		"""The widget's size"""
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
			