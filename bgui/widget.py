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
import weakref
import time

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

class WeakMethod:
	def __init__(self, f):
		if hasattr(f, "__func__"):
			self.f = f.__func__
			self.c = weakref.ref(f.__self__)
		else:
			self.f = f
			self.c = None
		
	def __call__(self, *args):
		if self.c == None:
			self.f(*args)
		elif self.c() == None:
			return None
		else:
			self.f(*((self.c(),)+args))

class Animation:
	def __init__(self, widget, newpos, time_, callback):
		self.widget = widget
		self.prevpos = widget.position[:]
		if widget.options & BGUI_NORMALIZED:
			self.prevpos[0] /= widget.parent.size[0]
			self.prevpos[1] /= widget.parent.size[1]
		self.newpos = newpos
		self.start_time = self.last_update = time.time()
		self.time = time_
		self.callback = callback
		
	def update(self):
		if (time.time()-self.start_time)*1000 >= self.time:
			# We're done, run the callback and
			# return false to let widget know we can be removed
			if self.callback: self.callback()
			return False
		
		dt = (time.time() - self.last_update)*1000
		self.last_update = time.time()
		
		dx = ((self.newpos[0] - self.prevpos[0])/self.time)*dt
		dy = ((self.newpos[1] - self.prevpos[1])/self.time)*dt
		
		
		p = self.widget.position
		if self.widget.options & BGUI_NORMALIZED:
			p[0] /= self.widget.parent.size[0]
			p[1] /= self.widget.parent.size[1]
			
		p[0] += dx
		p[1] += dy
		
		self.widget.position = p
		
		return True

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
		:param size: a tuple containing the width and height
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options

		"""
		
		self._name = name
		self.options = options
		
		# Store the system so children can access theming data
		self.system = parent.system
		
		if sub_theme:
			self.theme_section += ':'+sub_theme

		self._generate_theme()
		
		self._hover = False
		self._frozen = False
		
		# The widget is visible by default
		self._visible = True
		
		# Event callbacks
		self._on_click = None
		self._on_release = None
		self._on_hover = None
		self._on_active = None
		self._on_mouse_enter = None
		self._on_mouse_exit = None

		# Setup the parent
		parent._attach_widget(self)
		self._parent = weakref.proxy(parent)

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
			
		# A list of running animations
		self.anims = []
	
	def __del__(self):
		# Debug print
		# print("Deleting", self.name)
		self._cleanup()
		
	def _generate_theme(self):
		if isinstance(self.theme_options, set):
			if self.system.theme:
				self.system.theme.warn_legacy(self.theme_section)
			# Legacy theming
			if self.system.theme and self.options & BGUI_THEMED and self.theme_section != Widget.theme_section:
				if self.system.theme.supports(self):
					self.theme = self.system.theme
				else:
					self.system.theme.warn_support(self.theme_section)
					self.theme = None
			elif not hasattr(self, "theme"):
				self.theme = None
		else:
			theme = self.system.theme
			theme = theme[self.theme_section] if theme.has_section(self.theme_section) else None
			
			if theme and self.options & BGUI_THEMED:
				self.theme = {}
				
				for k, v in self.theme_options.items():
					if k in theme:
						self.theme[k] = theme[k]
					else:
						self.theme[k] = v
			elif not hasattr(self, "theme"):
				self.theme = self.theme_options

	def _cleanup(self):
		"""Override this if needed"""
		for child in self.children:
			self.children[child]._cleanup()

	def _update_position(self, size=None, pos=None):
		if size is not None:
			self._base_size = size[:]
		else:
			size = self._base_size[:]
		if pos is not None:
			self._base_pos = pos[:]
		else:
			pos = self._base_pos[:]

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
		self._name = value
		
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
		self._on_click = WeakMethod(value)	
		
	@property
	def on_release(self):
		"""The widget's on_release callback"""
		return self._on_release
		
	@on_release.setter
	def on_release(self, value):
		self._on_release = WeakMethod(value)		
		
	@property
	def on_hover(self):
		"""The widget's on_hover callback"""
		return self._on_hover
		
	@on_hover.setter
	def on_hover(self, value):
		self._on_hover = WeakMethod(value)
		
	@property
	def on_mouse_enter(self):
		"""The widget's on_mouse_enter callback"""
		return self._on_mouse_enter

	@on_mouse_enter.setter
	def on_mouse_enter(self, value):
		self._on_mouse_enter = WeakMethod(value)
		
	@property
	def on_mouse_exit(self):
		"""The widget's on_mouse_exit callback"""
		return self._on_mouse_exit

	@on_mouse_exit.setter
	def on_mouse_exit(self, value):
		self._on_mouse_exit = WeakMethod(value)
		
	@property
	def on_active(self):
		"""The widget's on_active callback"""
		return self._on_active
		
	@on_active.setter
	def on_active(self, value):
		self._on_active = WeakMethod(value)
		
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
		
	def move(self, position, time, callback=None):
		"""Move a widget to a new position over a number of frames
		
		:param positon: The new position
		:param time: The time in milliseconds to take doing the move
		:param callback: An optional callback that is called when he animation is complete
		"""
		self.anims.append(Animation(self, position, time, callback))
		
	def _update_anims(self):
		self.anims[:] = [i for i in self.anims if i.update()]
		
		for widget in self.children.values():
			widget._update_anims()

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
				
		if not self._hover and self.on_mouse_enter:
			self.on_mouse_enter(self)
		self._hover = True
			
		# Run any children callback methods
		for widget in self.children.values():
			if (widget.gl_position[0][0] <= pos[0] <= widget.gl_position[1][0]) and \
				(widget.gl_position[0][1] <= pos[1] <= widget.gl_position[2][1]):
					widget._handle_mouse(pos, event)
			else:
				widget._update_hover(False)
				
	def _update_hover(self, hover=False):
		if not hover and self._hover and self.on_mouse_exit:
			self.on_mouse_exit(self)
		self._hover = hover
	
		for widget in self.children.values():
			widget._update_hover(hover)
				
	def _handle_key(self, key, is_shifted):
		"""Handle any keyboard input"""
		for widget in self.children.values():
			if self._hover:
				widget._handle_key(key, is_shifted)

	def _attach_widget(self, widget):
		"""Attaches a widget to this widget"""

		if not isinstance(widget, Widget):
			raise TypeError("Expected a Widget object")

		if widget in self.children:
			raise ValueError("%s is already attached to this widget" % (widget.name))

		self.children[widget.name] = widget
		
	def _remove_widget(self, widget):
		"""Removes the widget from this widget's children"""
		
		del self.children[widget.name]

	def _draw(self):
		"""Draws the widget and the widget's children"""

		# This base class has nothing to draw, so just draw the children

		for child in self.children:
			if self.children[child].visible:
				self.children[child]._draw()
			