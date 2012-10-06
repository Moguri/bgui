from bgl import *
from bge import texture
import aud

from .widget import Widget, BGUI_DEFAULT
from .image import Image


class Video(Image):
	"""Widget for displaying video only (i.e., no sound)"""

	def __init__(self, parent, name, vid, play_audio=False, repeat=0, aspect=None, size=[1, 1], pos=[0, 0],
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

		# Bind and load the texture data
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		video = texture.VideoFFmpeg(vid)
		video.repeat = repeat
		video.play()
		im_buf = video.image

		if im_buf:
			# Setup some parameters
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

			glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

			# Upload the texture data
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, video.size[0], video.size[1],
							0, GL_RGBA, GL_UNSIGNED_BYTE, im_buf)
		else:
			print("Unable to load the video:", vid)

		if play_audio:
			f = aud.Factory(vid)
			self.aud_handle = aud.device().play(f)
		else:
			self.aud_handle = None

		# Store the video for later
		self.video = video

	def play(self, start, end, use_frames=True, fps=None):
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

	def _cleanup(self):
		if self.aud_handle:
			self.aud_handle.stop()

		# Set self.video to None to force VideoFFmpeg() to be deleted and free
		# its video data.
		self.video = None
		Image._cleanup(self)

	def update_image(self, img):
		"""This does nothing on a Video widget"""

		# This breaks the Liskov substitution principle, but I think the way to solve
		# that is to change the Image interface a bit to avoid the problem.

		Image.update_image(self, None)

	def _draw(self):
		"""Draws the video frame"""

		# Upload the next frame to the graphics
		im_buf = self.video.image

		if im_buf:
			glBindTexture(GL_TEXTURE_2D, self.tex_id)
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.video.size[0], self.video.size[1],
							0, GL_RGBA, GL_UNSIGNED_BYTE, im_buf)

		# Draw the textured quad
		Image._draw(self)

		# Invalidate the image
		self.video.refresh()
