from tkinter import *
from tkinter import filedialog as filedialog
import os
from PIL import Image
from PIL import ImageTk

class Tiles():
	def __init__(self, rack):
		self.tiles = []
		self.rack = rack

	def add(self, tile):
		self.tiles.append(tile)

	def shuffle(self):
		random.shuffle(self.tiles)
		i = 0
		for row in range(self.rack):
			for col in range(self.rack):
				self.tiles[i].pos = (row,col)
				i+=1

	def show(self):
		for tile in self.tiles:
			tile.show()
				

class Tile(Label):
	def __init__(self, parent, image, pos):
		photo = ImageTk.PhotoImage(image)
		self.Label = Label(image = photo)
		self.Label.image = photo
		self.image = image
		self.pos = pos
		self.curPos = pos

	def show(self):
		print(self.pos)
		self.Label.grid(row = self.pos[1],column = self.pos[0])
		# self.Label.pack()
		

class Board(Frame):
	MAX_BOARD_SIZE = 500
	def __init__(self,parent,image,rack,*args,**kwargs):
		Frame.__init__(self,parent,*args,**kwargs)

		self.parent = parent
		self.rack = rack
		self.image = self.openImage(image)
		self.tileSizeX = self.image.size[0]/self.rack
		self.tileSizeY = self.image.size[1]/self.rack
		self.tiles = self.createTiles()
		# self.tiles.shuffle()
		self.tiles.show()

	def openImage(self, image):
		image = Image.open(image)
		if image.size[0] > self.MAX_BOARD_SIZE:
			image = image.resize((self.MAX_BOARD_SIZE, image.size[1]), Image.ANTIALIAS)
		if image.size[1] > self.MAX_BOARD_SIZE:
			image = image.resize((image.size[0], self.MAX_BOARD_SIZE), Image.ANTIALIAS)
		return image

	def createTiles(self):
		tiles = Tiles(self.rack)
		for row in range(self.rack):
			for col in range(self.rack):
				x0 = row * self.tileSizeX
				y0 = col * self.tileSizeY
				x1 = x0 + self.tileSizeX
				y1 = y0 + self.tileSizeY
				tileImage = self.image.crop((x0,y0,x1,y1))
				tile = Tile(self, tileImage,(row,col))
				tiles.add(tile)
		return tiles

class Main():
	def __init__(self, parent):
		self.parent = parent
		self.image = StringVar()
		self.rack = IntVar()
		self.createWidgets()

	def createWidgets(self):
		self.mainFrame = Frame(self.parent)
		Label(self.mainFrame, text = 'Sliding Puzzle', font=(",50")).pack(padx = 10, pady = 10)
		frame = Frame(self.mainFrame)
		Label(frame,text = 'Image').grid(sticky = W)
		Entry(frame,textvariable = self.image, width = 50).grid(row = 0,column = 1, padx = 10, pady = 10)
		Button(frame,text='Browse',command=self.browse).grid(row = 0,column = 2, pady= 10, padx = 10)
		Label(frame,text = 'rack').grid(sticky = W)
		OptionMenu(frame,self.rack, *[3,4,5,6,7,8,9,10]).grid(row = 1,column = 1, padx = 10, pady = 10, sticky = W)
		frame.pack(padx=10,pady=10)
		Button(self.mainFrame,text='Start',command=self.start).pack(padx=10,pady=10)
		self.mainFrame.pack()
		self.board = Frame(self.parent)
		self.winFrame = Frame(self.parent)

	def start(self):
		image = self.image.get()
		rack = self.rack.get()
		if os.path.exists(image):
			self.board = Board(self.parent, image, rack)
			self.mainFrame.pack_forget()
			self.board.grid()

	def browse(self):
		self.image.set(filedialog.askopenfilename(title="Select Image",filetypes = (("jpeg files","*.gif"),("all files","*.*"))))

if __name__=="__main__":
	print("let's go")
	root = Tk()
	root.wm_title("NPuzzle")
	Main(root)
	root.mainloop()