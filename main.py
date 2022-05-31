import sys
import cv2 as cv
import gameBoard
import numpy as np

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500

def createWindows(numWindows = 10):

	i = 0
	j = 0
	k = 0

	while (numWindows > 0):
		cv.namedWindow('snakes%02d' %(k))
		cv.moveWindow('snakes%02d' %(k), i * WINDOW_WIDTH, j * WINDOW_HEIGHT)
		i += 1
		if (i > 4):
			i = 0
			j += 1
		k += 1

		numWindows -= 1

def main(dimension, numBoards = 10):
	createWindows()
	boards = []

	for i in range(numBoards):
		boards.append(gameBoard.gameBoard((dimension[0], dimension[1])))

	running = True

	while running:

		k = 0

		for board in boards:
			board.run()
			board.collision()

			screen = board.show()
			cv.imshow('snakes%02d' %(k), screen)

			k += 1

		key = cv.waitKey(20)
		if key >= 0:
			key = chr(key).upper()
			if key == 'Q':
				running = False





if __name__ == '__main__':
	if len(sys.argv) == 1:
		dimension = (30, 30)
	if len(sys.argv) == 2:
		dimension = (int(sys.argv[1]), int(sys.argv[1]))
	if len(sys.argv) == 3:
		dimension = (int(sys.argv[1]), int(sys.argv[2]))


	main(dimension)
	sys.exit(0)