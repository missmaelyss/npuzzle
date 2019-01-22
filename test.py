#!/usr/bin/env python
# -*-coding:Utf-8 -*

import pickle
from tkinter import *
from collections import OrderedDict

def exit(event):
    fenetre.quit()

mon_fichier = open("puzzle/puzzle5.txt", "r")
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

window = 200;

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
    if int(valeur) == 0:
        background = 'black'
    elif int(valeur) == int(puzzleGoal[coordonne[0] - 1, coordonne[1] - 1]) :
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
    if int(valeur) == 0:
        background = 'black'
    else:
        background = 'green'
    canvas = Canvas(FramePuzzle2, width=window / w_tab, height=window / h_tab, background=background, highlightthickness=0)
    txt = canvas.create_text((window / w_tab) / 2, (window / h_tab) / 2, text='%s' % (valeur), font="Arial 16 italic", fill="black")
	# canvas.pack()
    canvas.grid(row=coordonne[0], column=coordonne[1], padx=1, pady=1, ipadx=0, ipady=0)

fenetre.bind("<Escape>", exit)

# fenetre.mainloop()

# fenetre.destroy()

#algo de resolution

class Noeud:
    """docstring for Noeud"""
    def __init__(self, puzzle, cout, heuristique):
        self.puzzle = puzzle
        self.cout = cout
        self.heuristique = heuristique
        

class File:

    def __init__(self):
        self.noeuds = []    # creates a new empty list

    def ajouter(self, noeud):
        self.noeuds.append(noeud)

    def depiler(self):
        n = 0
        while self.noeuds[n] :
            n += 1
        return self.noeuds[n]



def compare2Noeuds(n1, n2):
    if n1.heuristique < n2.heuristique :
        return 1
    elif n1.heuristique == n2.heuristique :
        return 0
    else :
        return -1

def heuristique(puzzle, puzzleGoal):
    commun = 0;
    items = 0;
    for coordonne, valeur in puzzle.items():
        items += 1
        if int(valeur) == int(puzzleGoal[coordonne[0] - 1, coordonne[1] - 1]):
            commun += 1
    return items - commun

def createVoisin(noeud, oldPos0, newPos0):
    print("{} {}".format(oldPos0, newPos0))
    voisin = Noeud(noeud.puzzle, noeud.cout + 1, noeud.heuristique)
    print("{}".format(findCoordonne0(voisin.puzzle)))
    tmp = voisin.puzzle[oldPos0]
    voisin.puzzle[oldPos0] = voisin.puzzle[newPos0]
    voisin.puzzle[newPos0] = tmp
    print("ICI coordonne0 = {}".format(findCoordonne0(voisin.puzzle)))
    return voisin

def printPuzzle():
    return

def findCoordonne0(puzzle):
    for cle, valeur in puzzle.items():
        if int(valeur) == 0:
            return cle

def voisins(noeud):
    voisins = []
    coordonne0 = (-1,-1);
    coordonneMax = (-1,-1);
    for cle, valeur in noeud.puzzle.items():
        if int(valeur) == 0:
            coordonne0 = cle
        coordonneMax = cle
    # if coordonne0[1] > 1:
    #     voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] - 1)))
    if coordonne0[1] < coordonneMax[1]:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] + 1)))
    if coordonne0[0] > 1:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] - 1, coordonne0[1])))
    if coordonne0[0] < coordonneMax[0]:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] + 1, coordonne0[1])))
    # FrameVoisin = Frame(fenetre, borderwidth=2, bg='black')
    # FrameVoisin.pack(side=LEFT)
    # for noeud in voisins:
    #     print("coordonne0 = {}".format(findCoordonne0(noeud.puzzle)))
    #     for coordonne, valeur in noeud.puzzle.items():
    #         if int(valeur) == 0:
    #             background = 'black'
    #         elif int(valeur) == int(puzzleGoal[coordonne[0] - 1, coordonne[1] - 1]) :
    #             background = 'green'
    #         else :
    #             background = 'red'
    #         canvas = Canvas(FrameVoisin, width=window / w_tab, height=window / h_tab, background=background, highlightthickness=0)
    #         txt = canvas.create_text((window / w_tab) / 2, (window / h_tab) / 2, text='%s' % (valeur), font="Arial 16 italic", fill="black")
    #         canvas.grid(row= coordonne[0], column=coordonne[1], padx=1, pady=1, ipadx=0, ipady=0)
    # print("coordonne0 = {}\ncoordonneMax = {}".format(coordonne0, coordonneMax))



noeudActuel = Noeud(puzzle, 0, 0)
voisins(noeudActuel)

# closedList = File()
# openList = File()
# openList.ajouter(noeudActuel)
# n = 0
# while openList.noeuds[n]:
#     noeudActuel = openList.depiler()
#     if heuristique(noeudActuel.puzzle, puzzleGoal) == 0:
#         return 1
#     for v in :


fenetre.mainloop()

fenetre.destroy()

        


































