# This file handles differences between BGL and PyOpenGL, and provides various
# utility functions for OpenGL

try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
	from bgl import Buffer
	USING_BGL = False
except ImportError:
	from bgl import *
	USING_BGL = True

if USING_BGL:
	_glGenTextures = glGenTextures
	def glGenTextures(n, textures=None):
		id_buf = Buffer(GL_INT, n)
		_glGenTextures(n, id_buf)

		if textures:
			textures.extend(id_buf.to_list())

		return id_buf.to_list()[0] if n == 1 else id_buf.to_list()


	_glDeleteTextures = glDeleteTextures
	def glDeleteTextures(textures):
		n = len(textures)
		id_buf = Buffer(GL_INT, n, textures)
		_glDeleteTextures(n, id_buf)


	_glGetIntegerv = glGetIntegerv
	def glGetIntegerv(pname):
		# Only used for GL_VIEWPORT right now, so assume we want a size 4 Buffer
		buf = Buffer(GL_INT, 4)
		_glGetIntegerv(pname, buf)
		return buf.to_list()

else:
	_glTexImage2D = glTexImage2D
	def glTexImage2D(target, level, internalFormat, width, height, border, format, type, data):
		_glTexImage2D(target, level, internalFormat, width, height,
			border, format, type, data.to_list())
