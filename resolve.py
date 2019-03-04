#!/usr/bin/env python
# -*-coding:Utf-8 -*

import pickle
from tkinter import *
from collections import OrderedDict
import time
import visual

class variable:
	def __init__(self, val):
	    self.variable = val

	def Change(self, newVal):
	    self.variable = newVal

	def Add(self, add):
		self.variable += add

	def Int(self):
		return self.variable

class Noeud:

    def __init__(self, puzzle, cout, heuristique, parent):
        self.puzzle = puzzle
        self.cout = cout
        self.heuristique = heuristique
        self.parent = parent

class List:

    def __init__(self, name):
        self.noeuds = []    # creates a new empty list
        self.max = 0
        self.name = name

    def ajouter(self, noeud):
        self.noeuds.insert(0, noeud)
        # self.noeuds.append(noeud)
        self.max += 1
        # print('On vient d\'ajouter un element a {}, on en a actuellement {}'.format(self.name, self.max))

    def supprimer(self, noeud):
        self.noeuds.remove(noeud)
        self.max -= 1
        # print('On vient de supprimer un element a {}, on en a actuellement {}'.format(self.name, self.max))

    def depiler(self):
        if self.max == 0:
            return -1
        ret = self.noeuds[0]
        n = 0
        # print('In depiler')
        while n < self.max:
            # print('noeuds[{}]:  {},{}\nret: {},{}'.format(n, self.noeuds[n].heuristique, self.noeuds[n].cout, ret.heuristique, ret.cout))
            if compare2Noeuds(self.noeuds[n], ret) == 1:
                ret = self.noeuds[n]
            n += 1
        # print('On return : {},{}'.format(ret.heuristique, ret.cout))
        return ret

def createInitiateState(file, w_tab, h_tab):
	mon_fichier = open(file, "r")
	contenu = mon_fichier.read()
	contenu = contenu.split('\n')

	del contenu[0]
	del contenu[0]
	if contenu[len(contenu) - 1] == '' :
		del contenu[len(contenu) - 1]
	
	puzzle = {}

	for i, elt in enumerate(contenu):
	    elt = elt.split()
	    h_tab.Change(i)
	    for n,subElt in enumerate (elt):
	        puzzle[i, n] = subElt
	        w_tab.Change(n)
	puzzle = OrderedDict(sorted(puzzle.items(), key=lambda t: t[0]))

	w_tab.Add(1)
	h_tab.Add(1)

	return puzzle

def createGoalState(w_tab, h_tab):
	puzzleGoal = {}

	size=(w_tab.Int(), h_tab.Int())

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

	return puzzleGoal

def createLinearGoal(w_tab, h_tab):
	puzzleGoal = {}
	size=(w_tab.Int(), h_tab.Int())
	
	i = 1
	x = 0
	while x < size[0]:
		y = 0
		while y < size[1]:
			puzzleGoal[x,y] = i % (size[0] * size[1])
			y += 1
			i += 1
		x += 1

	puzzleGoal = OrderedDict(sorted(puzzleGoal.items(), key=lambda t: t[0]))
	
	return puzzleGoal

def initFrame(fenetre):
	FrameRPuzzle = Frame(fenetre, borderwidth=2, bg='black')
	FrameRPuzzle.pack(side=BOTTOM)
	return FrameRPuzzle

def initWindow(initialState, goalState, window, w_tab, h_tab):

	fenetre = Tk()

	fenetre['bg']='black'

	# FrameBase = Frame(fenetre, borderwidth=2, bg='black')
	# FrameBase.pack(padx=50, pady=50)

	# FrameInitial = Frame(FrameBase, borderwidth=2, bg='black')
	# FrameInitial.grid(row=0, column=0, padx=10)

	# Label(FrameInitial, text="Steps",bg='black', fg='white', font="Times 20 italic").pack(fill=X)

	FrameRPuzzle = Frame(fenetre, borderwidth=2, bg='black')
	FrameRPuzzle.pack(side=BOTTOM)

	def exit(event):
		fenetre.quit()

	fenetre.bind("<Escape>", exit)

	# Button(fenetre, text="supprime", command=(lambda : onSup(FrameRPuzzle))).pack()
	# Button(fenetre, text="draw", command=(lambda : drawPuzzle(FrameRPuzzle, initialState, goalState, window, w_tab, h_tab))).pack()
	return fenetre

def onSup(frame):
    for w in frame.winfo_children():
        w.destroy()

def drawPuzzle(frame, puzzle, puzzleGoal, window, w_tab, h_tab):

	FramePuzzle = Frame(frame, borderwidth=2, bg='black')
	FramePuzzle.pack(side=TOP)

	for coordonne, valeur in puzzle.items():
	    if int(valeur) == 0:
	        background = 'black'
	    elif int(valeur) == int(puzzleGoal[coordonne[0], coordonne[1]]) :
	        background = 'green'
	    else :
	        background = 'red'
	    canvas = Canvas(FramePuzzle, width=window / w_tab.Int(), height=window / h_tab.Int(), background=background, highlightthickness=0)
	    txt = canvas.create_text((window / w_tab.Int()) / 2, (window / h_tab.Int()) / 2, text='%s' % (valeur), font="Arial 16 italic", fill="black")
	    canvas.grid(row=coordonne[0], column=coordonne[1], padx=1, pady=1, ipadx=0, ipady=0)

def compare2Noeuds(n1, n2):
    if (n1.heuristique < n2.heuristique) or (n1.heuristique == n2.heuristique and n1.cout < n2.cout):
    	return 1
    return 0
    # if n1.heuristique + n1.cout < n2.heuristique + n2.cout:
    # 	return 1
    # return 0

def hammingHeuristique(puzzle, puzzleGoal):
    heuristique = 0;
    for coordonne, valeur in puzzle.items():
        if int(valeur) != 0 and int(valeur) != int(puzzleGoal[coordonne[0], coordonne[1]]):
            heuristique += 1
    return heuristique

def manhattanDistance(valeur, coordonne, puzzle, puzzleGoal):
	distance = 0
	for coordonneGoal, valeurGoal in puzzleGoal.items():
		if int(valeurGoal) == int(valeur):
			distance += abs(int(coordonneGoal[0]) - int(coordonne[0]))
			distance += abs(int(coordonneGoal[1]) - int(coordonne[1]))
			break
	return distance

def manhattanHeuristique(puzzle, puzzleGoal):
    heuristique = 0;
    for coordonne, valeur in puzzle.items():
        heuristique += manhattanDistance(valeur, coordonne, puzzle, puzzleGoal)
    return heuristique

def findCoordonneValue(valeur, puzzleGoal):
	for coordonneGoal, valeurGoal in puzzleGoal.items():
		if int(valeur) == int(valeurGoal):
			return coordonneGoal

def numOnTheWay(start, end, puzzle):
	values = []
	if start[0] == end[0]:
		values.append(puzzle[start])
		while start[1] != end[1]:
			if start[1] > end[1]:
				start = (start[0], start[1] - 1)
			else:
				start = (start[0], start[1] + 1)
			values.append(puzzle[start])
	elif start[1] == end[1]:
		values.append(puzzle[start])
		while start[0] != end[0]:
			if start[0] > end[0]:
				start = (start[0] - 1, start[1])
			else:
				start = (start[0] + 1, start[1])
			values.append(puzzle[start])
	return values

def linearConflict(puzzle, puzzleGoal):
	print("In linearConflict")
	heuristique = 0;
	conflit = 0

	y = 0
	while y < 3:
		x = 0
		s = ""
		while x < 3:
			s += str(puzzle[y, x])
			s += ' '
			# print("puzzle[",x,",",y,'] = ', puzzle[y,x])
			x += 1
		x = 0
		s += '	'
		while x < 3:
			s += str(puzzleGoal[y , x])
			s += ' '
			# print("puzzle[",x,",",y,'] = ', puzzle[y,x])
			x += 1
		print(s)
		y += 1

	for coordonne, valeur in puzzle.items():
		heuristique += manhattanDistance(valeur, coordonne, puzzle, puzzleGoal)
		coordonneGoal = findCoordonneValue(valeur, puzzleGoal)
		otherValue = puzzle[coordonneGoal[0], coordonneGoal[1]]
		otherValueCoordonne = findCoordonneValue(otherValue, puzzle)
		otherCoordonneGoal = findCoordonneValue(otherValue, puzzleGoal)
		print("\nvalue = ", valeur, "coordonne actuelle =", coordonne, "coordonneGoal", coordonneGoal)
		print("otherValue = ", otherValue, "coordonne actuelle =", otherValueCoordonne, "coordonneGoal", otherCoordonneGoal)

		values = numOnTheWay(coordonne, coordonneGoal, puzzle)
		print("On affiche les value")
		for value in values:
			print(value)

		test = 0
		if (coordonne[0] == coordonneGoal[0] and coordonne[1] + 2 == coordonneGoal[1]):
			test = 1
			coordonneGoal = (coordonneGoal[0], coordonneGoal[1] - 1)
		elif (coordonne[0] == coordonneGoal[0] and coordonne[1] - 2 == coordonneGoal[1]):
			test = 1
			coordonneGoal = (coordonneGoal[0], coordonneGoal[1] + 1)
		elif (coordonne[1] == coordonneGoal[1] and coordonne[0] + 2 == coordonneGoal[0]):
			test = 1
			coordonneGoal = (coordonneGoal[0] - 1, coordonneGoal[1])
		elif (coordonne[1] == coordonneGoal[1] and coordonne[0] - 2 == coordonneGoal[0]):
			test = 1
			coordonneGoal = (coordonneGoal[0] + 1, coordonneGoal[1])
		if test == 1:
			otherValue = puzzle[coordonneGoal[0], coordonneGoal[1]]
			otherValueCoordonne = findCoordonneValue(otherValue, puzzle)
			otherCoordonneGoal = findCoordonneValue(otherValue, puzzleGoal)
			print("\n2: value = ", valeur, "coordonne actuelle =", coordonne, "coordonneGoal", coordonneGoal)
			print("2: otherValue = ", otherValue, "coordonne actuelle =", otherValueCoordonne, "coordonneGoal", otherCoordonneGoal)
		
def createVoisin(noeud, oldPos0, newPos0, puzzleGoal):
    voisin = Noeud(noeud.puzzle.copy(), noeud.cout + 1, 0, noeud)
    tmp = voisin.puzzle[oldPos0]
    voisin.puzzle[oldPos0] = voisin.puzzle[newPos0]
    voisin.puzzle[newPos0] = tmp
    # voisin.heuristique = hammingHeuristique(voisin.puzzle, puzzleGoal)
    voisin.heuristique = manhattanHeuristique(voisin.puzzle, puzzleGoal)
    # linearConflict(voisin.puzzle, puzzleGoal)
    return voisin

def findVoisins(noeud, puzzleGoal):
    voisins = []
    coordonne0 = (-1,-1);
    coordonneMax = (-1,-1);
    for cle, valeur in noeud.puzzle.items():
        if int(valeur) == 0:
            coordonne0 = cle
        coordonneMax = cle
    if coordonne0[1] >= 1:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] - 1), puzzleGoal))
    if coordonne0[1] < coordonneMax[1]:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] + 1), puzzleGoal))
    if coordonne0[0] >= 1:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] - 1, coordonne0[1]), puzzleGoal))
    if coordonne0[0] < coordonneMax[0]:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] + 1, coordonne0[1]), puzzleGoal))
    return voisins

def printPuzzle(puzzle):
	s = ""
	for cle, valeur in puzzle.items():
		# s += valeur
		if (cle[1] == 0):
			s += "	\n"
		else:
			s += "	"
		s += str(valeur)
	print(s,'\n')

def printNoeud(noeud, infoOn):
	if (infoOn):
		print('Cout: {}\nHeuristique: {}'.format(noeud.cout, noeud.heuristique))
	printPuzzle(noeud.puzzle)

def same2Dict(dict1, dict2):
    for cle, valeur in dict1.items():
        if int(dict2[cle]) != int(valeur):
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

def heuristiquePuzzleInList(list, puzzle):
    for noeud in list:
        if same2Dict(noeud.puzzle, puzzle) == 1:
            return noeud.cout
    return 0

def printInfoNoeud(noeud):
    print('Cout: {}\nHeuristique: {}\n0 Position: {}\n\n'.format(noeud.cout, noeud.heuristique, findCoordonne0(noeud.puzzle)))

def printInfoList(list, infoOn):
    i = 1;
    print(list.name,":\n")
    for noeud in list.noeuds:
        print('Noeud #{}:\n'.format(i))
        i += 1
        printNoeud(noeud, infoOn)
        # printInfoNoeud(noeud)

def main():
	window = 200;

	h_tab = variable(0)
	w_tab = variable(0)

	puzzleInitial = createInitiateState("puzzle/puzzle3.txt", h_tab , w_tab)

	# puzzleGoal = createGoalState(h_tab , w_tab)

	puzzleGoal = createLinearGoal(h_tab , w_tab)

	# fenetre = initWindow(puzzleInitial, puzzleGoal, window, w_tab, h_tab)
	
	# FrameRPuzzle = initFrame(fenetre)
	# fenetre.mainloop()

	# fenetre.destroy()

	openList = List("openList")
	closedList = List("closedList")

	noeudActuel = Noeud(puzzleInitial, 0, 0, 0)
	
	openList.ajouter(noeudActuel)
	
	i = 0

	# linearConflict(noeudActuel.puzzle, puzzleGoal)

	while openList.max > 0 and i < 10000:
		
		i += 1
		# print('Boucle #{}\n'.format(i))
		
		noeudActuel = openList.depiler()

		# print("noeudActuel : \n")
		# printNoeud(noeudActuel, 1)

		# print("diff = ", hammingHeuristique(noeudActuel.puzzle, puzzleGoal), "\n")

		if hammingHeuristique(noeudActuel.puzzle, puzzleGoal) == 0:
			finalList = List("finalList")
			while noeudActuel.parent != 0:
				finalList.ajouter(noeudActuel)
				noeudActuel = noeudActuel.parent

			print("Reussi")
			printInfoList(finalList, 0)
			visual.visual(w_tab.Int(), puzzleGoal, finalList)
			print("nb boucle : ", i)

			# fenetre = initWindow(puzzleInitial, puzzleGoal, window, w_tab, h_tab)

			# FrameRPuzzle = initFrame(fenetre)

			# for noeud in finalList.noeuds:
			# 	drawPuzzle(FrameRPuzzle, noeud.puzzle, puzzleGoal, window, w_tab, h_tab)
			# 	time.sleep(0.5)
			# 	fenetre.update()
			# 	onSup(FrameRPuzzle)

			# drawPuzzle(FrameRPuzzle, noeud.puzzle, puzzleGoal, window, w_tab, h_tab)
			# fenetre.mainloop()
			return 1

		for v in findVoisins(noeudActuel, puzzleGoal):
			if puzzleInList(closedList.noeuds, v.puzzle) and coutPuzzleInList(closedList.noeuds, v.puzzle) <= v.cout:
				pass
			elif puzzleInList(openList.noeuds, v.puzzle) and heuristiquePuzzleInList(openList.noeuds, v.puzzle) <= v.heuristique:
				pass
			else:
				openList.ajouter(v)
		
		closedList.ajouter(noeudActuel)
		openList.supprimer(noeudActuel)

main()

# fenetre.mainloop()



