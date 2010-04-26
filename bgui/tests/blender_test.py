import sys

sys.path.append('../src')

import bgui

def main(cont):
	own = cont.owner

	if 'sys' not in own:
		sys = bgui.System()

		bgui.Widget(sys, 'widget', size=(.5, .5),
				options = bgui.BGUI_CENTERX | bgui.BGUI_CENTERY)

		own['sys'] = sys
	else:
		own['sys'].render()
