#!/usr/bin/env python
# -*-coding:Utf-8 -*

import pickle
from tkinter import *
from collections import OrderedDict
import time

class Noeud:

    def __init__(self, puzzle, cout, heuristique):
        self.puzzle = puzzle
        self.cout = cout
        self.heuristique = heuristique
        

class File:

    def __init__(self, name):
        self.noeuds = []    # creates a new empty list
        self.max = 0
        self.name = name

    def ajouter(self, noeud):
        self.noeuds.append(noeud)
        self.max += 1
        print('On vient d\'ajouter un element a {}, on en a actuellement {}'.format(self.name, self.max))

    def supprimer(self, noeud):
        self.noeuds.remove(noeud)
        self.max -= 1
        print('On vient de supprimer un element a {}, on en a actuellement {}'.format(self.name, self.max))

    def depiler(self):
        if self.max == 0:
            return -1
        ret = self.noeuds[0]
        n = 0
        print('In depiler')
        while n < self.max:
            # print('noeuds[{}]:  {},{}\nret: {},{}'.format(n, self.noeuds[n].heuristique, self.noeuds[n].cout, ret.heuristique, ret.cout))
            if compare2Noeuds(self.noeuds[n], ret) == 1:
                ret = self.noeuds[n]
            n += 1
        print('On return : {},{}'.format(ret.heuristique, ret.cout))
        return ret


def compare2Noeuds(n1, n2):
    if (n1.heuristique + n1.cout < n2.heuristique + n2.cout) or (n1.heuristique + n1.cout == n2.heuristique + n2.cout and n1.cout > n2.cout):
        return 1
    elif n1.heuristique + n1.cout == n2.heuristique + n2.cout:
        return 0
    else :
        return -1

def hammingHeuristique(puzzle, puzzleGoal):
    bad = 0;
    for coordonne, valeur in puzzle.items():
        if int(valeur) != 0 and int(valeur) != int(puzzleGoal[coordonne[0], coordonne[1]]):
            bad += 1
    return bad

def manhattanHeuristique(puzzle, puzzleGoal):
    commun = 0;
    items = 0;
    for coordonne, valeur in puzzle.items():
        items += 1
        if int(valeur) == int(puzzleGoal[coordonne[0], coordonne[1]]):
            commun += 1
    return items - commun

def createVoisin(noeud, oldPos0, newPos0):
    voisin = Noeud(noeud.puzzle.copy(), noeud.cout + 1, noeud.heuristique)
    tmp = voisin.puzzle[oldPos0]
    # print('oldPos0 = {}, newPos0 = {}'.format(oldPos0, newPos0))
    voisin.puzzle[oldPos0] = voisin.puzzle[newPos0]
    voisin.puzzle[newPos0] = tmp
    voisin.heuristique = hammingHeuristique(voisin.puzzle, puzzleGoal)
    return voisin

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
    # print('Noeud actuel\nheuristique: {}\ncout: {}\ncoordonne0: {},{}\ncoordonne max: {},{}\nVoisins :'.format(noeud.heuristique, noeud.cout, coordonne0[0], coordonne0[1], coordonneMax[0], coordonneMax[1]))
    # print('1    coordonne0 : {},{}'.format(coordonne0[0], coordonne0[1] - 1))
    # print('2    coordonne0 : {},{}'.format(coordonne0[0], coordonne0[1] + 1))
    # print('3    coordonne0 : {},{}'.format(coordonne0[0] - 1, coordonne0[1]))
    # print('4    coordonne0 : {},{}\n\n'.format(coordonne0[0] + 1, coordonne0[1]))
    if coordonne0[1] >= 1:
        # print('1    coordonne0 : {},{}'.format(coordonne0[0], coordonne0[1] - 1))
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] - 1)))
    if coordonne0[1] < coordonneMax[1]:
        # print('2    coordonne0 : {},{}'.format(coordonne0[0], coordonne0[1] + 1))
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] + 1)))
    if coordonne0[0] >= 1:
        # print('3    coordonne0 : {},{}'.format(coordonne0[0] - 1, coordonne0[1]))
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] - 1, coordonne0[1])))
    if coordonne0[0] < coordonneMax[0]:
        # print('4    coordonne0 : {},{}'.format(coordonne0[0] + 1, coordonne0[1]))
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] + 1, coordonne0[1])))
    return voisins

def same2Dict(dict1, dict2):
    for cle, valeur in dict1.items():
        if dict2[cle] != valeur:
            return 0
    return 1

def puzzleInList(list, puzzle):
    for noeud in list:
        if same2Dict(noeud.puzzle, puzzle) == 1:
            return 1
    return 0

def coutPuzzleInList(list, puzzle):
    for noeud in list:
        if same2Dict(noeud.puzzle, puzzle) == 1:
            return noeud.cout
    return 0

def onSup(frame):
    for w in frame.winfo_children():
        w.destroy()

def printInfoNoeud(noeud):
    print('Cout: {}\nHeuristique: {}\n0 Position: {}\n\n'.format(noeud.cout, noeud.heuristique, findCoordonne0(noeud.puzzle)))

def printInfoList(list):
    i = 1;
    for noeud in list:
        print('Noeud #{}:\n'.format(i))
        i += 1
        printInfoNoeud(noeud)

def loop():
    
    noeudActuel = Noeud(puzzle, 0, 0)

    closedList = File("closedList")
    openList = File("openList")
    openList.ajouter(noeudActuel)
    i = 0
    while openList.max > 0 and i < 500:
        i += 1
        print('Boucle #{}'.format(i))
        # printInfoList(openList.noeuds)
        # noeudActuel = openList.noeuds[0]
        noeudActuel = openList.depiler()
        print('Noeud actuel:\n')
        printInfoNoeud(noeudActuel)
        # onSup(FrameRPuzzle)
        # print ("Start : {}".format(time.ctime()))
        # time.sleep(0.2)
        # print ("End : {}".format(time.ctime()))
        # drawPuzzle(FrameRPuzzle, noeudActuel.puzzle, puzzleGoal)
        # fenetre.update()
        if hammingHeuristique(noeudActuel.puzzle, puzzleGoal) == 0:
            return(1)
        v_i = 0
        for v in voisins(noeudActuel):
            print('openList:\n')
            printInfoList(openList.noeuds)
            print('closedList:\n')
            printInfoList(closedList.noeuds)
            print('noeud voisin #{}:\n'.format(v_i))
            printInfoNoeud(v)
            v_i += 1
            if (puzzleInList(closedList.noeuds, v.puzzle) and v.cout >= coutPuzzleInList(closedList.noeuds, v.puzzle)) or (puzzleInList(openList.noeuds, v.puzzle) and  v.cout >= coutPuzzleInList(openList.noeuds, v.puzzle)):
                print('pass')
                pass
            else:
                print('add')
                openList.ajouter(v)
        # print('On avait : {},{}'.format(noeudActuel.heuristique, noeudActuel.cout))
        closedList.ajouter(noeudActuel)
        openList.supprimer(noeudActuel)
    return(0)

def exit(event):
    fenetre.quit()

def drawPuzzle(frame, puzzle, puzzleGoal):

    FramePuzzle = Frame(frame, borderwidth=2, bg='black')
    FramePuzzle.pack(side=TOP)

    for coordonne, valeur in puzzle.items():
        if int(valeur) == 0:
            background = 'black'
        elif int(valeur) == int(puzzleGoal[coordonne[0], coordonne[1]]) :
            background = 'green'
        else :
            background = 'red'
        canvas = Canvas(FramePuzzle, width=window / w_tab, height=window / h_tab, background=background, highlightthickness=0)
        txt = canvas.create_text((window / w_tab) / 2, (window / h_tab) / 2, text='%s' % (valeur), font="Arial 16 italic", fill="black")
        canvas.grid(row=coordonne[0], column=coordonne[1], padx=1, pady=1, ipadx=0, ipady=0)


mon_fichier = open("puzzle/puzzle3-2.txt", "r")
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
        puzzle[i, n] = subElt
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

Label(FrameInitial, text="Steps",bg='black', fg='white', font="Times 20 italic").pack(fill=X)

FrameRPuzzle = Frame(FrameInitial, borderwidth=2, bg='black')
FrameRPuzzle.pack(side=BOTTOM)
# Label(FrameRPuzzle, text="1").pack()
# Label(FrameRPuzzle, text="2").pack()

# drawPuzzle(FrameRPuzzle, puzzle, puzzleGoal)

# FrameGoal = Frame(FrameBase, borderwidth=2, bg='black')
# FrameGoal.grid(row=0, column=1, padx=10)

# Label(FrameGoal, text="Goal state",bg='black', fg='white', font="Times 20 italic").pack(fill=X)

# drawPuzzle(FrameGoal, puzzleGoal, puzzleGoal)

fenetre.bind("<Escape>", exit)

# FrameVoisin = Frame(fenetre, borderwidth=2, bg='black')
# FrameVoisin.pack(side=TOP)

# Label(FrameVoisin, text="Voisins",bg='black', fg='white', font="Times 20 italic").pack(fill=X)

# fenetre.mainloop()

# fenetre.destroy()

# algo de resolution

# Label(fenetre, text="texte").pack()
# Button(fenetre, text="supprime", command=(lambda : onSup(FrameRPuzzle))).pack()
# Button(fenetre, text="draw", command=(lambda : drawPuzzle(FrameRPuzzle, puzzle, puzzleGoal))).pack()

# fenetre.mainloop()

if (loop() == 1):
    print('Reussi')
else:
    print('Rate')

# print ("Start : {}".format(time.ctime()))
# time.sleep(0.5)
# print ("End : {}".format(time.ctime()))

# fenetre.update()
# fenetre.mainloop()

# fenetre.destroy()

        


































