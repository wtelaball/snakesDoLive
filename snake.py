import neuralnetwork
import numpy as np

class Snake:

	UP = 0
	LEFT = 1
	DOWN = 2
	RIGHT = 3

	BASE_COLOR = (255, 255, 0)

	SENSOR_NUM = 5

	def __init__(self):

		self.x = 1
		self.y = 1
		self.direction = np.random.randint(self.RIGHT)
		self.color = self.BASE_COLOR
		self.alive = True

		self.sensors = np.zeros([self.SENSOR_NUM])


		# init neuralnetwork
		self.nn = neuralnetwork.NeuralNetwork()
		self.nn.addLayer(self.SENSOR_NUM, 4)
		self.nn.addLayer(4, 3)
		self.nn.addLayer(3, 2)
		self.nn.addLayer(2, 1)

		self.nn.randomWeights()


	def randomizeStartPosition(self, dimension, notEqualToTrophy):

		x = 1
		y = 1

		equal = True

		while equal:
			x = np.random.randint(1, dimension[1])
			y = np.random.randint(1, dimension[0])

			if (x, y) == notEqualToTrophy:
				equal = True
			else:
				equal = False

		self.x = x
		self.y = y


	def move(self):
	
		if self.alive:
			if self.direction == self.UP:
				self.y = self.y - 1
			if self.direction == self.DOWN:
				self.y = self.y + 1
			if self.direction == self.LEFT:
				self.x = self.x - 1
			if self.direction == self.RIGHT:
				self.x = self.x + 1

	def turnLeft(self):
		self.direction +=1
		if self.direction > self.RIGHT:
			self.direction = self.UP

	def turnRight(self):
		self.direction -= 1
		if self.direction < self.UP:
			self.direction = self.RIGHT

	def turnNo(self):
		self.direction = self.direction

	def getPos(self):
		return self.x, self.y

	def setColor(self, color):
		self.color = color

	def getColor(self):
		return self.color


	
	def control(self):

		'''
		calc outputs based on sensor readings
		'''

		if self.alive:
			self.output = self.nn.processInputs(self.sensors)

			if (self.output[0] > 2/3.0):
				self.turnRight()
			elif (self.output[0] < 1/3.0):
				self.turnLeft()
			else:
				self.turnNo()

	def isAlive(self):
		return self.alive

	def die(self):
		self.alive = False
