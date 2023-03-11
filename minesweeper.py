from random import randint
from tkinter import *
from tkinter import ttk


class Data:
	def __init__(self, height=10, width=10, bombs=15):
		self.height, self.width, self.bombs = height, width, bombs
		self.board = []

		# Generate a board filled with 0
		for i in range(self.height):
			self.board.append([])
			for j in range(self.width):
				self.board[i].append(0)

		# Generate bomb coordinates
		self.bombCoordinates = []
		for i in range(self.bombs):
			self.cords = [randint(0, self.height-1), randint(0, self.width-1)]
			while self.cords in self.bombCoordinates:
				self.cords = [randint(0, self.height-1), randint(0, self.width-1)]
			self.bombCoordinates.append(self.cords)

		# Place 1 in place of 0 in self.board using self.bombCoordinates
		for i in self.bombCoordinates:
			self.board[i[0]][i[1]] = 1

		for i in self.board:
			print(i)

		self.boardWithBombCounter = [[x for x in range(self.width)][:] for y in range(self.height)]
		for i in range(len(self.boardWithBombCounter)):
			for j in range(len(self.boardWithBombCounter[0])):
				self.boardWithBombCounter[i][j] = self.checkHowManyBombsAround(i, j)

		print()

		for i in self.boardWithBombCounter:
			print(i)

	def checkHowManyBombsAround(self, x, y) -> int:
		self.x, self.y = x, y
		self.UpRight, self.UpLeft, self.DownRight, self.DownLeft = 0, 0, 0, 0
		self.directions = [self.UpRight, self.UpLeft, self.DownRight, self.DownLeft]
		self.counter = 0
		if self.board[self.x][self.y] == 0:
			if self.x < len(self.board)-1:
				if self.board[self.x+1][self.y] == 1:
					self.counter += 1
				self.DownLeft += 1
				self.DownRight += 1
			if self.x > 0:
				if self.board[self.x-1][self.y] == 1:
					self.counter += 1
				self.UpLeft += 1
				self.UpRight += 1
			if self.y < len(self.board[0])-1:
				if self.board[self.x][self.y+1] == 1:
					self.counter += 1
				self.UpRight += 1
				self.DownRight += 1
			if self.y > 0:
				if self.board[self.x][self.y-1] == 1:
					self.counter += 1
				self.UpLeft += 1
				self.DownLeft += 1
			if self.UpRight == 2:
				if self.board[self.x-1][self.y+1] == 1:
					self.counter += 1
			if self.DownRight == 2:
				if self.board[self.x+1][self.y+1] == 1:
					self.counter += 1
			if self.UpLeft == 2:
				if self.board[self.x-1][self.y-1] == 1:
					self.counter += 1
			if self.DownLeft == 2:
				if self.board[self.x+1][self.y-1] == 1:
					self.counter += 1
		else:
			self.counter = 9
		return self.counter



class ButtonProperties:
	
	# DISABLE BUTTON:
	# 	button['state'] = DISABLED
	#	may need a name!!

	def __init__(self, sRoot, x, y):
		self.x, self.y, self.sRoot = x, y, sRoot
		self.button = Button(self.sRoot.root, height = 1, width = 1, command=self.bombAction)
		self.button.grid(column=self.x, row=self.y)

	def getVal(self):
		print(self.y, 'x', self.x, '=', self.sRoot.data.board[self.y][self.x])
		self.button['text'] = self.isBomb()

	def isBomb(self) -> str:
		return str(self.sRoot.data.board[self.y][self.x])

	def bombAction(self):
		# IF CLICKED ON A BOMB
		if int(self.isBomb()):
			print('-    GAME OVER    -')
			for i in range(self.sRoot.width):
				for j in range(self.sRoot.height):
					globals()['field%sx%s'%(i, j)].button['text'] = globals()['field%sx%s'%(i, j)].isBomb()
					globals()['field%sx%s'%(i, j)].button['command'] = lambda: print('Game ended')
		# IF CLICKED ON AN EMPTY FIELD
		else:
			print('empty!')

class Window:
	def __init__(self):
		self.root = Tk()
		self.root.geometry('100x150')
		self.chooseDifficulty()
		self.root.mainloop()


	def chooseDifficulty(self):
		self.easy = Button(self.root, text='Easy', height=2, width=7, command=lambda: self.createButtons(8, 8, 10))
		self.easy.grid(column=1, row=1, padx=11, pady=5)
		self.medium = Button(self.root, text='Medium', height=2, width=7, command=lambda: self.createButtons(16, 16, 40))
		self.medium.grid(column=1, row=2, pady=5)
		self.hard = Button(self.root, text='Hard', height=2, width=7, command=lambda: self.createButtons(16, 30, 99))
		self.hard.grid(column=1, row=3)


	def destroySelfMenuButtons(self):
		self.easy.destroy()
		self.medium.destroy()
		self.hard.destroy()


	def createButtons(self, height, width, bombs):
		self.height, self.width, self.bombs = height, width, bombs

		# Set screen size fitting to the difficulty
		if self.height == 8 and self.width == 8 and self.bombs == 10:
			self.root.geometry('280x225')
			self.destroySelfMenuButtons()
		elif self.height == 16 and self.width == 16 and self.bombs == 40:
			self.root.geometry('565x450')
			self.destroySelfMenuButtons()
		elif self.height == 16 and self.width == 30 and self.bombs == 99:
			self.root.geometry('1055x450')
			self.destroySelfMenuButtons()

		# Create buttons on the grid
		self.data = Data(self.height, self.width, self.bombs)
		for i in range(self.width):
			for j in range(self.height):
				globals()['field%sx%s'%(i, j)] = ButtonProperties(self, i, j)

		#	CHANGING PROPERTIES OF A BUTTON
		'''for i in range(self.width):
			for j in range(self.height):
				if (i+j)%2 == 0:
					globals()['field%sx%s'%(i, j)].button['command'] = lambda: print('nuttin')
					globals()['field%sx%s'%(i, j)].button['text'] = '0' '''


if __name__ == '__main__':
	# data = Data(10, 10, 25)
	# for i in data.board:
	# 	print(i)
	# print(data.bombCoordinates)
	window = Window()
