# This file is to make Sphinx happy (the module just needs to be imported, not used)

GL_NEAREST = None
GL_LINEAR = None

try:
	from bgl import *
except:
	print("Warning: BGL not found!")