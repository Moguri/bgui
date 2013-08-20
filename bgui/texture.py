# This module encapsulates texture loading so we are not dependent on bge.texture

from .gl_utils import *
try:
	from bge import texture
	USING_BGE_TEXTURE = True
except ImportError:
	USING_BGE_TEXTURE = False

class ImageTexture:

	_cache = {}

	def __init__(self, image, interp_mode, caching):
		self._tex_id = glGenTextures(1)
		self.size = [0, 0]
		self.image_name = None
		self._interp_mode = None
		self._caching = caching

		# Setup some parameters
		self.bind()
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
		self.interp_mode = interp_mode

		self.reload(image)

	def __del__(self):
		glDeleteTextures([self._tex_id])

	@property
	def interp_mode(self):
		return self._interp_mode

	@interp_mode.setter
	def interp_mode(self, value):
		if value != self._interp_mode:
			self.bind()
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, value)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, value)
			self._interp_mode = value

	def reload(self, image):
		if image == self.image_name:
			return

		self.bind()

		if image in ImageTexture._cache:
			# Image has already been loaded from disk, recall it from the cache
			img = ImageTexture._cache[image]
		else:
			# Load the image data from disk
			if USING_BGE_TEXTURE:
				img = texture.ImageFFmpeg(image)
				img.scale = False
				if self._caching:
					ImageTexture._cache[image] = img

		if USING_BGE_TEXTURE:
			data = img.image
		else:
			data = None

		if data == None:
			print("Unabled to load the image", image)
			return

		# Upload the texture data
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0,
						GL_RGBA, GL_UNSIGNED_BYTE, data)

		# Save the image size and name
		self.image_size = img.size[:]
		self.image_name = image

		img = None

	def bind(self):
		glBindTexture(GL_TEXTURE_2D, self._tex_id)
