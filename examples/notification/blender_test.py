import sys

# So we can find the bgui module
sys.path.append('../..')

import bgui
import bge
import time

class MySys(bgui.System):
	"""
	A subclass to handle our game specific gui
	"""

	def __init__(self):
		# Initialize the system
		bgui.System.__init__(self)
		self.clear_time = time.time()
		self.note_visible = False

		self.frame = bgui.Frame(self, 'frame', aspect=(4/3),
					options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.frame.visible = False
		# Create the note
		self.note = bgui.Frame(self, 'note', border=1, size=[.25, .25], pos=[0.7, -0.3],
				options=bgui.BGUI_DEFAULT)
		self.note.colors = [[0, 0, 1, 0.5]] * 4
		self.note_hdr = bgui.Label(self.note, 'hdr', text="Notification:", pt_size=42, pos=[0.05, 0.8])
		self.note_msg = bgui.Label(self.note, 'msg', text="The button was clicked!", pos=[0.1, 0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERY)
		
		# Create the button
		self.button = bgui.FrameButton(self, 'btn', text='Click Me!', size=[0.4, 0.2],
				pos=[0.3, 0.4])
		self.button.on_click = self.display_note
		
		# Create a keymap for keyboard input
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}

	def note_finished(self):
		self.note_visible = True
		self.clear_time = time.time()+1
		
	def hide_note(self):
		x=self.note.position[0]/self.size[0]
		self.note.move([x, -0.3], 750)

	def display_note(self, widget):
		print("Displaying note")
		x=self.note.position[0]/self.size[0]
		self.note.move([x, -.05], 750, self.note_finished)
		
	def update(self):
		if self.note_visible and time.time() > self.clear_time:
			print("Hiding note")
			self.hide_note()
			self.note_visible = False

	def main(self):
		"""A high-level method to be run every frame"""
		
		self.update()
		
		# Handle the mouse
		mouse = bge.logic.mouse
		
		pos = list(mouse.position)
		pos[0] *= bge.render.getWindowWidth()
		pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])
		
		mouse_state = bgui.BGUI_MOUSE_NONE
		mouse_events = mouse.events
				
		if mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			mouse_state = bgui.BGUI_MOUSE_CLICK
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_RELEASED:
			mouse_state = bgui.BGUI_MOUSE_RELEASE
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_ACTIVE:
			mouse_state = bgui.BGUI_MOUSE_ACTIVE
		
		self.update_mouse(pos, mouse_state)
		
		# Handle the keyboard
		keyboard = bge.logic.keyboard
		
		key_events = keyboard.events
		is_shifted = key_events[bge.events.LEFTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE or \
					key_events[bge.events.RIGHTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE
					
		for key, state in keyboard.events.items():
			if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
				self.update_keyboard(self.keymap[key], is_shifted)
		
		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().post_draw = [self.render]

def main(cont):
	own = cont.owner
	mouse = bge.logic.mouse

	if 'sys' not in own:
		# Create our system and show the mouse
		own['sys'] = MySys()
		mouse.visible = True

	else:
		own['sys'].main()
