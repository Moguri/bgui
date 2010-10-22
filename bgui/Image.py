from bgl import *
import bge

from .Widget import *

class Image(Widget):
	"""Widget for displaying images"""

	def __init__(self, parent, name, img, aspect=None, size=[0, 0], pos=[0, 0], options=BGUI_DEFAULT):
		"""The ImageWidget constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		img -- the image to use for the widget
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""

		Widget.__init__(self, parent, name, size, pos, options)
		
		if aspect:
			# print(self._base_size[1], (aspect))
			# size = [self._base_size[0], self._base_size[0]/aspect]
			size = [self.size[1]*aspect, self.size[1]]
			if self.options & BGUI_NORMALIZED:
				size = [size[0]/self.parent.size[0], size[1]/self.parent.size[1]]
			self._update_position(size, self._base_pos)
			# print(self.size)

		# Generate a texture
		id_buf = Buffer(GL_INT, 1)
		glGenTextures(1, id_buf)

		self.tex_id = id_buf.list[0]


		self.update_image(img)

	def _cleanup(self):
		id_buf = Buffer(GL_INT, 1)
		id_buf.list[0] = self.tex_id
		glDeleteTextures(1, id_buf)
		
		Widget._cleanup(self)

	def update_image(self, img):
		"""Change's the image texture

		Arguments
		img -- the path to the new image

		"""

		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		
		# Load the texture data
		image = bge.texture.ImageFFmpeg(img)
		image.scale = False
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