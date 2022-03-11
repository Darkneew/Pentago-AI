#!/usr/bin/python
# -*- coding: UTF-8 -*-

from copy import deepcopy
from eval import fonction_evaluation_simple as evaluation

grille = [[0 for i in range(6)] for j in range(6)]

def isWinning (g, side):
    '''Savoir si le side gagne sur la g'''
    lg = len(g)
    for i in range(lg):
        if isWinningColumn(g[i], side):
            return True
        if isWinningColumn([c[i] for c in g], side):
            return True
    if isWinningColumn([g[i][i] for i in range(lg)], side):
        return True
    if isWinningColumn([g[i][lg-1-i] for i in range(lg)], side):
        return True
    b1, b2, b3, b4 = True, True, True, True
    for i in range(lg-1):
        b1 = b1 and g[i][i+1] == side
        b2 = b2 and g[i+1][i] == side
        b3 = b3 and g[lg-1-i][i+1] == side
        b4 = b4 and g[lg-2-i][i] == side
    if b1 or b2 or b3 or b4:
        return True
    return False

def isWinningColumn (col, side):
    '''Renvoie si le side forme une ligne sur la colonne de 6 cases donnée'''
    l = len(col) - 1
    if col[0] != side and col[l] != side:
        return False
    for i in range(1, l):
        if col[i] != side:
            return False
    return True

def rotate (g, sens):
    '''Tourne la grille dans le sens indiqué'''
    tourne=[[0 for k in range(len(g))] for j in range(len(g))]
    n=len(g)-1
    if sens==1:
        for i in range(len(g)):
            for j in range(len(g)):
                tourne[i][j]=g[j][n-i]
    elif sens==0:
        for i in range(len(g)):
            for j in range(len(g)):
                tourne[i][j]=g[n-j][i]
    return tourne

def grilleToMiniGrille(g):
    L1,L2,L3,L4=[],[],[],[]
    n = len(g)
    for i in range(n):
        if i<3:
            L1.append(g[i][:n//2])
            L2.append(g[i][n//2:])
        else :
            L3.append(g[i][:n//2])
            L4.append(g[i][n//2:])
    return([L1,L2,L3,L4])

def miniGrilleToGrille(m):
    L=[]
    n = len(m[0]) + len(m[1])
    for i in range(n):
        if i < n//2:
            L.append(m[0][i] + m[1][i])
        else:
            L.append(m[2][i-n//2] + m[3][i-n//2])
    return L

def choosePos (g):
    '''Permet au joueur de choisir une position libre sur la grille et retourne la position choisie'''
    while True:
        try:
            x = int(input("Sur quelle ligne voulez vous jouer?\n"))
        except ValueError:
            print("Veuillez choisir un nombre valide")
            continue
        if x >= 6 or x < 0: 
            print("Votre nombre doit être entre 0 et 5")
            continue
        try:
            y = int(input("Sur quelle colonne voulez vous jouer?\n"))
        except ValueError:
            print("Veuillez choisir un nombre valide")
            continue
        if y >= 6 or y < 0: 
            print("Votre nombre doit être entre 0 et 5")
            continue
        if g[x][y] != 0:
            print("Cette position est occupée, veuillez choisir une autre case")
            continue
        v = str(input("Validez vous votre coup? (si oui, entrez y)")).lower() # le str est là parce que replit est buggé, fonction à enlever si on repasse sur une ide qui fonctionne
        if v.startswith("y"):
            break
    return {"x":x, "y":y}

def ChooseRot ():
    '''Permet au joueur de choisir une rotation pour la grille et la retourne'''
    while True:
        try:
            n = int(input("Quelle grille voulez vous faire tourner? (en numérotant les grilles de 0 à 3 en partant de en haut à gauche)\n"))
        except ValueError:
            print("Veuillez choisir un nombre valide")
            continue
        if n >= 4 or n < 0: 
            print("Votre nombre doit être entre 0 et 3")
            continue
        try:
            s = int(input("Dans quel sens voulez vous faire tourner la grille? (entrez 0 pour faire tourner dans le sens horaire et 1 pour le sens antihoraire)\n"))
        except ValueError:
            print("Veuillez choisir un nombre valide")
            continue
        if s >= 2 or s < 0: 
            print("Veuillez choisir 0 ou 1")
            continue
        v = input("Validez vous votre coup? (si oui, entrez y)").lower()
        if v.startswith("y"):
            break
    return {"n":n, "s":s}

def turn (g, side):
    '''Fait le tour de side dans la g. Retourne la nouvelle grille'''
    _g = deepcopy(g)
    pos = choosePos(_g)
    _g[pos["x"]][pos["y"]] = side
    rot = ChooseRot()
    mg = grilleToMiniGrille(_g)
    mg[rot["n"]] = rotate(mg[rot["n"]], rot["s"])
    return miniGrilleToGrille(mg)

def turn_ia (g, side):
    '''Fait le tour de side dans la g. Retourne la nouvelle grille'''
    best_pos = {"x":0, "y":0}
    best_score = -100
    best_rot = {"n":0, "s":0}
    for x in range(len(g)):
        for y in range(len(g)):
            if g[x][y] != 0:
                continue
            for n in range(4):
                for s in range(2):
                    _g = deepcopy(g)
                    _g[x][y] = side
                    mg = grilleToMiniGrille(_g)
                    mg[n] = rotate(mg[n], s)
                    score = evaluation(miniGrilleToGrille(mg), side)
                    if score > best_score:
                        best_pos = {"x":x, "y":y}
                        best_rot = {"n":n, "s":s}
                        best_score = score
    __g = deepcopy(g)
    __g[best_pos["x"]][best_pos["y"]] = side
    _mg = grilleToMiniGrille(__g)
    _mg[best_rot["n"]] = rotate(_mg[best_rot["n"]],best_rot["s"])
    return miniGrilleToGrille(_mg)

def printGrille(g):
    '''Affiche la grille'''
    L=["-" for k in range(6)]
    print("+".join(L))
    for i in g:
        print("|".join(map(str, i)))
        print("+".join(L))
    print("\n\n")
    return 
         


with_ia_1 = input("Do you want the player 1 to be an AI? (n for no)\n")
with_ia_1 = False if with_ia_1.lower().startswith("n") else True
with_ia_2 = input("Do you want the player 2 to be an AI? (n for no)\n")
with_ia_2 = False if with_ia_2.lower().startswith("n") else True

while True:
    printGrille(grille)
    if with_ia_1:
        grille = turn_ia(grille, 1)
    else:
        grille = turn(grille, 1)
    if isWinning(grille, 1):
        print("player 1 win")
        break
    printGrille(grille)
    if with_ia_2:
        grille = turn_ia(grille, 2)
    else:
        grille = turn(grille, 2)
    if isWinning(grille, 2):
        print("player 2 win")
        break