from bgl import *
from .widget import *
from .theme import *
from collections import OrderedDict

class System:
	"""The main gui system. Add widgets to this and then call the render() method
	draw the gui.

	"""

	normalize_text = True
	
	def __init__(self, theme=None):
		"""System constructor
		theme -- the path to a theme directory
		
		"""

		# A dictionary to store 'root' widgets
		self._widgets = OrderedDict()

		# Size and positions for children to use.
		# The size will the the view port size and
		# the position will be the top left of the screen

		# Get some viewport info
		view_buf = Buffer(GL_INT, 4)
		glGetIntegerv(GL_VIEWPORT, view_buf)
		view = view_buf.list

		self.size = (view[2], view[3])
		self.position = (0, 0)
		
		self.name = "<System>"
		
		# Theming
		self.system = self
		self.theme = Theme(theme) if theme else None
		self.focused_widget = None
		self.lock_focus = False

	def _attach_widget(self, widget):
		"""Attaches a widget to the system. The widget then becomes a \"root\"
		widget. Ie, a widget who's parent is the system

		"""

		if not isinstance(widget, Widget):
			raise TypeError("Expected a Widget object")

		if widget in self._widgets:
			raise ValueError("%s is already attached to the system" %s (widget.name))

		self._widgets[widget.name] = widget

	def _remove_widget(self, widget):
		"""Removes the widget from the system"""

		for child in widget.children:
			widget.children[child]._cleanup()
		
		del self._widgets[widget.name]

	def update_mouse(self, pos, click_state=BGUI_MOUSE_NONE):
		"""Updates the system's mouse data

		pos -- the mouse position
		click_state -- the current state of the mouse

		"""

		self.cursor_pos = pos

		# If the mouse was clicked, and handle any on_click events			
		for widget in [self._widgets[i] for i in self._widgets]:
			if (widget.gl_position[0][0] <= pos[0] <= widget.gl_position[1][0]) and \
				(widget.gl_position[0][1] <= pos[1] <= widget.gl_position[2][1]):
					widget._handle_mouse(pos, click_state)
			else:
				widget._hover = False

	def update_keyboard(self, key, is_shifted):
		"""Updates the system's keyboard data
		
		key -- the key being input
		is_shifted -- is the shift key held down?
		
		"""
		
		if self.focused_widget:
			self.focused_widget._handle_key(key, is_shifted)
		
		
	def render(self):
		"""Renders the GUI system"""

		# Get some viewport info
		view_buf = Buffer(GL_INT, 4)
		glGetIntegerv(GL_VIEWPORT, view_buf)
		view = view_buf.list

		# Save the state
		glPushAttrib(GL_ALL_ATTRIB_BITS)
		
		# Disable depth test so we always draw over things
		glDisable(GL_DEPTH_TEST)
		
		# Disable lighting so everything is shadless
		glDisable(GL_LIGHTING)
		
		# Unbinding the texture prevents BGUI frames from somehow picking up on
		# color of the last used texture
		glBindTexture(GL_TEXTURE_2D, 0)
		
		# Make sure we're using smooth shading instead of flat
		glShadeModel(GL_SMOOTH)

		# Setup the matrices
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		gluOrtho2D(0, view[2], 0, view[3])
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()

		# Render the windows
		for widget in self._widgets:
			if self._widgets[widget].visible:
				self._widgets[widget]._draw()

		# Reset the state
		glPopMatrix()
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		glPopAttrib()