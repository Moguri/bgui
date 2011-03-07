# This file is to make Sphinx happy (the module just needs to be imported, not used)

try:
	from bgl import *
except:
	print("Warning: BGL not found!")