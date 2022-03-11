from random import randint
def fonction_evaluation_aleatoire (g, side):
    return randint(0, 400)

def fonction_evaluation_ordonee (g, side):
    return 0

def fonction_evaluation_naive (g, side):
    score = 0
    n = len(g[0])
    autours = [-1, 0, 1]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0: continue
            elif g[i][j] == side: 
                value = 1
            else: 
                value = -1
            for k in range(autours):
                for l in range(autours):
                    if not bien_def(i+k, j+l, n): continue
                    if g[i][j] == g[i+k][j+l]: score += value
    return score

def fonction_evaluation_naive_aggressive (g, side):
    score = 0
    n = len(g[0])
    autours = [-1, 0, 1]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0: continue
            elif g[i][j] == side: 
                value = 10
            else: 
                value = -1
            for k in range(autours):
                for l in range(autours):
                    if not bien_def(i+k, j+l, n): continue
                    if g[i][j] == g[i+k][j+l]: score += value
    return score

def fonction_evaluation_naive_defensive (g, side):
    score = 0
    n = len(g[0])
    autours = [-1, 0, 1]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0: continue
            elif g[i][j] == side: 
                value = 1
            else: 
                value = -10
            for k in range(autours):
                for l in range(autours):
                    if not bien_def(i+k, j+l, n): continue
                    if g[i][j] == g[i+k][j+l]: score += value
    return score

#PRINCIPE:
#ma fonction compte 1 point par tronc, puis note géométriquement en fonction de la taille du tronc
#j'ai créé des sous fonctions pour faire ca:
#la fonction extremites cherche quels sont les extrémités des troncs, et si ces extrémités forment un tronc d'axe X, Y ou diagonal de pente positive ou négative
#les fonctions de taille comptent la taille du tronc, j'ai fait 4 sous fonctions selon l'axe du tronc

def fonction_evaluation_simple(grille_tour_n,player):

    #dans les fonctions des troncs d'axe Y, diagonale de pente positive, diagonale de pente négative, il y a toutes les valeurs en double, donc va falloir diviser par 2 les résultats

    #compte 1 point par troncs
    T=len(extremite(grille_tour_n,player)[0])
    A=0
    for k in range(3):
        T+=len(extremite(grille_tour_n,player)[k+1])/2

    #compte taille des troncs
    for k in range(len(taille_troncsX(grille_tour_n,player))):
        T+=2**taille_troncsX(grille_tour_n,player)[k] #jsp si c'est la meilleure notation, à tester

    for k in range(len(taille_troncsY(grille_tour_n,player))):
        A+=2**taille_troncsY(grille_tour_n,player)[k]
    T+=A/2
    A=0
    for k in range(len(taille_troncspentepos(grille_tour_n,player))):
        A+=2**taille_troncspentepos(grille_tour_n,player)[k]
    T+=A/2
    A=0
    for k in range(len(taille_troncspenteneg(grille_tour_n,player))):
        A+=2**taille_troncspenteneg(grille_tour_n,player)[k]
    T+=A/2
    return T


def bien_def(i,j, n):
     #vérifie qu'une coordonée est bien définie
    if i>=n:
        return False
    if i<0:
        return False
    if j>=n:
        return False
    if j<0:
        return False
    return True




def extremite(grille_tour_n,player):
    L=[]

    #cherche les débuts et axes de troncs, pour pouvoir les compter ensuite
    troncs_X=[] #extrémités de troncs d'axe x
    troncs_Y=[]
    troncs_pentepos=[] # extrémités de troncs de pente positive
    troncs_penteneg=[]
    n = len(grille_tour_n[0])
    for i in range(n):
        for j in range(n):
            a=[i,j]
            if grille_tour_n[i][j]==player:

                #cherche si c'est un tronc d'axe X

                if bien_def(i,j+1, n):
                    if grille_tour_n[i][j+1] ==player:
                        troncs_X.append(a)

                #cherche si c'est un tronc d'axe Y en tenant compte des cas d'extrémités
                if bien_def(i+1,j, n)==False or ( bien_def(i+1,j, n)==True and grille_tour_n[i+1][j] ==0):
                    if grille_tour_n[i-1][j] ==player:
                        troncs_Y.append(a)

                if bien_def(i+1,j, n)==True and grille_tour_n[i+1][j] ==player:
                    if bien_def(i-1,j, n)==False or ( bien_def(i-1,j, n)==True and grille_tour_n[i-1][j] ==0):
                        troncs_Y.append(a)

                #cherche si c'est un tronc de pente positive
                if  bien_def(i-1,j+1, n)==False or ( bien_def(i-1,j+1, n)==True and grille_tour_n[i-1][j+1] ==0):
                    if grille_tour_n[i+1][j-1] ==player:
                        troncs_pentepos.append(a)

                if bien_def(i-1,j+1, n)==True and grille_tour_n[i-1][1+j] ==player:
                    if bien_def(i+1,j-1, n)==False or ( bien_def(i+1,j-1, n)==True and grille_tour_n[i+1][j-1] ==0):
                        troncs_Y.append(a)


                #cherche si c'est un tronc de pente négative
                if  bien_def(i-1,j-1, n)==False or ( bien_def(i-1,j-1, n)==True and grille_tour_n[i-1][j-1] ==0):
                    if grille_tour_n[i+1][j+1] ==player:
                        troncs_pentepos.append(a)

                if bien_def(i-1,j-1, n)==True and grille_tour_n[i-1][1-j] ==player:
                    if bien_def(i+1,j+1, n)==False or ( bien_def(i+1,j+1, n)==True and grille_tour_n[i+1][j+1] ==0):
                        troncs_Y.append(a)

                #crée la liste de tous les couples, qui se présente sous la forme L=[ tronc_X,tronc_Y,tronc_pentepos,tronc_penteneg]
                L.append(troncs_X)
                L.append(troncs_Y)
                L.append(troncs_pentepos)
                L.append(troncs_penteneg)

                return L





def taille_troncsX(grille_tour_n,player):
    #compte la taille des troncs d'axe X
    L=[0]
    n = len(grille_tour_n[0])
    troncs_X=extremite(grille_tour_n,player)[0]
    for k in range(len(troncs_X)):
        i=troncs_X[k][0]
        j=troncs_X[k][1]
        a=0
        while bien_def(i,j+1, n) and grille_tour_n[i][j+1]==1:
            t+=1
            a+=1
        L.append(a)
    return L




def taille_troncsY(grille_tour_n,player):
    #compte la taille des troncs associés un couple d'extrémités d'axe Y
    L=[0]
    n = len(grille_tour_n[0])
    troncs_Y=extremite(grille_tour_n,player)[1]
    for k in range(len(troncs_X)):
        i=troncs_Y[k][0]
        j=troncs_Y[k][1]
        a=0
        extrem_finale=[0,0]
        while bien_def(i+1,j, n) and grille_tour_n[i+1][j]==player:#on regarde si le tronc descend
            a+=1
            i+=1
        extrem_finale=[i,j]
        if a==0:
            i=troncs_Y[k][0]
            j=troncs_Y[k][1]
            while bien_def(i-1,j, n) and grille_tour_n[i-1][j]==player:#ou s'il monte
                a+=1
                i-=1
            extrem_finale=[i,j]

        couple=[troncs_Y[k],extrem_finale]
        L.append([couple,a])
    return L


def taille_troncspentepos(grille_tour_n,player):
    #compte la taille des troncs qui ont une pente diagonale positive associés un couple d'extrémités
    L=[0]
    n = len(grille_tour_n[0])
    troncs=extremite(grille_tour_n,player)[2]
    for k in range(len(troncs_X)):
        i=troncs[k][0]
        j=troncs[k][1]
        a=0
        extrem_finale=[0,0]
        while bien_def(i-1,j+1, n) and grille_tour_n[i-1][j+1]==player:#on regarde si le tronc monte
            a+=1
            i+=1
        extrem_finale=[i,j]
        if a==0:
            i=troncs[k][0]
            j=troncs[k][1]
            while bien_def(i+1,j-1, n) and grille_tour_n[i+1][j-1]==player:#ou s'il descend
                a+=1
                i-=1
            extrem_finale=[i,j]

        couple=[troncs[k],extrem_finale]
        L.append([couple,a])
    return L


def taille_troncspenteneg(grille_tour_n,player):
    #compte la taille des troncs qui ont une pente diagonale négative associés à un couple d'extrémités
    L=[0]
    n = len(grille_tour_n[0])
    troncs=extremite(grille_tour_n,player)[3]
    for k in range(len(troncs_X)):
        i=troncs[k][0]
        j=troncs[k][1]
        a=0
        extrem_finale=[0,0]
        while bien_def(i-1,j-1, n) and grille_tour_n[i-1][j-1]==player:#on regarde si le tronc monte
            a+=1
            i+=1
        extrem_finale=[i,j]
        if a==0:
            i=troncs[k][0]
            j=troncs[k][1]
            while bien_def(i+1,j+1, n) and grille_tour_n[i+1][j+1]==player:#ou s'il descend
                a+=1
                i-=1
            extrem_finale=[i,j]

        couple=[troncs[k],extrem_finale]
        L.append([couple,a])
    return L
