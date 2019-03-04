from tkinter import *
from tkinter import filedialog as filedialog
import os
from PIL import Image
from PIL import ImageTk
import time
import random
import resolve

class Tiles():
	def __init__(self, rack):
		self.tiles = []
		self.rack = rack
		self.gap = None

	def add(self, tile):
		self.tiles.append(tile)

	def getTile(self, *pos):
		for tile in self.tiles:
			if tile.pos == pos:
				return tile

	def getTileAroundGap(self):
		gRow,gCol = self.gap.pos
		return self.getTile(gRow,gCol - 1), self.getTile(gRow - 1,gCol), self.getTile(gRow ,gCol + 1), self.getTile(gRow + 1,gCol)

	def changeGap(self, tile):
		try:
			gPos = self.gap.pos
			self.gap.pos = tile.pos
			tile.pos = gPos
		except:
			pass

	def slide(self,key):
		left,up,right,down = self.getTileAroundGap()
		if key == 'Up':
			self.changeGap(down)
		if key == 'Down':
			self.changeGap(up)
		if key == 'Left':
			self.changeGap(right)
		if key == 'Right':
			self.changeGap(left)
		self.show()

	def shuffle(self):
		random.shuffle(self.tiles)
		i = 0
		for row in range(self.rack):
			for col in range(self.rack):
				self.tiles[i].pos = (row,col)
				i+=1

	def show(self):
		for tile in self.tiles:
			if self.gap != tile:
				tile.show()

	def setGap(self, index):
		self.gap = self.tiles[index]

	def orderByPuzzle(self, puzzle):
		for cle, valeur in puzzle.items():
			for tile in self.tiles:
				if int(tile.num) == int(valeur):
					tile.pos = cle
		self.show()
					# print("cle:",cle, "valeur", valeur, "tile.num:", tile.num)

				

class Tile(Label):
	def __init__(self, parent, image, pos, num):
		photo = ImageTk.PhotoImage(image)
		self.Label = Label(image = photo)
		self.Label.image = photo
		self.pos = pos
		self.num = num

	def show(self):
		self.Label.grid(row = self.pos[0],column = self.pos[1])

class Board(Frame):
	MAX_BOARD_SIZE = 500
	def __init__(self,parent,image,rack,puzzleGoal,puzzle,*args,**kwargs):
		Frame.__init__(self,parent,*args,**kwargs)

		self.parent = parent
		self.rack = rack
		self.puzzleGoal = puzzleGoal
		self.image = self.openImage(image)
		self.tileSizeX = self.image.size[0]/self.rack
		self.tileSizeY = self.image.size[1]/self.rack
		self.tiles = self.createTiles()
		# self.tiles.orderByPuzzle(puzzle)
		self.tiles.shuffle()
		self.tiles.show()
		self.bindKeys()

	def openImage(self, image):
		image = Image.open(image)
		if image.size[0] > self.MAX_BOARD_SIZE:
			image = image.resize((self.MAX_BOARD_SIZE, image.size[1]), Image.ANTIALIAS)
		if image.size[1] > self.MAX_BOARD_SIZE:
			image = image.resize((image.size[0], self.MAX_BOARD_SIZE), Image.ANTIALIAS)
		return image

	def bindKeys(self):
		self.bind_all('<Key-Up>', self.slide)
		self.bind_all('<Key-Down>', self.slide)
		self.bind_all('<Key-Right>', self.slide)
		self.bind_all('<Key-Left>', self.slide)

	def slide(self,event):
		self.tiles.slide(event.keysym)

	def createTiles(self):
		tiles = Tiles(self.rack)
		for row in range(self.rack):
			for col in range(self.rack):
				x0 = col * self.tileSizeX
				y0 = row * self.tileSizeY
				x1 = x0 + self.tileSizeX
				y1 = y0 + self.tileSizeY
				tileImage = self.image.crop((x0,y0,x1,y1))
				tile = Tile(self, tileImage,(row,col), self.puzzleGoal[row, col])
				tiles.add(tile)
		tiles.setGap(-1)
		return tiles


class Main():
	def __init__(self, parent, size, puzzleGoal, finalList):
		self.parent = parent
		self.image = StringVar()
		self.rack = size
		self.puzzleGoal = puzzleGoal
		self.finalList = finalList
		self.createWidgets()

	def createWidgets(self):
		self.mainFrame = Frame(self.parent)
		Label(self.mainFrame, text = 'Sliding Puzzle', font=(",50")).pack(padx = 10, pady = 10)
		frame = Frame(self.mainFrame)
		Label(frame,text = 'Image').grid(sticky = W)
		Entry(frame,textvariable = self.image, width = 50).grid(row = 0,column = 1, padx = 10, pady = 10)
		Button(frame,text='Browse',command=self.browse).grid(row = 0,column = 2, pady= 10, padx = 10)
		Label(frame,text = 'Size').grid(sticky = W)
		Label(frame, text = self.rack).grid(row = 1,column = 1, padx = 10, pady = 10, sticky = W)
		frame.pack(padx=10,pady=10)
		Button(self.mainFrame,text='Start',command=self.start).pack(padx=10,pady=10)
		self.mainFrame.pack()

	def start(self):
		image = self.image.get()
		if os.path.exists(image):
			self.mainFrame.pack_forget()
			self.board = Board(self.parent, image, self.rack, self.puzzleGoal, self.puzzleGoal)
			self.board.grid()
			# for noeud in self.finalList.noeuds:
			# 	time.sleep(0.5)
			# 	# self.parent.update()
			# 	self.board = Board(self.parent, image, self.rack, self.puzzleGoal, noeud.puzzle)
			# 	# self.board.grid()

	def browse(self):
		self.image.set(filedialog.askopenfilename(title="Select Image",filetypes = (("jpeg files","*.gif"),("all files","*.*"))))

def visual(size,puzzleGoal,finalList):
	root = Tk()
	root.wm_title("NPuzzle")
	Main(root,size,puzzleGoal, finalList)
	root.mainloop()

# visual()