from .Widget import *
from .Label import *
from .Frame import *

class TextInput(Widget):
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
		Widget.__init__(self, parent, name, size, pos, options)
		self.frame = Frame(self, name+"_frame")
		self.frame.colors = [(0, 0, 0, 0)] *4
		
		self.label = Label(self.frame, name+"_label", text, font, pt_size, color)
		
		self.pos = len(text)
				
	@property
	def text(self):
		return self.label.text
	
	@text.setter
	def text(self, value):
		self.label.text = value

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
		elif key == BACKSPACEKEY and self.pos > 0:
			self.text = self.text[:self.pos-1] + self.text[self.pos:]
			self.pos -= 1
		elif key == LEFTARROWKEY and self.pos > 0:
			self.pos -= 1
		elif key == RIGHTARROWKEY and self.pos > 0:
			self.pos += 1
		
		Widget._handle_key(self, key, is_shifted)
		
	def _draw(self):
		temp = self.text
		
		if self._active:
			self.text = self.text[:self.pos] +"|"+ self.text[self.pos:]
		
		# Now draw the children
		Widget._draw(self)
		
		self.label.text = temp