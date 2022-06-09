import numpy as np
import point
import cv2 as cv
from snake import Snake

class gameBoard:

	BOARD_ZOOM = 10
	BOARD_COLOR = (255, 255, 255)
	BOARD_TROPHY_COLOR = (0, 0, 255)


	FONT_SCALE = 0.5
	FONT_COLOR = (0, 255, 0)
	
	def __init__(self, dimension, numSnakes=1, boardName="board"):
		self.width = dimension[1]
		self.height = dimension[0]
		self.board = np.zeros([self.height, self.width])
		self.name = boardName
		self.drawBoard()

		self.trophy = point.Point(-1, -1)

		self.randomizeTrophy()

		self.snakes = []
		x, y = (1, 1)

		for i in range(numSnakes):
			snake = Snake(name = boardName + "_snake%02d" %i)
			if i == 0:
				snake.randomizeStartPosition(width = self.width, height = self.height, notEqualToTrophy = self.trophy.getPos())
				x, y = snake.getPos()
			else:
				snake.setPos(x, y)

			self.snakes.append(snake)
		
	def __str__(self):
		return self.name

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
		oldx, oldy = self.trophy.getPos()

		if oldx != -1 and oldy != -1:
			self.board[oldy, oldx] = 0

		x = np.random.randint(1, self.width)
		y = np.random.randint(1, self.height)

		self.trophy.setPos(x, y)

		self.board[y, x] = 2

	def show(self):

		img = np.zeros([self.height * self.BOARD_ZOOM + 1, self.width * self.BOARD_ZOOM + 1, 3], dtype=np.uint8)

		# draw board

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
			if snake.isAlive():
				i, j = snake.getPos()		
				cv.rectangle(img, (x + i * self.BOARD_ZOOM + 1, y + j * self.BOARD_ZOOM + 1), (x + (i + 1) * self.BOARD_ZOOM - 1, y + (j + 1) * self.BOARD_ZOOM - 1), snake.getColor(), -1)		

		# data

		posy = 20
		x = 10
		font = cv.FONT_HERSHEY_SIMPLEX
		FONT_SCALE = 0.5

		for snake in self.snakes:
			text = "d=%.2f md=%.2f t=%d sc=%d" %(snake.distanceToTrophy, snake.minDistanceToTrophy, snake.stuckCounter, snake.getScore())
			cv.putText(img, text, (x, posy), font, FONT_SCALE, self.FONT_COLOR, 1, cv.LINE_AA)
			posy = posy + 20



		return img

	def run(self):
		for snake in self.snakes:
			snake.control()
			snake.move(width = self.width, height = self.height)
			snake.updateSensor(self.board, self.trophy)
			snake.collision(self.board)
			if snake.reachedTrophy(self.board, self.trophy):
				self.randomizeTrophy()


	def finished(self):
		for snake in self.snakes:
			if snake.isAlive(): return False

		return True


	def bestSnake(self):
		best = None

		for snake in self.snakes:
			if best is None:
				best = snake
			else:
				if snake.getScore() > best.getScore():
					best = snake

		return best


	def getNumSnakes(self):
		return len(self.snakes)

	def getSnakes(self):
		return self.snakes