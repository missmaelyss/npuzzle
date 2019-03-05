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
		self.manhattan = IntVar()
		self.hamming = IntVar()
		self.linear = IntVar()
		self.heuristique = 3
		self.createWidgets()

	def createWidgets(self):
		self.mainFrame = Frame(self.parent)
		Label(self.mainFrame, text = 'Choose your file', font=(",50")).pack(padx = 10, pady = 10)
		frame = Frame(self.mainFrame)
		Label(frame,text = 'File').grid(sticky = W)
		Entry(frame,textvariable = self.file, width = 50).grid(row = 0,column = 1, padx = 10, pady = 10)
		Button(frame,text='Browse',command=self.browse).grid(row = 0,column = 2, pady= 10, padx = 10)
		buttons = Frame(frame)
		Label(frame,text = 'Heuristique').grid(row = 1,column = 0,sticky = W)
		Checkbutton(buttons,text="Manhattan",variable=self.manhattan, command=self.updateMan).grid(row = 1,column = 1, padx = 10, pady = 10, sticky = W)
		Checkbutton(buttons,text="Hamming",variable=self.hamming, command=self.updateHam).grid(row = 1,column = 2, padx = 10, pady = 10, sticky = W)
		Checkbutton(buttons,text="Linear",variable=self.linear, command=self.updateLin).grid(row = 1,column = 3, padx = 10, pady = 10, sticky = W)
		buttons.grid(row = 1,column = 1, padx = 10, pady = 10, sticky = E)
		Label(frame,text = 'Greedy').grid(row = 2,column = 0,sticky = W)
		Checkbutton(frame,variable=self.greedy).grid(row = 2,column = 1, padx = 10, pady = 10, sticky = E)
		frame.pack(padx=10,pady=10)
		Button(self.mainFrame,text='Resolve',command=self.start).pack()
		self.mainFrame.pack()

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
				self.heuristique = 2
			elif self.hamming.get() == 1:
				self.heuristique = 1
			else:
				self.heuristique = 3
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