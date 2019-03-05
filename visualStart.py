from tkinter import *
from tkinter import filedialog as filedialog
import os
# import resolve

class Start():
	def __init__(self, parent):
		self.parent = parent
		self.warning = 0
		self.file = StringVar()
		self.greedy = IntVar()
		self.uniform = IntVar()
		self.manhattan = IntVar()
		self.hamming = IntVar()
		self.linear = IntVar()
		self.heuristique = IntVar()
		self.createWidgets()

	def createWidgets(self):
		self.heuristique.set(3)
		self.greedy.set(1)
		self.uniform.set(0)
		self.mainFrame = Frame(self.parent)
		Label(self.mainFrame, text = 'Choose your file', font=(",50")).pack(padx = 10, pady = 10)
		frame = Frame(self.mainFrame)
		Label(frame,text = 'File').grid(sticky = W)
		Entry(frame,textvariable = self.file, width = 50).grid(row = 0,column = 1, padx = 10, pady = 10)
		Button(frame,text='Browse',command=self.browse).grid(row = 0,column = 2, pady= 10, padx = 10)
		buttons = Frame(frame)
		Label(frame,text = 'Heuristique').grid(row = 1,column = 0,sticky = E)
		Checkbutton(buttons,text="Manhattan",variable=self.manhattan, command=self.updateMan).grid(row = 1,column = 1, padx = 10, pady = 10, sticky = W)
		Checkbutton(buttons,text="Hamming",variable=self.hamming, command=self.updateHam).grid(row = 1,column = 2, padx = 10, pady = 10, sticky = W)
		Checkbutton(buttons,text="Linear",variable=self.linear, command=self.updateLin).grid(row = 1,column = 3, padx = 10, pady = 10, sticky = W)
		buttons.grid(row = 1,column = 1, padx = 10, pady = 10, sticky = W)
		Label(frame,text = 'Mode').grid(row = 2,column = 0,sticky = W)
		buttons2 = Frame(frame)
		Checkbutton(buttons2,text="Greedy Search",variable=self.greedy, command=self.updateGreedy).grid(row = 1,column = 1, padx = 10, pady = 10, sticky = W)
		Checkbutton(buttons2,text="Uniform Cost",variable=self.uniform, command=self.updateUniform).grid(row = 1,column = 2, padx = 10, pady = 10, sticky = W)
		buttons2.grid(row = 2,column = 1, padx = 10, pady = 10, sticky = W)
		frame.pack(padx=10,pady=10)
		Button(self.mainFrame,text='Resolve',command=self.start).pack(padx=10,pady=10)
		self.mainFrame.pack()

	def updateGreedy(self):
		self.uniform.set((self.uniform.get() + 1) % 2)

	def updateUniform(self):
		self.greedy.set((self.greedy.get() + 1) % 2)

	def updateMan(self):
		self.hamming.set(0)
		self.linear.set(0)

	def updateHam(self):
		self.manhattan.set(0)
		self.linear.set(0)

	def updateLin(self):
		self.hamming.set(0)
		self.manhattan.set(0)

	def start(self):
		if self.file.get() == "":
			if self.warning == 0:
				self.warning = 1
				Label(self.mainFrame,text = 'Please select a File before starting',padx = 10, pady = 10, fg = 'red').pack()
		else:
			if self.manhattan.get() == 1:
				self.heuristique.set(2)
			elif self.hamming.get() == 1:
				self.heuristique.set(1)
			else:
				self.heuristique.set(3)
			print("Resolving")
			self.parent.destroy()

	def browse(self):
		self.file.set(filedialog.askopenfilename(title="Select File",filetypes = (("jpeg files","*.txt"),("all files","*.*"))))

def visualStart():
	root = Tk()
	root.wm_title("NPuzzle")
	start = Start(root)
	root.mainloop()
	return(start)