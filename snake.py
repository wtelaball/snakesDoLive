import neuralnetwork
import numpy as np
import math
import tools
import time

class Snake:

	UP = 0
	LEFT = 1
	DOWN = 2
	RIGHT = 3

	BASE_COLOR = (255, 255, 0)

	SENSOR_NUM = 8

	SNAKE_MAX_STUCK = 2

	def __init__(self, name = "snake"):

		self.x = 1
		self.y = 1
		self.direction = np.random.randint(self.RIGHT)
		self.color = self.BASE_COLOR
		self.alive = True

		self.sensors = np.zeros([self.SENSOR_NUM])


		# init neuralnetwork
		self.nn = neuralnetwork.NeuralNetwork()
		self.nn.addLayer(self.SENSOR_NUM, 10)
		self.nn.addLayer(10, 10)
		self.nn.addLayer(10, 3)
		#self.nn.addLayer(2, 1)

		self.nn.randomWeights()

		# timer
		self.distanceToTrophy = 1000
		self.minDistanceToTrophy = 1000
		self.lastSensorUpdate = time.time()


		self.score = 0

		self.name = name

	def __str__(self):
		return self.name

	def randomizeStartPosition(self, width, height, notEqualToTrophy):

		x = 1
		y = 1

		equal = True

		while equal:
			x = np.random.randint(1, width)
			y = np.random.randint(1, height)

			if (x, y) == notEqualToTrophy:
				equal = True
			else:
				equal = False

		self.x = x
		self.y = y


	def move(self, width, height):


		if self.alive:
			if self.direction == self.UP:
				self.y = self.y - 1
			if self.direction == self.DOWN:
				self.y = self.y + 1
			if self.direction == self.LEFT:
				self.x = self.x - 1
			if self.direction == self.RIGHT:
				self.x = self.x + 1

			# out of limits
			if self.y<0 or self.y>=height or self.x<0 or self.x>=width:
				self.die()


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

			maximo = max(self.output)

			if maximo == self.output[0]:
				self.turnRight()
			elif maximo == self.output[1]:
				self.turnLeft()
			else:
				self.turnNo()

		
	def isAlive(self):
		return self.alive

	def die(self):
		self.alive = False
		self.stuckCounter = 0

	def mdistance(self, x1, y1, x2, y2):
		return abs(x1-x2) + abs(y1 - y2)

	def distance(self, board, direction):

		if direction == self.UP:
			dx = 0
			dy = -1
		
		if direction == self.DOWN:
			dx = 0
			dy = 1
		
		if direction == self.RIGHT:
			dx = 1
			dy = 0
		
		if direction == self.LEFT:
			dx = -1
			dy = 0

		x,y = self.getPos()
		
		distance = 0

		while True:
			x += dx
			y += dy

			if y < 0: break
			if y >= board.shape[0]: break
			if x < 0: break
			if x >= board.shape[1]: break

			if board[y, x] == 1: break

			distance += 1

		return distance

	def updateSensor(self, board, trophy):

		if self.alive:

			maxDistance = math.sqrt(board.shape[0] ** 2 + board.shape[1] ** 2)

			self.sensors[0] = self.distance(board, self.UP) / maxDistance
			self.sensors[1] = self.distance(board, self.LEFT) / maxDistance
			self.sensors[2] = self.distance(board, self.DOWN) / maxDistance
			self.sensors[3] = self.distance(board, self.RIGHT) / maxDistance

			tx, ty = trophy.getPos()
			x, y = self.getPos()

			w = board.shape[1]
			h = board.shape[0]

			self.sensors[4] = self.mdistance(x, y-1, tx, ty) / maxDistance
			self.sensors[5] = self.mdistance(x-1, y, tx, ty) / maxDistance
			self.sensors[6] = self.mdistance(x, y+1, tx, ty) / maxDistance
			self.sensors[7] = self.mdistance(x+1, y, tx, ty) / maxDistance


			self.distanceToTrophy = tools.distance(x, y, tx, ty)

			if (self.distanceToTrophy < self.minDistanceToTrophy):
				self.minDistanceToTrophy = self.distanceToTrophy

				self.stuckCounter = self.SNAKE_MAX_STUCK
			else:
				if (time.time() - self.lastSensorUpdate) >= 1.0:
					self.stuckCounter -= 1
					self.lastSensorUpdate = time.time()

					if self.stuckCounter == 0:
						self.die()



			#print(self.sensors)


	def collision(self, board):
	
		if self.alive:
			x, y = self.getPos()

			if board[y, x] == 1:
				self.die()

	def reachedTrophy(self, board, trophy):
		x, y = self.getPos()

		if self.alive:
			if board[y, x] == 2:
				self.score = self.score + 1
				return True

		return False


	def getGenotype(self):
		'''
		get features of this individual
		'''

		return self.nn.getWeights()

	def setGenotype(self, w):
		'''
		set features of this individual
		'''
		self.nn.setWeights(w)


	def getScore(self):
		return self.score