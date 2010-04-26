import sys

sys.path.append('../src')

import bgui
import GameLogic
import Rasterizer

class MySys(bgui.System):
	def __init__(self):
		bgui.System.__init__(self)

		self.img = bgui.Image(self, 'widget', 'retards.jpg', size=[.75, .75],
			options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFUALT)

		self.img.on_click = self.on_img_click

		self.lbl = bgui.Label(self, 'label', "I haz label!", None, 70, pos=[0, .01],
			options = bgui.BGUI_DEFUALT | bgui.BGUI_CENTERX)

		self.counter = 0

	def on_img_click(self, widget):
		self.counter += 1
		self.lbl.text = "You've clicked me %d times" % self.counter

		if self.counter % 2 == 1:
			self.img.update_image('logo.png')
		else:
			self.img.update_image('retards.jpg')

def main(cont):
	own = cont.owner
	mouse = GameLogic.mouse

	if 'sys' not in own:
		own['sys'] = MySys()
		mouse.visible = True

	else:
		pos = [i for i in mouse.position]
		pos[0] *= Rasterizer.getWindowWidth()
		pos[1] = Rasterizer.getWindowHeight() - (Rasterizer.getWindowHeight() * pos[1])
		own['sys'].update_mouse(pos, (189, 1) in mouse.events)
		GameLogic.getCurrentScene().post_draw = [own['sys'].render]
