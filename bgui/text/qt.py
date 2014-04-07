from PyQt4 import QtGui, QtOpenGL
from . import TextLibrary


class QtTextLibrary(TextLibrary):
	"""Text library wrapper around PyQt"""

	def __init__(self, gl_widget):
		self._gl_widget = gl_widget
		self._fonts = {0: [QtGui.QFont("Ruthie", 11), (0, 0)]}

	def load(self, filename):
		if filename not in self._fonts:
			fid = QtGui.QFontDatabase.addApplicationFont(filename)
			if fid < 0:
				print("Error loading font", filename, "using default font.")
				self._fonts[filename] = self._fonts[0]
			else:
				family = QtGui.QFontDatabase.applicationFontFamilies(fid)[0]
				self._fonts[filename] = [QtGui.QFont(family), (0, 0)]

		return filename

	def draw(self, fontid, text):
		font, s = self._fonts[fontid]

		self._gl_widget.renderText(s[0], s[1], 0, text, font)

	def dimensions(self, fontid, text):
		fm = QtGui.QFontMetrics(self._fonts[fontid][0])

		return (fm.width(text), fm.height())

	def position(self, fontid, x, y, z):
		self._fonts[fontid][1] = (x, y)

	def size(self, fontid, size, dpi):
		self._fonts[fontid][0].setPointSize(size)