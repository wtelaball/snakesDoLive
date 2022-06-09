import sys
import cv2 as cv
import gameBoard
import numpy as np
import screeninfo
import time
import genetics

WINDOW_HEIGHT = 300
WINDOW_WIDTH = 300

windows = []

def getScreenSize():
	'''
	get screen size from monitor placed at x=0
	'''

	for m in screeninfo.get_monitors():
		if (m.x == 0):
			return m.width, m.height

	print("cannot capture screen size")
	sys.exit(-1)


def createWindows(numWindows, screenSize):

	i = 0
	j = 0
	k = 0

	for k in range(numWindows):
		windows.append('board%02d' %(k))

		cv.namedWindow('board%02d' %(k), cv.WINDOW_NORMAL)
		cv.moveWindow('board%02d' %(k), i * WINDOW_WIDTH, j * WINDOW_HEIGHT)
		
		#print("window moved to ", i *WINDOW_WIDTH, j * WINDOW_HEIGHT)

		i += 1
		if (i * WINDOW_WIDTH > screenSize[0]):
			i = 0
			j += 1

	#print(windows)
	#input()

def moveWindows(screenSize):
	i = 0
	j = 0

	x, y, w, h = cv.getWindowImageRect(windows[0])

	for k in windows:
		cv.moveWindow(k, i * w, j * h)
		i += 1
		if (i * WINDOW_WIDTH > screenSize[0]):
			i = 0
			j += 1

def getBestSnake(boards):
	best = None
	secondBest = None

	for board in boards:
		if best is None:
			best = board.bestSnake()
		else:
			if board.bestSnake().getScore() > best.getScore():
				best = board.bestSnake()

	if best is not None:

		for board in boards:
			if secondBest is None:
				if secondBest != best:
					secondBest = board.bestSnake()
			else:
				if board.bestSnake() != best:
					if board.bestSnake().getScore() > secondBest.getScore() and board.bestSnake().getScore() <= best.getScore():
						secondBest = board.bestSnake()

	if best.getScore() == 0:
		return None, None


	return best, secondBest


def main(dimension, numBoards = 10, totalGenerations = 10):

	screenSize = getScreenSize()
	print("screen size=", screenSize)

	createWindows(numBoards, screenSize)


	best = None
	secondBest = None

	generations = totalGenerations

	while (generations > 0):

		boards = []

		for i in range(numBoards):
			boards.append(
				gameBoard.gameBoard(
					(dimension[0], dimension[1]), 
					numSnakes = 5, 
					boardName = "board%02d" %i))

		genetics.updateGenetics(boards, best, secondBest)

		running = True
		finished = False
		

		while running and not finished:

			k = 0
			finished = True

			for board in boards:
				board.run()

				screen = board.show()
				cv.imshow('board%02d' %(k), screen)

				finished = finished and board.finished()

				k += 1

			key = cv.waitKey(20)

			if key >= 0:
				key = chr(key).upper()
				if key == 'W':
					running = False
				if key == 'Q':
					running = False
					generations = 0

			moveWindows(screenSize)


		if finished:
			best, secondBest = getBestSnake(boards)
			print(best)
			print(secondBest)

		generations -= 1
		print(totalGenerations - generations)

		time.sleep(0.5)



	cv.destroyAllWindows()



if __name__ == '__main__':
	if len(sys.argv) == 1:
		dimension = (30, 30)
	if len(sys.argv) == 2:
		dimension = (int(sys.argv[1]), int(sys.argv[1]))
	if len(sys.argv) == 3:
		dimension = (int(sys.argv[1]), int(sys.argv[2]))


	main(dimension, 10)
	sys.exit(0)