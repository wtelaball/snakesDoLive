class Point:

	'''
	The point object is just a point object for handling (x,y) coordinates 
	'''

	def __init__(self, x = 0, y = 0):
		self.x = int(x)
		self.y = int(y)

	def getPos(self):
		return self.x, self.y

	def setPos(self, x, y):
		self.x = int(x)
		self.y = int(y)


	def __str__(self):
		return "(%d,%d)" %(self.x, self.y)
