import sys

sys.path.append('../src')

import bgui
import GameLogic

def main(cont):
	own = cont.owner

	if 'sys' not in own:
		sys = bgui.System()

		bgui.ImageWidget(sys, 'widget', 'retards.jpg', size=[0.75, 0.75],
				options =  bgui.BGUI_CENTERX | bgui.BGUI_CENTERY | bgui.BGUI_DEFUALT)

		own['sys'] = sys
	else:
		GameLogic.getCurrentScene().post_draw = [own['sys'].render]
