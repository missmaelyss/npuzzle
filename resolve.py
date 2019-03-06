#!/usr/bin/env python
# -*-coding:Utf-8 -*

import pickle
from tkinter import *
from collections import OrderedDict
import time
import visualStart
import visualFinal

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
        self.noeuds = []
        self.max = 0
        self.name = name

    def ajouter(self, noeud):
       	self.noeuds.insert(0, noeud)
        self.max += 1

    def supprimer(self, noeud):
        self.noeuds.remove(noeud)
        self.max -= 1

    def getBest(self, type):
        if self.max == 0:
            return -1
        ret = self.noeuds[0]
        n = 0
        while n < self.max:
            if type == 1 and compare2Noeuds(self.noeuds[n], ret) == 1:
                ret = self.noeuds[n]
            elif type == 2 and compare2Heuristique(self.noeuds[n], ret) == 1:
                ret = self.noeuds[n]
            n += 1
        return ret

class Mode():
	def __init__(self, heuristique, greedy, visualFinal):
		self.heuristique = heuristique
		self.greedy = greedy
		self.visualFinal = visualFinal

	def chooseHeuristique(self, heuristique):
		self.heuristique = heuristique
		
	def switchGreedy(self):
		self.greedy = int(self.greedy + 1) % 2

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

def compare2Noeuds(n1, n2):
    if (n1.heuristique < n2.heuristique) or (n1.heuristique == n2.heuristique and n1.cout < n2.cout):
    	return 1
    return 0

def compare2Heuristique(n1, n2):
    if (n1.heuristique < n2.heuristique):
    	return 1
    return 0

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

def lenTab(tab):
	n = 0
	for truc in tab:
		n += 1
	return n

def isOnTheWay(values, valueToFind):
	if values == []:
		return 0
	for value in values:
		if value == valueToFind:
			return 1
	return 0

def linearConflict(puzzle, puzzleGoal):
	heuristique = 0
	conflit = 0

	for coordonne, valeur in puzzle.items():
		heuristique += manhattanDistance(valeur, coordonne, puzzle, puzzleGoal)
		coordonneGoal = findCoordonneValue(valeur, puzzleGoal)
		values = numOnTheWay(coordonne, coordonneGoal, puzzle)
		for value in values:
			if int(value) == int(valeur):
				continue
			if isOnTheWay(numOnTheWay(findCoordonneValue(value, puzzle), findCoordonneValue(value, puzzleGoal), puzzle), valeur) == 1:
				conflit += 1
			elif lenTab(numOnTheWay(findCoordonneValue(value, puzzle), findCoordonneValue(value, puzzleGoal), puzzle)) == 1:
				conflit += 2
	return heuristique + conflit
		
def createVoisin(noeud, oldPos0, newPos0, puzzleGoal, mode):
    voisin = Noeud(noeud.puzzle.copy(), noeud.cout + 1, 0, noeud)
    tmp = voisin.puzzle[oldPos0]
    voisin.puzzle[oldPos0] = voisin.puzzle[newPos0]
    voisin.puzzle[newPos0] = tmp
    if mode == 1:
    	voisin.heuristique = hammingHeuristique(voisin.puzzle, puzzleGoal)
    elif mode == 2:
    	voisin.heuristique = manhattanHeuristique(voisin.puzzle, puzzleGoal)
    else:
    	voisin.heuristique = linearConflict(voisin.puzzle, puzzleGoal)
    return voisin

def findVoisins(noeud, puzzleGoal, mode):
    voisins = []
    coordonne0 = (-1,-1);
    coordonneMax = (-1,-1);
    for cle, valeur in noeud.puzzle.items():
        if int(valeur) == 0:
            coordonne0 = cle
        coordonneMax = cle
    if coordonne0[1] >= 1:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] - 1), puzzleGoal, mode))
    if coordonne0[1] < coordonneMax[1]:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0], coordonne0[1] + 1), puzzleGoal, mode))
    if coordonne0[0] >= 1:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] - 1, coordonne0[1]), puzzleGoal, mode))
    if coordonne0[0] < coordonneMax[0]:
        voisins.append(createVoisin(noeud, coordonne0, (coordonne0[0] + 1, coordonne0[1]), puzzleGoal, mode))
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

def puzzleInList2(list, puzzle):
    for noeud in list:
        print("1:")
        printPuzzle(noeud.puzzle)
        print("2:")
        printPuzzle(puzzle)
        if same2Dict(noeud.puzzle, puzzle) == 1:
            print("Same")
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
    i = 1
    print(list.name,":\n")
    for noeud in list.noeuds:
        print('Noeud #{}:\n'.format(i))
        i += 1
        printNoeud(noeud, infoOn)		

def getZeroIndex(puzzle, size):
	i = 0
	while (i < size):
		j = 0
		while (j < size):
			# print(int(puzzle[i,j]))
			if (int(puzzle[i,j]) == 0):
				return ((i * size) + j)
			j += 1
		i += 1
	print('Unexpected error')

def getInversionsFor(puzzle, i, j, x, size):
    if (x == 0):
        return 0
    inversions = 0
    while (i < size):
        while (j < size):
            if (puzzle[i,j] != 0 and puzzle[i,j] < x):
                inversions += 1
            j += 1
        j = 0
        i += 1
    return inversions

def getInversions(puzzle, size):
    inversions = 0
    i = 0
    while (i < size):
        j = 0
        while (j < size):
            inversions += getInversionsFor(puzzle, i, j, puzzle[i,j], size)
            j += 1
        i += 1
    return inversions

def checkSolvable(puzzle, goal, size):
    start = getInversions(puzzle, size)
    end = getInversions(goal, size)
    if (size % 2 == 0):
        start += int(getZeroIndex(puzzle) / size, size)
        end += int(getZeroIndex(goal) / size, size)
    if ((start % 2 == end % 2) is False):
        print('Unsolvable')
    else:
    	print('Solvable')
	
def greedy(openList, closedList, mode, puzzleInitial, puzzleGoal, w_tab):

	timeComplexity = 0
	sizeComplexity = 0
	while openList.max > 0:
		timeComplexity += 1
		noeudActuel = openList.getBest(2)
		if hammingHeuristique(noeudActuel.puzzle, puzzleGoal) == 0:
			finalList = List("finalList")
			while noeudActuel.parent != 0:
				finalList.ajouter(noeudActuel)
				noeudActuel = noeudActuel.parent
			printInfoList(finalList, 0)
			print("Complexity in time:\t", timeComplexity)
			print("Complexity in size:\t", sizeComplexity)
			print("OpenList:\t", openList.max)
			print("ClosedList:\t", closedList.max)
			print("Moves:\t", finalList.max)
			if mode.visualFinal == 1:
				visualFinal.visualFinal(w_tab.Int(), puzzleGoal, finalList)
				print("Fini !")
			return 1
		better = 0
		for v in findVoisins(noeudActuel, puzzleGoal, mode.heuristique):
			if puzzleInList(closedList.noeuds, v.puzzle) and coutPuzzleInList(closedList.noeuds, v.puzzle) <= v.cout:
				pass
			elif puzzleInList(openList.noeuds, v.puzzle) and heuristiquePuzzleInList(openList.noeuds, v.puzzle) <= v.heuristique:
				pass
			else:
				if better == 0 or v.heuristique < better.heuristique:
					better = v
				sizeComplexity += 1
		if puzzleInList(closedList.noeuds, noeudActuel.puzzle) == 0:
			closedList.ajouter(noeudActuel)
		openList.supprimer(noeudActuel)
		if better == 0:
			openList.ajouter(noeudActuel.parent)
		else:
			openList.ajouter(better)

def uniform(openList, closedList, mode, puzzleInitial, puzzleGoal, w_tab):
	timeComplexity = 0
	sizeComplexity = 0
	while openList.max > 0:
		timeComplexity += 1
		noeudActuel = openList.getBest(1)
		if hammingHeuristique(noeudActuel.puzzle, puzzleGoal) == 0:
			finalList = List("finalList")
			while noeudActuel.parent != 0:
				finalList.ajouter(noeudActuel)
				noeudActuel = noeudActuel.parent
			printInfoList(finalList, 0)
			print("Complexity in time:\t", timeComplexity)
			print("Complexity in size:\t", sizeComplexity)
			print("OpenList:\t", openList.max)
			print("ClosedList:\t", closedList.max)
			print("Moves:\t", finalList.max)
			if mode.visualFinal == 1:
				visualFinal.visualFinal(w_tab.Int(), puzzleGoal, finalList)
				print("Fini !")
			return 1
		for v in findVoisins(noeudActuel, puzzleGoal, mode.heuristique):
			if puzzleInList(closedList.noeuds, v.puzzle) and coutPuzzleInList(closedList.noeuds, v.puzzle) <= v.cout:
				pass
			elif puzzleInList(openList.noeuds, v.puzzle) and heuristiquePuzzleInList(openList.noeuds, v.puzzle) <= v.heuristique:
				pass
			else:
				sizeComplexity += 1
				openList.ajouter(v)
		closedList.ajouter(noeudActuel)
		openList.supprimer(noeudActuel)

def main():

	# start = visualStart.visualStart()
	# if start.file.get() == "":
	# 	return 
	mode = Mode(3,0, 0)
	# mode = Mode(start.heuristique.get(),start.greedy.get(), start.visual.get())
	h_tab = variable(0)
	w_tab = variable(0)
	timeComplexity = 0
	sizeComplexity = 0
	puzzleInitial = createInitiateState("puzzle/puzzle3.txt", h_tab , w_tab)
	# print(checkSolvable())
	# puzzleInitial = createInitiateState(start.file.get(), h_tab , w_tab)
	puzzleGoal = createGoalState(h_tab , w_tab)
	checkSolvable(puzzleInitial, puzzleGoal, h_tab.Int())
	checkSolvable(puzzleGoal, puzzleGoal, h_tab.Int())
	# print(getZeroIndex(puzzleGoal, h_tab.Int()))
	# openList = List("openList")
	# closedList = List("closedList")
	# noeudActuel = Noeud(puzzleInitial, 0, 0, 0)
	# openList.ajouter(noeudActuel)
	# if mode.greedy == 1:
	# 	greedy(openList, closedList, mode, puzzleInitial, puzzleGoal, w_tab)
	# else:
	# 	uniform(openList, closedList, mode, puzzleInitial, puzzleGoal, w_tab)

main()
# start = visualStart.visualStart()
# print(start.hamming.get(), start.manhattan.get(), start.linear.get(), start.greedy.get(), start.file.get())

