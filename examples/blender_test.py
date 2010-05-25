import sys

# So we can find the bgui module
sys.path.append('..')

import bgui
import GameLogic
import Rasterizer

class MySys(bgui.System):
	"""
	A subclass to handle our game specific gui
	"""
	def __init__(self):
		# Initiate the system
		bgui.System.__init__(self)
		
		# Use a frame to store all of our widgets
		self.frame = bgui.Frame(self, 'window')#options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERED)

		# Create an image to display
		self.img = bgui.Image(self.frame, 'widget', 'img.jpg', size=[.75, .75],
			options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

		# Setup an on_click callback for the image
		self.img.on_click = self.on_img_click

		# Add a label
		self.lbl = bgui.Label(self.img, 'label', "I'm a label!", 'myfont.otf', 70, pos=[0, 1.1],
			options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

		# A counter property used for the on_img_click() method
		self.counter = 0

	def on_img_click(self, widget):
		self.counter += 1
		self.lbl.text = "You've clicked me %d times" % self.counter

		if self.counter % 2 == 1:
			self.img.update_image('img_flipped.png')
		else:
			self.img.update_image('img.jpg')

def main(cont):
	own = cont.owner
	mouse = GameLogic.mouse

	if 'sys' not in own:
		# Create our system and show the mouse
		own['sys'] = MySys()
		mouse.visible = True

	else:
		# Send mouse data to the system and draw it using the scene's post_draw callback
		pos = [i for i in mouse.position]
		pos[0] *= Rasterizer.getWindowWidth()
		pos[1] = Rasterizer.getWindowHeight() - (Rasterizer.getWindowHeight() * pos[1])
		own['sys'].update_mouse(pos, (189, 1) in mouse.events)
		GameLogic.getCurrentScene().post_draw = [own['sys'].render]
