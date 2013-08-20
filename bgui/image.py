"""

This module defines the following constants:

*Texture interpolation modes*
	* BGUI_NEAREST
	* BGUI_LINEAR
"""

from . import gl_utils
from .gl_utils import *
from bge import texture

from .widget import Widget, BGUI_DEFAULT, BGUI_CACHE

# Interpolation mode constants for texture filtering
BGUI_NEAREST = gl_utils.GL_NEAREST
BGUI_LINEAR = gl_utils.GL_LINEAR


class Image(Widget):
	"""Widget for displaying images"""

	_cache = {}

	def __init__(self, parent, img, name=None, aspect=None, size=[0, 0], pos=[0, 0],
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
		self.tex_id = glGenTextures(1)
		
		self.texco = texco
		
		#: The type of image filtering to be performed on the texture.
		self.interp_mode = interp_mode
		self.image = None
		
		#: The size (in pixels) of the currently loaded image, or [0, 0] if an image is not loaded
		self.image_size = [0, 0]
		
		self.update_image(img)
		
		#: The color of the plane the texture is on.
		self.color = [1, 1, 1, 1]

	def __del__(self):
		super().__del__()

		glDeleteTextures([self.tex_id])

		# Set self.image to None to force ImageFFmpeg() to be deleted and free
		# its image data.
		self.image = None

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
		
		# Save the image size
		self.image_size = image.size[:]

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
