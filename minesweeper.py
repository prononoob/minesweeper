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
			while self.cords in self.bombCoordinates or self.cords == [0, 0]:
				self.cords = [randint(0, self.height-1), randint(0, self.width-1)]
			self.bombCoordinates.append(self.cords)

		# Place 1 in place of 0 in self.board using self.bombCoordinates
		for i in self.bombCoordinates:
			self.board[i[0]][i[1]] = 1

		for i in self.board:
			print(i)

	# THIS HAS TO BE DONE AFTER TRANSFORMATION
	# Generate a board with fields saying
	# how many bombs are around
	def generateBoardWithBombCounter(self):
		self.boardWithBombCounter = [[x for x in range(self.width)][:] for y in range(self.height)]
		for i in range(len(self.boardWithBombCounter)):
			for j in range(len(self.boardWithBombCounter[0])):
				self.boardWithBombCounter[i][j] = self.checkHowManyBombsAround(i, j)
		
		print()
		for i in self.boardWithBombCounter:
			print(i)

	# If first click was on a bomb
	# this method transform the board
	# so that the click was on an empty field
	def transformBoard(self, clickVals: list):
		print(clickVals)
		self.copyBoard = [i[:] for i in self.board]
		self.clickVals = clickVals
		for y in range(len(self.board)):
			for x in range(len(self.board[0])):
				self.newXY = self.makeCords(x, y)
				self.board[y][x] = self.copyBoard[self.newXY[1]][self.newXY[0]]
		del self.clickVals, self.copyBoard
		for i in self.board:
			print(i)

	def makeCords(self, oldX, oldY) -> list:
		self.newX = oldX-self.clickVals[0]
		self.newY = oldY-self.clickVals[1]
		return [self.newX, self.newY]

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
		self.button = Button(self.sRoot.mineField, height = 1, width = 1, command=self.fieldAction)
		self.button.grid(column=self.x, row=self.y)

	def getVals(self) -> list:
		return[self.x, self.y]

	def isBomb(self) -> str:
		return str(self.sRoot.data.board[self.y][self.x])

	def fieldAction(self):

		# IF CLICKED ON A BOMB
		if int(self.isBomb()):
			if self.sRoot.firstClick and not self.sRoot.isFlag.get():
				self.sRoot.firstClick = False
				self.sRoot.data.transformBoard(self.getVals())
			else:
				if (globals()['field%sx%s'%(self.x, self.y)].button['bg'] == '#c9c9c9'
					and not globals()['field%sx%s'%(self.x, self.y)].isBomb()):
					print('flagged, cant reveal')
				if self.sRoot.isFlag.get():
					self.changeFlag()
				elif globals()['field%sx%s'%(self.x, self.y)].button['bg'] != '#c9c9c9':
					if not self.sRoot.isFlag.get():
						print('-    GAME OVER    -')
						self.boardReveal()
						
			
		# IF CLICKED ON AN EMPTY FIELD
		else:
			if self.sRoot.firstClick and not self.sRoot.isFlag.get():
				self.sRoot.firstClick = False
			if self.sRoot.isFlag.get():
				self.changeFlag()
			else:
				if globals()['field%sx%s'%(self.x, self.y)].button['bg'] != '#c9c9c9':
					globals()['field%sx%s'%(self.x, self.y)].button['bg'] = '#a9a9a9'
					globals()['field%sx%s'%(self.x, self.y)].button['state'] = DISABLED
			print('empty!')

	def changeFlag(self):
		if globals()['field%sx%s'%(self.x, self.y)].button['bg'] != '#c9c9c9':
			globals()['field%sx%s'%(self.x, self.y)].button['bg'] = '#c9c9c9'
			globals()['field%sx%s'%(self.x, self.y)].button['text'] = '?'
		else:
			globals()['field%sx%s'%(self.x, self.y)].button['bg'] = '#d9d9d9'
			globals()['field%sx%s'%(self.x, self.y)].button['text'] = ''

	def boardReveal(self):
		for i in range(self.sRoot.width):
			for j in range(self.sRoot.height):
				if int(globals()['field%sx%s'%(i, j)].isBomb()):
					globals()['field%sx%s'%(i, j)].button['text'] = 'X'
				else:
					globals()['field%sx%s'%(i, j)].button['bg'] = '#a9a9a9'
					globals()['field%sx%s'%(i, j)].button['state'] = DISABLED
				globals()['field%sx%s'%(i, j)].button['command'] = lambda: print('Game ended')


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


	def createFrames(self, height, width):
		self.mineField = Frame(self.root, height=height, width=width)
		self.mineField.grid(column=0, row=0)
		self.switchFrame = Frame(self.root, height=40, width=width)
		self.switchFrame.grid(column=0, row=1)
		self.isFlag = BooleanVar(value=False)
		Radiobutton(self.switchFrame, text='Reveal', variable=self.isFlag, value=False).pack()
		Radiobutton(self.switchFrame, text='Flag', variable=self.isFlag, value=True).pack()



	def createButtons(self, height, width, bombs):
		self.height, self.width, self.bombs = height, width, bombs

		# Set screen size fitting to the difficulty
		if self.height == 8 and self.width == 8 and self.bombs == 10:
			self.root.geometry('280x265')
			self.destroySelfMenuButtons()
			self.createFrames(225, 280)
		elif self.height == 16 and self.width == 16 and self.bombs == 40:
			self.root.geometry('565x490')
			self.destroySelfMenuButtons()
			self.createFrames(450, 565)
		elif self.height == 16 and self.width == 30 and self.bombs == 99:
			self.root.geometry('1055x490')
			self.destroySelfMenuButtons()
			self.createFrames(450, 1055)

		# Create buttons on the grid
		self.data = Data(self.height, self.width, self.bombs)
		for i in range(self.width):
			for j in range(self.height):
				globals()['field%sx%s'%(i, j)] = ButtonProperties(self, i, j)
		self.firstClick = True

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
