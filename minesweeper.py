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


class Window:
	def __init__(self, board, m, n):
		self.board = board
		self.m, self.n = m, n
		self.root = Tk()
		self.root.geometry('700x700')
		self.frm = ttk.Frame(self.root, padding=10)
		self.createButtons(self.m, self.n)
		self.root.mainloop()


	def createButtons(self, height, width):
		for i in range(width):
			for j in range(height):
				Button(self.root, text='B', height = 1, width = 1).grid(column=i, row=j)


if __name__ == '__main__':
	data = Data(10, 10, 25)
	for i in data.board:
		print(i)
	print(data.bombCoordinates)
	window = Window(data.board, 5, 10)