from .Widget import *
from .Label import *

class TextInput(Label):
	"""Widget for getting text input"""

	def __init__(self, parent, name, text="", font=None, pt_size=30, color=(1, 1, 1, 1), size=[0, 0], pos=[0, 0], options=BGUI_DEFAULT):
		"""The TextInput constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		text -- the text to display (this can be changed later via the text property)
		font -- the font to use
		pt_size -- the point size of the text to draw
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		options -- various other options

		"""
		Label.__init__(self, parent, name, text, font, pt_size, color, pos, options)
		
		self.pos = len(text)
		
	def _handle_key(self, key, is_shifted):
		"""Handle any keyboard input"""
		
		# Try char to int conversion for alphanumeric keys... kinda hacky though
		try:
			key = ord(key)
		except:
			pass
			
		if ord(AKEY) <= key <= ord(ZKEY):
			if is_shifted:
				key -= 32
			self.text = self.text[:self.pos] + chr(key) + self.text[self.pos:]
			self.pos += 1
		if ord(ZEROKEY) <= key <= ord(NINEKEY):
			self.text = self.text[:self.pos] + chr(key) + self.text[self.pos:]
			self.pos += 1
		elif key == SPACEKEY:
			self.text = self.text[:self.pos] + " " + self.text[self.pos:]
			self.pos += 1
		elif key == BACKSPACEKEY:
			self.text = self.text[:self.pos-1] + self.text[self.pos:]
			self.pos -= 1
		elif key == LEFTARROWKEY:
			self.pos -= 1
		elif key == RIGHTARROWKEY:
			self.pos += 1
		
		Widget._handle_key(self, key, is_shifted)
		
	def _draw(self):
		temp = self.text
		
		if self._active:
			self.text = self.text[:self.pos] +"|"+ self.text[self.pos:]
		
		Label._draw(self)
		
		self.text = temp