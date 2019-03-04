from Tkinter import * 
from time import * 
 
def initialize(title = 'MonApplication'):
  global app
  app = Tk()
  app.title(title)
  app.geometry('640x500')
 
  #Canvas
  global can
  # can = Label(app,text = 'Appuyer sur N pour demarrer')
  can = Canvas(app, width = 640, height = 480, bg = 'green')
  can.pack()
 
  #Label
  new = Label(app,text = 'Appuyer sur N pour demarrer')
  new.pack()
 
  #Evenement
  app.bind_all('<n>',Nouveau)
  app.bind_all('<q>',Quit)

  global x,y
  x , y = 50, 50
 
def Nouveau(event): #Quand on appui sur N
  Animate()
 
 
 
 
def affiche(x,y):
  drawcircle(x,y,30)
  can.update()
 
def drawcircle(x,y,rad):
  global boule
  # boule = can.create_oval(x-rad, y-rad, x+rad, y+rad,fill = 'red')photo = PhotoImage(file="pics/test.gif")
  photo = PhotoImage(file="pics/test.gif")
  photo.crop(10,10)
  boule = can.create_image(x, y, photo)
 
def Animate():
  global dx,dy #Les directions
  global x,y 
  dx,dy = 1,1
 
  while 1:
    x = x+ (dx* 10)
    y = y+ (dy*10)
 
    if x > 610:
      dx = -dx
    if x < 30:
      dx = -dx
    if y >450:
      dy = -dy
    if y<30:
      dy = -dy
 
    can.after(30,affiche(x,y))
    can.delete(boule)
 
 
def Quit(event):
  app.destroy()
 
 
#Le main
initialize('Une balle qui rebondit')
app.mainloop()
app.destroy()