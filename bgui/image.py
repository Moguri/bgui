"""

This module defines the following constants:

*Texture interpolation modes*
	* BGUI_NEAREST
	* BGUI_LINEAR
"""

from bgl import *
from bge import texture

from .widget import Widget, BGUI_DEFAULT, BGUI_CACHE

# Interpolation mode constants for texture filtering
BGUI_NEAREST = GL_NEAREST
BGUI_LINEAR = GL_LINEAR


class Image(Widget):
	"""Widget for displaying images"""

	_cache = {}

	def __init__(self, parent, name, img, aspect=None, size=[0, 0], pos=[0, 0],
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

		# Generate a texture
		id_buf = Buffer(GL_INT, 1)
		glGenTextures(1, id_buf)

		self.tex_id = id_buf.to_list()[0] if hasattr(id_buf, "to_list") else id_buf.list[0]
		self.texco = texco
		self._interp_mode = interp_mode
		self.image = None
		self.update_image(img)

		self._color = [1, 1, 1, 1]

	@property
	def interp_mode(self):
		"""The type of image filtering to be performed on the texture."""
		return self._interp_mode

	@interp_mode.setter
	def interp_mode(self, value):
		self._interp_mode = value

	@property
	def color(self):
		"""The color of the plane the texture is on."""
		return self._color

	@color.setter
	def color(self, value):
		self._color = value

	def _cleanup(self):
		id_buf = Buffer(GL_INT, 1)
		id_buf[0] = self.tex_id
		glDeleteTextures(1, id_buf)

		# Set self.image to None to force ImageFFmpeg() to be deleted and free
		# its image data.
		self.image = None

		Widget._cleanup(self)

	def update_image(self, img):
		"""Changes the image texture

		:param img: the path to the new image
		:rtype: None
		"""

		# Try to avoid unnecessary texture uploads
		if img == self.image:
			return

		self.image = img

		glBindTexture(GL_TEXTURE_2D, self.tex_id)

		if img in Image._cache:
			# Image has already been loaded from disk, recall it from the cache
			image = Image._cache[img]
		else:
			# Load the texture data from disk
			image = texture.ImageFFmpeg(img)
			image.scale = False
			if self.options & BGUI_CACHE:
				Image._cache[img] = image

		im_buf = image.image

		# If the image failed to load the im_buf will be None
		# If this happens stop before things get ugly.
		if im_buf == None:
			print("Unable to load the image %s" % img)
			return

		# Setup some parameters
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.interp_mode)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.interp_mode)

		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

		# Upload the texture data
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0,
						GL_RGBA, GL_UNSIGNED_BYTE, im_buf)

	def _draw(self):
		"""Draws the image"""

		# Enable textures
		glEnable(GL_TEXTURE_2D)

		# Enable alpha blending
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		# Bind the texture
		glBindTexture(GL_TEXTURE_2D, self.tex_id)

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
