from bgl import *
from .widget import *
from .theme import *

class System(Widget):
	"""The main gui system. Add widgets to this and then call the render() method
	draw the gui.

	"""

	normalize_text = True
	
	def __init__(self, theme=None):
		"""
		:param theme: the path to a theme directory
		
		"""

		# Size and positions for children to use.
		# The size will the the view port size and
		# the position will be the top left of the screen

		# Get some viewport info
		view_buf = Buffer(GL_INT, 4)
		glGetIntegerv(GL_VIEWPORT, view_buf)
		view = view_buf.list
		
		# Theming
		self.system = self
		self.theme = Theme(theme) if theme else None
		self.focused_widget = None
		self.lock_focus = False
		
		Widget.__init__(self, self, "<System>", size=[view[2], view[3]],
					pos=[0, 0], options=0)
		

	def update_mouse(self, pos, click_state=BGUI_MOUSE_NONE):
		"""Updates the system's mouse data

		:param pos: the mouse position
		:param click_state: the current state of the mouse
		:rtype: None

		"""

		self.cursor_pos = pos

		Widget._handle_mouse(self, pos, click_state)

	def update_keyboard(self, key, is_shifted):
		"""Updates the system's keyboard data
		
		:param key: the key being input
		:param is_shifted: is the shift key held down?
		:rtype: None
		
		"""
		
		if self.focused_widget:
			self.focused_widget._handle_key(key, is_shifted)
		
	def _attach_widget(self, widget):
		if widget == self:
			return 
		
		Widget._attach_widget(self, widget)
	def render(self):
		"""Renders the GUI system
		
		:rtype: None
		
		"""

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
		
		# Update any animations
		Widget._update_anims(self)

		# Render the windows
		Widget._draw(self)

		# Reset the state
		glPopMatrix()
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		glPopAttrib()