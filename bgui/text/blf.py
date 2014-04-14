from . import TextLibrary
import blf

class BlfTextLibrary(TextLibrary):
	"""Text library wrapper around blf"""

	def draw(self, fontid, text):
		blf.draw(fontid, text)

	def size(self, fontid, size, dpi):
		blf.size(fontid, size, dpi)

	def position(self, fontid, x, y, z):
		blf.position(fontid, x, y, z)

	def dimensions(self, fontid, text):
		return blf.dimensions(fontid, text)

	def load(self, filename):
		return blf.load(filename)
