from bgl import *
import bge
import aud

from .widget import *

class Video(Widget):
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
		
		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)
		
		# Generate a texture
		
		id_buf = Buffer(GL_INT, 1)
		glGenTextures(1, id_buf)
		
		self.tex_id = id_buf.list[0]
		
		# Bind and load the texture data
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		video = bge.texture.VideoFFmpeg(vid)
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
		
	def _cleanup(self):
		id_buf = Buffer(GL_INT, 1)
		id_buf[0] = self.tex_id
		glDeleteTextures(1, id_buf)
		
		if self.aud_handle:
			self.aud_handle.stop()
			
		del self.video
		
		Widget._cleanup(self)
		
	def _draw(self):
		"""Draws the video frame"""
		
		# Enable textures and alpha blending
		glEnable(GL_TEXTURE_2D)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		# Bind the texture
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		texco = [(0, 0), (1, 0), (1, 1), (0, 1)]
		
		# Upload the next frame to the graphics
		im_buf = self.video.image
		
		if im_buf:
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.video.size[0], self.video.size[1],
							0, GL_RGBA, GL_UNSIGNED_BYTE, im_buf)
		
		# Draw the textured quad
		glColor4f(1, 1, 1, 1)
		
		glBegin(GL_QUADS)
		for i in range(4):
			glTexCoord2f(texco[i][0], texco[i][1])
			glVertex2f(self.gl_position[i][0], self.gl_position[i][1])
		glEnd()
		
		glBindTexture(GL_TEXTURE_2D, 0)
		
		# Invalidate the image
		if self.aud_handle:
			self.video.preseek = int(self.aud_handle.position)
			self.video.play()
		self.video.refresh()
		
		# Now draw the children
		Widget._draw(self)