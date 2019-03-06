from tkinter import *
from tkinter import filedialog as filedialog
import os
from PIL import Image
from PIL import ImageTk
import time
import sys

class Tiles():
	def __init__(self, rack):
		self.tiles = []
		self.rack = rack

	def add(self, tile):
		self.tiles.append(tile)

	def show(self, final):
		for tile in self.tiles:
			if int(tile.num) != 0 or final:
				tile.show()

	def orderByPuzzle(self, puzzle):
		for cle, valeur in puzzle.items():
			for tile in self.tiles:
				if int(tile.num) == int(valeur):
					tile.pos = cle

class Tile(Label):
	def __init__(self, parent, image, pos, num):
		photo = ImageTk.PhotoImage(image)
		self.Label = Label(image=photo)
		self.Label.image = photo
		self.pos = pos
		self.num = num

	def show(self):
		self.Label.grid(row = self.pos[0],column = self.pos[1])

class Board(Frame):
	MAX_BOARD_SIZE = 500
	def __init__(self,parent,image,rack,puzzleGoal,finalList, timeSleep,*args,**kwargs):
		Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		self.rack = rack
		self.puzzleGoal = puzzleGoal
		self.finalList = finalList
		self.image = self.openImage(image)
		self.tileSizeX = self.image.size[0]/self.rack
		self.tileSizeY = self.image.size[1]/self.rack
		self.tiles = self.createTiles()
		for noeud in finalList.noeuds:
			self.tiles.orderByPuzzle(noeud.puzzle)
			self.tiles.show(0)
			time.sleep(timeSleep.get()/int(finalList.max))
			parent.update()
		time.sleep(timeSleep.get()/int(finalList.max) * 2)
		self.tiles.show(1)

	def openImage(self, image):
		image = Image.open(image)
		if image.size[0] > self.MAX_BOARD_SIZE:
			image = image.resize((self.MAX_BOARD_SIZE, image.size[1]), Image.ANTIALIAS)
		if image.size[1] > self.MAX_BOARD_SIZE:
			image = image.resize((image.size[0], self.MAX_BOARD_SIZE), Image.ANTIALIAS)
		return image

	def createTiles(self):
		tiles = Tiles(self.rack)
		i = 0
		for row in range(self.rack):
			for col in range(self.rack):
				x0 = row * self.tileSizeX
				y0 = col * self.tileSizeY
				x1 = x0 + self.tileSizeX
				y1 = y0 + self.tileSizeY
				tileImage = self.image.crop((x0,y0,x1,y1))
				tile = Tile(self, tileImage,(row,col), self.puzzleGoal[col, row])
				tiles.add(tile)
				i += 1
		return tiles

class Main():
	def __init__(self, parent, size, puzzleGoal, finalList):
		self.parent = parent
		self.image = StringVar()
		self.rack = size
		self.puzzleGoal = puzzleGoal
		self.finalList = finalList
		self.fini = IntVar()
		self.time = IntVar()
		self.createWidgets()
		self.parent.protocol("WM_DELETE_WINDOW", self.Intercepte)

	def createWidgets(self):
		self.fini.set(1)
		listeOptions = (5, 10, 20, 30, 50)
		self.time.set(listeOptions[0])
		self.mainFrame = Frame(self.parent)
		Label(self.mainFrame, text = 'Choose your image', font=(",50")).pack(padx = 10, pady = 10)
		frame = Frame(self.mainFrame)
		Label(frame,text = 'Image').grid(sticky = W)
		Entry(frame,textvariable = self.image, width = 50).grid(row = 0,column = 1, padx = 10, pady = 10)
		Button(frame,text='Browse',command=self.browse).grid(row = 0,column = 2, pady= 10, padx = 10)
		Label(frame,text = 'Size').grid(sticky = W)
		Label(frame, text = self.rack).grid(row = 1,column = 1, padx = 10, pady = 10, sticky = W)
		Label(frame,text = 'Time').grid(sticky = W)
		OptionMenu(frame, self.time, *listeOptions).grid(row = 2,column = 1, padx = 10, pady = 10, sticky = W)
		frame.pack(padx=10,pady=10)
		Button(self.mainFrame,text='Start',command=self.start).pack(padx=10,pady=10)
		self.mainFrame.pack()

	def start(self):
		image = self.image.get()
		self.fini.set(0)
		if os.path.exists(image):
			self.mainFrame.pack_forget()
			self.board = Board(self.parent, image, self.rack, self.puzzleGoal, self.finalList, self.time)
			self.board.grid()
			self.fini.set(1)

	def browse(self):
		self.image.set(filedialog.askopenfilename(title="Select Image",filetypes = (("jpeg files","*.gif"),("all files","*.*"))))

	def Intercepte(self):
		if self.fini.get() == 0:
	   		print("Wait !")
		else:
		   	self.parent.destroy()
		   	return

def visualFinal(size,puzzleGoal,finalList):
	root = Tk()
	root.wm_title("NPuzzle")
	Main(root,size,puzzleGoal, finalList)
	root.mainloop()