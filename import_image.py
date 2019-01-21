from tkinter import *

fenetre = Tk()

photo = PhotoImage(file="pics/test.gif")
photo2 = PhotoImage(file="pics/carre.gif")
canvas = Canvas(fenetre, width=photo.width(), height=photo.height(), bg="white")
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack()

fenetre.mainloop()