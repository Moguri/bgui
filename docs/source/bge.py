# This file is to make Sphinx happy (the module just needs to be imported, not used)

texture = None

try:
	from bge import *
except:
	print("Warning: BLF not found!")