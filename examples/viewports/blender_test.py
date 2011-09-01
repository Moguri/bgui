import sys

# So we can find the bgui module
sys.path.append('../..')

import bgui
import bge

class MySys(bgui.System):
	"""
	A subclass to handle our game specific gui
	"""
	def __init__(self, viewport):
		# Initialize the system
		bgui.System.__init__(self, '../../themes/default')
		
		# viewport = [x, y, width, height]		
		# Use a frame to store all of our widgets
		self.frame = bgui.Frame(self, 'window', border=0, size=viewport[2:], pos=viewport[:2])
		self.frame.colors = [(0, 0, 0, 0)] * 4

		# A themed frame
		self.win = bgui.Frame(self.frame, 'win', size=[0.6, 0.8],
			options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			
		# Create an image to display
		self.win.img = bgui.Image(self.win, 'image', 'img.jpg', size=[.92, .7], pos=[.01, .24],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)
		
		# A button
		self.button = bgui.FrameButton(self.win, 'button', text='Click Me!', size=[.14, .09], pos=[.815, .03],
			options = bgui.BGUI_DEFAULT)
		# Setup an on_click callback for the image
		self.button.on_click = self.on_img_click

		# Add a label
		self.lbl = bgui.Label(self.frame, 'label', text="I'm a label!", pos=[0, 0.9],
			sub_theme='Large', options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
		
		# A couple of progress bars to demonstrate sub themes
		self.progress = bgui.ProgressBar(self.win, "progess", percent=0.0, size=[0.92, 0.06], pos=[.2, 0.17],
											sub_theme="Progress", options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
											
		self.health = bgui.ProgressBar(self.win, "health", percent=0.5, size=[0.92, 0.02], pos=[0, 0.14],
											sub_theme="Health",	options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
			
		# A few TextInput widgets
		self.input = bgui.TextInput(self.win, 'input', "I'm active.", font="myfont.otf", size=[.4, .04], pos=[.04, 0.02],
			input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.input.activate()
		self.input.on_enter_key = self.on_input_enter
		
		self.input2 = bgui.TextInput(self.win, 'input2', "I select all when activated.", size=[.4, .04], pos=[.04, 0.08],
			input_options = bgui.BGUI_INPUT_SELECT_ALL, options = bgui.BGUI_DEFAULT)
		
		# A counter property used for the on_img_click() method
		self.counter = 0
		
		# Create a keymap for keyboard input
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}
		
		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().post_draw.append(self.render)

	def on_input_enter(self, widget):
		self.lbl.text = "You've entered: " + widget.text
		widget.text = "You've locked this widget."
		widget.deactivate()
		widget.frozen = 1
		
	def on_img_click(self, widget):
		print("Click?")
		self.counter += 1
		self.lbl.text = "You've clicked me %d times" % self.counter
		self.progress.percent += .1
		if self.counter % 2 == 1:
			self.win.img.texco = [(1,0), (0,0), (0,1), (1,1)]
		else:
			self.win.img.texco = [(0,0), (1,0), (1,1), (0,1)]
	
	def main(self):
		"""A high-level method to be run every frame"""
		
		# Handle the mouse
		mouse = bge.logic.mouse
		
		pos = list(mouse.position)
		pos[0] *= bge.render.getWindowWidth()
		pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])
		
		# if self.camera.name == 'Camera2':
		# print(self.camera, self.size)
		
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
		
def main(cont):
	own = cont.owner
	mouse = bge.logic.mouse

	if 'sys' not in own:
		ob_list = bge.logic.getCurrentScene().objects
		
		# Setup the viewports
		x = bge.render.getWindowWidth()
		y = bge.render.getWindowHeight()
		
		cam = ob_list['Camera']
		cam.useViewport = True
		cam.setViewport(0, 0, x//2, y)
		
		cam = ob_list['Camera2']
		cam.useViewport = True
		cam.setViewport(x//2, 0, x, y)
	
		# Create our systems and show the mouse
		own['sys'] = MySys([0, 0, 0.5, 1])
		own['sys2'] = MySys([0.5, 0, 0.5, 1])
		mouse.visible = True

	else:
		own['sys'].main()
		own['sys2'].main()
