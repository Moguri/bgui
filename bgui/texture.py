# This module encapsulates texture loading so we are not dependent on bge.texture

from .gl_utils import *
try:
	from bge import texture
	import aud
	USING_BGE_TEXTURE = True
except ImportError:
	from PyQt4 import QtOpenGL, QtGui
	USING_BGE_TEXTURE = False

class Texture:
	def __init__(self, path, interp_mode):
		self._tex_id = glGenTextures(1)
		self.size = [0, 0]
		self._interp_mode = None
		self.path = None

		# Setup some parameters
		self.bind()
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
		self.interp_mode = interp_mode

		self.reload(path)

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

	def bind(self):
		glBindTexture(GL_TEXTURE_2D, self._tex_id)


class ImageTexture(Texture):

	_cache = {}

	def __init__(self, image, interp_mode, caching):
		self._caching = caching
		super().__init__(image, interp_mode);

	def reload(self, image):
		if image == self.path:
			return

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
			else:
				img = QtGui.QImage(image)

		if USING_BGE_TEXTURE:
			data = img.image
			if data == None:
				print("Unabled to load the image", image)
				return

			# Upload the texture data
			self.bind()
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0,
							GL_RGBA, GL_UNSIGNED_BYTE, data)

			self.image_size = img.size[:]
		else:
			if img.isNull():
				print("Unable to load the image", image)
				return
			glDeleteTextures([self._tex_id])
			self._tex_id = QtOpenGL.QGLContext.currentContext().bindTexture(img)
			self.interp_mode = self.interp_mode
			self.image_size = [img.width(), img.height()]


		# Save the image name
		self.path = image

		img = None


class VideoTexture(Texture):
	def __init__(self, video, interp_mode, repeat, play_audio):
		self.repeat = repeat
		self.play_audio = play_audio
		self.video = None
		self.audio = None

		super().__init__(video, interp_mode)

	def __del__(self):
		super().__del__()

		if self.audio:
			self.audio.stop()

		self.video = None

	def reload(self, video):
		if video == self.path:
			return

		if USING_BGE_TEXTURE:
			vid = texture.VideoFFmpeg(video)
			vid.repeat = self.repeat
			vid.play()
			self.video = vid
			data = vid.image

			if self.play_audio:
				self.audio = aud.device().play(aud.Factory(video))
		else:
			data = None

		if data == None:
			print("Unable to load the video", video)
			return

		self.bind()
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, vid.size[0], vid.size[1],
				0, GL_RGBA, GL_UNSIGNED_BYTE, data)

		self.image_size = vid.size[:]
		self.path = video

	def update(self):
		if not self.video:
			return

		self.video.refresh()
		data = self.video.image
		if data:
			self.bind()
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.video.size[0], self.video.size[1],
					0, GL_RGBA, GL_UNSIGNED_BYTE, data)

	def play(self, start, end, use_frames=True, fps=None):
		if not self.video:
			return

		start = float(start)
		end = float(end)

		if use_frames:
			if not fps:
				fps = self.video.framerate
				print("Using fps:", fps)
			start /= fps
			end /= fps

		if start == end:
			end += 0.1
		self.video.stop()
		self.video.range = [start, end]
		self.video.play()
