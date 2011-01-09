from .Widget import *
from .Label import *
from .Frame import *

class TextInput(Widget):
	"""Widget for getting text input"""

	def __init__(self, parent, name, text="", prefix="", font=None, pt_size=30, color=(1, 1, 1, 1),
					aspect=None, size=[0, 0], pos=[0, 0], sub_theme='', options=BGUI_DEFAULT):
		"""The TextInput constructor

		Arguments:

		parent -- the widget's parent
		name -- the name of the widget
		text -- the text to display (this can be changed later via the text property)
		prefix -- prefix text displayed before user input, cannot be edited by user (this can be changed later via the prefix property)
		font -- the font to use
		pt_size -- the point size of the text to draw
		color -- color of the font for this widget
		aspect -- constrain the widget size to a specified aspect ratio
		size -- a tuple containing the wdith and height
		pos -- a tuple containing the x and y position
		sub_theme -- sub theme to be applied to this widget
		options -- various other options

		"""
		Widget.__init__(self, parent, name, aspect, size, pos, options)
		self.frame = Frame(self, name+"_frame", size=[1,1], options = BGUI_NO_FOCUS)
		self.frame.colors = [(0, 0, 0, 0)] *4
		
		self.label = Label(self.frame, name+"_label", text, font, pt_size, color, options = BGUI_NO_FOCUS)
		
		self.text_prefix = prefix
		self.pos = len(text)
		
		# On Enter callback
		self.on_enter_key = None
				
	@property
	def text(self):
		return self.label.text
	
	@text.setter
	def text(self, value):
		self.label.text = value

	def _handle_key(self, key, is_shifted):
		"""Handle any keyboard input"""
		# Check that pos is within text bounds.
		if 0 > self.pos or self.pos > len(self.text):
			self.pos = len(self.text)
		
		# Try char to int conversion for alphanumeric keys... kinda hacky though
		try:
			key = ord(key)
		except:
			pass
			
		if key == BACKSPACEKEY and self.pos > 0:
			self.text = self.text[:self.pos-1] + self.text[self.pos:]
			self.pos -= 1
		elif key == LEFTARROWKEY and self.pos > 0:
			self.pos -= 1
		elif key == RIGHTARROWKEY and self.pos >= 0:
			self.pos += 1
		else:
			char = None
			if ord(AKEY) <= key <= ord(ZKEY):
				if is_shifted: char = chr(key - 32)
				else: char = chr(key)
				
			elif ord(ZEROKEY) <= key <= ord(NINEKEY):
				if not is_shifted: char = chr(key)
				else:
					key = chr(key)
					if key == ZEROKEY: char = ")"
					elif key == ONEKEY: char = "!"
					elif key == TWOKEY: char = "@"
					elif key == THREEKEY: char = "#"
					elif key == FOURKEY: char = "$"
					elif key == FIVEKEY: char = "%"
					elif key == SIXKEY: char = "^"
					elif key == SEVENKEY: char = "&"
					elif key == EIGHTKEY: char = "*"
					elif key == NINEKEY: char = "("
					
			elif PAD0 <= key <= PAD9:
				char = str(key-PAD0)
			elif key == PADPERIOD: char = "."
			elif key == PADSLASHKEY: char = "/"
			elif key == PADASTERKEY: char = "*"
			elif key == PADMINUS: char = "-"
			elif key == PADPLUSKEY: char = "+"
			elif key == SPACEKEY: char = " "
			elif key == TABKEY: char = "\t"
			elif key in (ENTERKEY, PADENTER):
				if self.on_enter_key:
					self.on_enter_key(self)
			elif not is_shifted:
				if key == ACCENTGRAVEKEY: char = "`"
				elif key == MINUSKEY: char = "-"
				elif key == EQUALKEY: char = "="
				elif key == LEFTBRACKETKEY: char = "["
				elif key == RIGHTBRACKETKEY: char = "]"
				elif key == BACKSLASHKEY: char = "\\"
				elif key == SEMICOLONKEY: char = ";"
				elif key == QUOTEKEY: char = "'"
				elif key == COMMAKEY: char = ","
				elif key == PERIODKEY: char = "."
				elif key == SLASHKEY: char = "/"
			else:
				if key == ACCENTGRAVEKEY: char = "~"
				elif key == MINUSKEY: char = "_"
				elif key == EQUALKEY: char = "+"
				elif key == LEFTBRACKETKEY: char = "{"
				elif key == RIGHTBRACKETKEY: char = "}"
				elif key == BACKSLASHKEY: char = "|"
				elif key == SEMICOLONKEY: char = ":"
				elif key == QUOTEKEY: char = '"'
				elif key == COMMAKEY: char = "<"
				elif key == PERIODKEY: char = ">"
				elif key == SLASHKEY: char = "?"
				
			if char:
				self.text = self.text[:self.pos] + char + self.text[self.pos:]
				self.pos += 1
		
	def _draw(self):
		temp = self.text
		
		if self == self.system.focused_widget:
			self.text = self.text[:self.pos] +"|"+ self.text[self.pos:]
		
		self.text = self.text_prefix + self.text
		
		# Now draw the children
		Widget._draw(self)
		
		self.label.text = temp