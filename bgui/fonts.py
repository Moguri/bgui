try:
	from blf import *
	USING_BLF = True
except ImportError:
	from PyQt4 import QtGui, QtOpenGL
	USING_BLF = False

	GL_WIDGET = None


	_fonts = {0: [QtGui.QFont("Ruthie", 11), (0, 0)]}

	def load(filename):
		if filename not in _fonts:
			id = QtGui.QFontDatabase.addApplicationFont(filename)
			if id < 0:
				print("Error loading font", filename, "using default font.")
				_fonts[filename] = _fonts[0]
			else:
				family = QtGui.QFontDatabase.applicationFontFamilies(id)[0]
				_fonts[filename] = [QtGui.QFont(family), (0, 0)]

		return filename


	def draw(fontid, text):
		assert(GL_WIDGET is not None)
		font, s = _fonts[fontid]
		
		GL_WIDGET.renderText(s[0], s[1], 0, text, font)


	def dimensions(fontid, text):
		fm = QtGui.QFontMetrics(_fonts[fontid][0])
		
		return (fm.width(text), fm.height())


	def position(fontid, x, y, z):
		_fonts[fontid][1] = (x, y)


	def size(fontid, size, dpi):
		_fonts[fontid][0].setPointSize(size)