import abc


#TODO: This just follows the blf interface, which isn't very Pythonic

class TextLibrary:
	"""Class for handling text drawing.	"""

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def load(self, filename):
		pass

	@abc.abstractmethod
	def draw(self, fontid, text):
		pass

	@abc.abstractmethod
	def dimensions(self, fontid, text):
		pass

	@abc.abstractmethod
	def position(self, fontid, x, y, z):
		pass

	@abc.abstractmethod
	def size(self, fontid, size, dpi):
		pass