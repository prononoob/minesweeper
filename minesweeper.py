from random import randint


class Data:
	def __init__(self, height=10, width=10, bombs=15):
		self.height, self.width, self.bombs = height, width, bombs
		self.board = []

		for i in range(self.height):
			self.board.append([])
			for j in range(self.width):
				self.board[i].append(0)

		self.bombCoordinates = []
		for i in range(self.bombs):
			self.cords = [randint(0, self.height-1), randint(0, self.width-1)]
			while self.cords in self.bombCoordinates:
				self.cords = [randint(0, self.height-1), randint(0, self.width-1)]
			self.bombCoordinates.append(self.cords)

		for i in self.bombCoordinates:
			self.board[i[0]][i[1]] = 1




if __name__ == '__main__':
	data = Data(10, 10, 25)
	for i in data.board:
		print(i)
	print(data.bombCoordinates)