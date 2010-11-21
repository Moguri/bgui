from bgl import *
import bge

from .Widget import *

class Video(Widget):
	"""Widget for displaying video"""
	
	def __init__(self, parent, name, vid, aspect=None, size=[0, 0], pos=[0, 0],
				sub_theme='', options=BGUI_DEFAULT):
		"""The Video constructor
		
		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		vid -- the video to use for the widget
		aspect -- constrain the widget size to a specified aspect ratio
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""
		
		Widget.__init__(self, parent, name, aspect, size, pos, sub_theme, options)
		
		# Generate a texture
		
		id_buf = Buffer(GL_INT, 1)
		glGenTextures(1, id_buf)
		
		self.tex_id = id_buf.list[0]
		
		# Bind and load the texture data
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		video = bge.texture.VideoFFmpeg(vid)
		video.repeat = -1
		video.play()
		im_buf = video.image
		
		# Setup some parameters
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

		# Upload the texture data
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, video.size[0], video.size[1],
						0, GL_RGBA, GL_UNSIGNED_BYTE, im_buf)
						
		# Store the video for later
		self.video = video
		
	def _draw(self):
		"""Draws the video frame"""
		
		# Enable textures and alpha blending
		glEnable(GL_TEXTURE_2D)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		# Bind the texture
		glBindTexture(GL_TEXTURE_2D, self.tex_id)
		texco = [(0, 0), (1, 0), (1, 1), (0, 1)]
		
		# Upload the next fram to the graphics
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
		self.video.refresh()
		
		# Now draw the children
		Widget._draw(self)