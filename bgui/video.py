from .gl_utils import *
from .texture import VideoTexture

from .widget import Widget, BGUI_DEFAULT, WeakMethod
from .image import Image


class Video(Image):
	"""Widget for displaying video"""

	def __init__(self, parent, vid, name=None, play_audio=False, repeat=0, aspect=None, size=[1, 1], pos=[0, 0],
				sub_theme='', options=BGUI_DEFAULT):
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param vid: the video to use for the widget
		:param play_audio: play the audio track of the video
		:param repeat: how many times to repeat the video (-1 = infinite)
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the width and height
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options: various other options

		"""

		Image.__init__(self, parent, name, None, aspect, size, pos, sub_theme=sub_theme, options=options)

		self._texture = VideoTexture(vid, GL_LINEAR, repeat, play_audio)

		self._on_finish = None
		self._on_finish_called = False

	def play(self, start, end, use_frames=True, fps=None):
		self._texture.play(start, end, use_frames, fps)

		# Reset the on_finish callback after every play
		self._on_finish_called = False

	@property
	def on_finish(self):
		"""The widget's on_finish callback"""
		return self._on_finish

	@on_finish.setter
	def on_finish(self, value):
		self._on_finish = WeakMethod(value)

	def _draw(self):
		"""Draws the video frame"""

		self._texture.update()

		# Draw the textured quad
		Image._draw(self)

		# Check if the video has finished playing through
		if self._texture.video.status == 3:
			if self._on_finish and not self._on_finish_called:
				self.on_finish(self)
				self._on_finish_called = True