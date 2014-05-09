"""

This module defines the following constants:

*Texture interpolation modes*
	* BGUI_NEAREST
	* BGUI_LINEAR
"""

from .gl_utils import *
from .texture import ImageTexture

from .widget import Widget, BGUI_DEFAULT, BGUI_CACHE

# Interpolation mode constants for texture filtering
BGUI_NEAREST = GL_NEAREST
BGUI_LINEAR = GL_LINEAR


class Image(Widget):
	"""Widget for displaying images"""

	def __init__(self, parent, img, name=None, aspect=None, size=[1, 1], pos=[0, 0],
				texco=[(0, 0), (1, 0), (1, 1), (0, 1)], interp_mode=BGUI_LINEAR, sub_theme='', options=BGUI_DEFAULT):
		""":param parent: the widget's parent
		:param name: the name of the widget
		:param img: the image to use for the widget
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the width and height
		:param pos: a tuple containing the x and y position
		:param texco: the UV texture coordinates to use for the image
		:param interp_mode: texture interpolating mode for both maximizing and minifying the texture (defaults to BGUI_LINEAR)
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options
		"""

		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)

		if img != None:
			self._texture = ImageTexture(img, interp_mode, options & BGUI_CACHE)
		else:
			self._texture = None

		#: The UV texture coordinates to use for the image.
		self.texco = texco

		#: The color of the plane the texture is on.
		self.color = [1, 1, 1, 1]

	@property
	def interp_mode(self):
		"""The type of image filtering to be performed on the texture."""
		return self._texture.interp_mode

	@interp_mode.setter
	def interp_mode(self, value):
		self._texture.interp_mode = value

	@property
	def image_size(self):
		"""The size (in pixels) of the currently loaded image, or [0, 0] if an image is not loaded"""
		return self._texture.size

	def update_image(self, img):
		"""Changes the image texture

		:param img: the path to the new image
		:rtype: None
		"""

		self._texture.reload(img)

	def _draw(self):
		"""Draws the image"""

		# Enable textures
		glEnable(GL_TEXTURE_2D)

		# Enable alpha blending
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		# Bind the texture
		self._texture.bind()

		# Draw the textured quad
		glColor4f(*self.color)

		glBegin(GL_QUADS)
		for i in range(4):
			glTexCoord2f(self.texco[i][0], self.texco[i][1])
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()

		glBindTexture(GL_TEXTURE_2D, 0)

		# Now draw the children
		Widget._draw(self)
