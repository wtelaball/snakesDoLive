import numpy as np
import point
import cv2 as cv
from snake import Snake

class gameBoard:

	BOARD_ZOOM = 10
	BOARD_COLOR = (255, 255, 255)
	BOARD_TROPHY_COLOR = (0, 0, 255)
	
	def __init__(self, dimension, numSnakes=1):
		self.width = dimension[1]
		self.height = dimension[0]
		self.board = np.zeros([self.height, self.width])
		self.drawBoard()

		self.trophy = point.Point()

		self.randomizeTrophy()

		self.snakes = []
		for i in range(numSnakes):
			snake = Snake()
			snake.randomizeStartPosition((self.width, self.height), self.trophy.getPos())
			self.snakes.append(snake)
		


	def getDimension(self):
		return self.height, self.width


	def drawBoard(self):
		for i in range(self.width):
			self.board[0, i] = 1
			self.board[self.height - 1, i] = 1

		for j in range(self.height):
			self.board[j, 0] = 1
			self.board[j, self.width - 1] = 1


	def randomizeTrophy(self):
		x = np.random.randint(1, self.width)
		y = np.random.randint(1, self.height)

		self.trophy.setPos(x, y)

		self.board[y, x] = 2

	def show(self):

		img = np.zeros([self.height * self.BOARD_ZOOM + 1, self.width * self.BOARD_ZOOM + 1, 3], dtype=np.uint8)
		x = 0
		y = 0

		for j in range(self.height):
			for i in range(self.width):
				if self.board[j, i] == 1:
					cv.rectangle(img, (x + i * self.BOARD_ZOOM + 1, y + j * self.BOARD_ZOOM + 1), (x + (i + 1) * self.BOARD_ZOOM - 1, y + (j + 1) * self.BOARD_ZOOM - 1), self.BOARD_COLOR, -1)


		# trophy
		i, j = self.trophy.getPos()
		cv.rectangle(img, (x + i * self.BOARD_ZOOM + 1, y + j * self.BOARD_ZOOM + 1), (x + (i + 1) * self.BOARD_ZOOM - 1, y + (j + 1) * self.BOARD_ZOOM - 1), self.BOARD_TROPHY_COLOR, -1)		

		# snake

		for snake in self.snakes:
			i, j = snake.getPos()		
			cv.rectangle(img, (x + i * self.BOARD_ZOOM + 1, y + j * self.BOARD_ZOOM + 1), (x + (i + 1) * self.BOARD_ZOOM - 1, y + (j + 1) * self.BOARD_ZOOM - 1), snake.getColor(), -1)		


		return img

	def run(self):
		for snake in self.snakes:
			snake.control()
			snake.move()


	def collision(self):
		for snake in self.snakes:		
			x, y = snake.getPos()
			print("%d, %d" %(x,y))
			if self.board[y, x] == 1:
				snake.die()

	def finished(self):
		for snake in snakes:
			if snake.isAlive(): return False

		return True

