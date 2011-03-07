from bgl import *
import bge

from .widget import *

class Image(Widget):
	"""Widget for displaying images"""
	
	_cache = {}
	
	def __init__(self, parent, name, img, aspect=None, size=[0, 0], pos=[0, 0],
				sub_theme='', options=BGUI_DEFAULT):
		""":param parent: the widget's parent
		:param name: the name of the widget
		:param img: the image to use for the widget
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the wdith and height
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options
		"""

		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)

		# Generate a texture
		id_buf = Buffer(GL_INT, 1)
		glGenTextures(1, id_buf)

		self.tex_id = id_buf.list[0]


		self.update_image(img)

	def _cleanup(self):
		id_buf = Buffer(GL_INT, 1)
		id_buf[0] = self.tex_id
		glDeleteTextures(1, id_buf)
		
		Widget._cleanup(self)

	def update_image(self, img):
		"""Changes the image texture

		:param img: the path to the new image
		:rtype: None
		"""

		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		
		if img in Image._cache:
			# Image has already been loaded from disk, recall it from the cache
			image = Image._cache[img]
		else:
			# Load the texture data from disk
			image = bge.texture.ImageFFmpeg(img)
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
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

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
		texco = [(0, 0), (1, 0), (1, 1), (0, 1)]

		# Draw the textured quad
		glColor4f(1, 1, 1, 1)

		glBegin(GL_QUADS)
		for i in range(4):
			glTexCoord2f(texco[i][0], texco[i][1])
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()

		glBindTexture(GL_TEXTURE_2D, 0)

		# Now draw the children
		Widget._draw(self)