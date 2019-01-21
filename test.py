#!/usr/bin/env python
# -*-coding:Utf-8 -*

import pickle
from tkinter import *
from collections import OrderedDict

def exit(event):
    fenetre.quit()

mon_fichier = open("puzzle/puzzle3.txt", "r")
contenu = mon_fichier.read()
contenu = contenu.split('\n')

del contenu[0]
del contenu[0]

if contenu[len(contenu) - 1] == '' :
    del contenu[len(contenu) - 1]

puzzle = {}

h_tab = 0
w_tab = 0

for i, elt in enumerate(contenu):
    elt = elt.split()
    h_tab = i
    for n,subElt in enumerate (elt):
        puzzle[i + 1, n + 1] = subElt
        w_tab = n
puzzle = OrderedDict(sorted(puzzle.items(), key=lambda t: t[0]))
for coordonne, valeur in puzzle.items():
    print("{} = {}".format(coordonne,valeur))

w_tab += 1
h_tab += 1

puzzleGoal = {}

size=(w_tab, h_tab)

x=0
y=0
lh=0 #ligne haut
lb=0 #ligne bas
hd=0 #hauteur droite
hl=0 #hauteau gauche
sens='d'
k = 1;
for k in range(size[0]*size[1]):
    if(size[0]-x-hd>1 and sens=='d') :
        puzzleGoal[y,x]= (k + 1) % (size[0]*size[1])
        x+=1
    elif(sens=='b' and y<size[1]-lb) :
        puzzleGoal[y,x]= (k + 1) % (size[0]*size[1])
        y+=1
    elif(sens=='g' and x>=hl):
        puzzleGoal[y,x]= (k + 1) % (size[0]*size[1])
        x-=1
    elif(sens=='h' and y>=lh):
        puzzleGoal[y,x]= (k + 1) % (size[0]*size[1])
        y-=1
    else :
        if(sens=='d'):
            sens='b'
            lh+=1
            puzzleGoal[y,x]= (k + 1) % (size[0]*size[1])
            y+=1
        elif(sens=='b') :
            sens='g'
            hd+=1
            puzzleGoal[y-1,x-1]= (k + 1) % (size[0]*size[1])
            y=size[1]-lb-1
            x=size[0]-hd-2
        elif(sens=='g'):
            sens='h'
            lb+=1
            y=size[1]-lb-1
            x=hl
            puzzleGoal[y,x]= (k + 1) % (size[0]*size[1])
            y-=1
        elif(sens=='h'):
            sens='d'
            hl+=1
            puzzleGoal[x+1,lh]= (k + 1) % (size[0]*size[1])
            x+=2
            y=lh

puzzleGoal = OrderedDict(sorted(puzzleGoal.items(), key=lambda t: t[0]))
for coordonne, valeur in puzzleGoal.items():
    print("{} = {}".format(coordonne,valeur))

print("{}".format(puzzleGoal[0,0]))

print("w_tab = {}, h_tab = {}".format(w_tab, h_tab))

window = 500;

fenetre = Tk()

fenetre['bg']='black'

FrameBase = Frame(fenetre, borderwidth=2, bg='black')
FrameBase.pack(padx=50, pady=50)

FrameInitial = Frame(FrameBase, borderwidth=2, bg='black')
FrameInitial.grid(row=0, column=0, padx=10)

Label(FrameInitial, text="Initial state",bg='black', fg='white', font="Times 20 italic").pack(fill=X)

FramePuzzle = Frame(FrameInitial, borderwidth=2, bg='black')
FramePuzzle.pack(side=BOTTOM)

for coordonne, valeur in puzzle.items():
    print("{} {}".format(coordonne[0], coordonne[1]))
    if int(valeur) == int(puzzleGoal[coordonne[0] - 1, coordonne[1] - 1]) :
        background = 'green'
    else :
        background = 'red'
    canvas = Canvas(FramePuzzle, width=window / w_tab, height=window / h_tab, background=background, highlightthickness=0)
    txt = canvas.create_text((window / w_tab) / 2, (window / h_tab) / 2, text='%s' % (valeur), font="Arial 16 italic", fill="black")
    canvas.grid(row=coordonne[0], column=coordonne[1], padx=1, pady=1, ipadx=0, ipady=0)

FrameGoal = Frame(FrameBase, borderwidth=2, bg='black')
FrameGoal.grid(row=0, column=1, padx=10)

Label(FrameGoal, text="Goal state",bg='black', fg='white', font="Times 20 italic").pack(fill=X)

FramePuzzle2 = Frame(FrameGoal, borderwidth=2, bg='black')
FramePuzzle2.pack(side=BOTTOM)

for coordonne, valeur in puzzleGoal.items():
	background = 'green'
	canvas = Canvas(FramePuzzle2, width=window / w_tab, height=window / h_tab, background=background, highlightthickness=0)
	txt = canvas.create_text((window / w_tab) / 2, (window / h_tab) / 2, text='%s' % (valeur), font="Arial 16 italic", fill="black")
	# canvas.pack()
	canvas.grid(row=coordonne[0], column=coordonne[1], padx=1, pady=1, ipadx=0, ipady=0)

fenetre.bind("<Escape>", exit)

fenetre.mainloop()

fenetre.destroy()