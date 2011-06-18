"""
ListBoxes make use of a ListBoxRenderer. The default ListBoxRenderer simply
displays an item's string representation. To make your own ListBoxRenderer
create a class that has a render_item() method that accepts the item to be rendered
and returns a widget to render.

Here is an simple example of using the ListBox widget::

	class MySys(bgui.System):
		def lb_click(self, lb):
			print(lb.selected)
		
		def __init__(self):
			bgui.System.__init__(self)
			
			items = ["One", "Two", 4, 4.6]
			self.frame = bgui.Frame(self, 'window', border=2, size=[0.5, 0.5],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			self.lb = bgui.ListBox(self.frame, "lb", items=items, padding=0.05, size=[0.9, 0.9], pos=[0.05, 0.05])
			self.lb.on_click = self.lb_click
			
			# ... rest of __init__

"""

from .widget import *
from .frame import *
from .label import *

class ListBoxRenderer():
	"""Base class for rendering an item in a ListBox"""
	def __init__(self, listbox):
		"""
		:param listbox: the listbox the renderer will be used with (used for parenting)
		"""
		self.label = Label(listbox, "label")
	
	def render_item(self, item):
		"""Creates and returns a :py:class:`bgui.label.Label` representation of the supplied item
		
		:param item: the item to be rendered
		:rtype: :py:class:`bgui.label.Label`
		"""
		self.label.text=item.__repr__()
		
		return self.label

class ListBox(Widget):
	"""Widget for displaying a list of data"""
	
	theme_section = 'ListBox'
	theme_options = {
				'HighlightColor1',
				'HighlightColor2',
				'HighlightColor3',
				'HighlightColor4',
				'Border',
				'Padding'
				}
	
	def __init__(self, parent, name, items=[], padding=0, aspect=None, size=[1, 1], pos=[0, 0], sub_theme='', options=BGUI_DEFAULT):
		"""
		:param parent: the widget's parent
		:param name: the name of the widget
		:param items: the items to fill the list with (can also be changed via ListBox.items)
		:param padding: the amount of extra spacing to put between items (can also be changed via ListBox.padding)
		:param aspect: constrain the widget size to a specified aspect ratio
		:param size: a tuple containing the width and height
		:param pos: a tuple containing the x and y position
		:param sub_theme: name of a sub_theme defined in the theme file (similar to CSS classes)
		:param options:	various other options
		"""
		
		Widget.__init__(self, parent, name, aspect=aspect, size=size, pos=pos, sub_theme='', options=options)
		
		theme = self.theme[self.theme_section] if self.theme else None
		
		self.items = items
		if padding:
			self._padding = padding
		elif theme:
			self._padding = theme['Padding']
		else: # Use the default
			self._padding = padding
			
		self.highlight = Frame(self, "frame", border=1, size=[1, 1], pos=[0, 0])
		self.highlight.visible = False
		if theme:
			self.highlight.border = theme['Border']
		if theme:
			self.highlight.colors = [
					theme['HighlightColor1'],
					theme['HighlightColor2'],
					theme['HighlightColor3'],
					theme['HighlightColor4'],
					]
		
		self.selected = None
		self._spatial_map = {}
		
		self._renderer = ListBoxRenderer(self)
		
	##
	# These props are created simply for documentation purposes
	#
	@property
	def renderer(self):
		"""The ListBoxRenderer to use to display items"""
		return self._renderer
		
	@renderer.setter
	def renderer(self, value):
		self._renderer = value
		
	@property
	def padding(self):
		"""The amount of extra spacing to put between items"""
		return self._padding
	
	@padding.setter
	def padding(self, value):
		self._padding = value
		
	def _draw(self):
		
		for idx, item in enumerate(self.items):
			w = self.renderer.render_item(item)
			w.position = [0, 1-(idx+1)*(w.size[1]/self.size[1])-(idx*self.padding)]
			w.size = [1, w.size[1]/self.size[1]]
			self._spatial_map[item] = [i[:] for i in w.gl_position] # Make a full copy
			w._draw()
			
			if self.selected == item:
				self.highlight.gl_position = [i[:] for i in w.gl_position]
				self.highlight.visible = True
			
		Widget._draw(self)
		
	def _handle_mouse(self, pos, event):
		self.selected = None
	
		if event == BGUI_MOUSE_CLICK:
			for item, gl_position in self._spatial_map.items():
				if (gl_position[0][0] <= pos[0] <= gl_position[1][0]) and \
					(gl_position[0][1] <= pos[1] <= gl_position[2][1]):
						self.selected = item
		
		Widget._handle_mouse(self, pos, event)