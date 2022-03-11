MONTECARLO_DEPTH = 10
MONTECARLO_NUM = 10
MINIMAX_DEPTH = 1

from random import randint, choice
from copy import deepcopy
from grid_manipulation import miniGrilleToGrille, grilleToMiniGrille, rotate_minigrid

def get_move(g, side, struct, eval):
    return function_map["struct"][list(function_map["struct"].keys())[struct]](g, side, function_map["eval"][list(function_map["eval"].keys())[eval]])

def filt(c):
        if g[c[0]][c[1]] == 0:
            return True
        else:
            return False

def bien_def(i,j, n):
    if i>=n:
        return False
    if i<0:
        return False
    if j>=n:
        return False
    if j<0:
        return False
    return True

### STRUCTURES D'IA ###
def s_evaluation (g, side, eval):
    g = deepcopy(g)
    best_pos = [0, 0]
    best_score = -100*abs(eval(g, side))
    best_rot = [0, 0]
    for x in range(len(g)):
        for y in range(len(g)):
            if g[x][y] != 0:
                continue
            for n in range(4):
                for s in range(2):
                    g[x][y] = side
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], s)
                    g = miniGrilleToGrille(mg)
                    score = eval(g, side)
                    if score > best_score:
                        best_pos = [x, y]
                        best_rot = [n, s]
                        best_score = score
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], (s + 1)%2)
                    g = miniGrilleToGrille(mg)
                    g[x][y] = 0
    return [best_pos, best_rot]

def s_montecarlo (g, side, eval):
    g = deepcopy(g)
    size = len(g)
    coups = [[m//size, m%size] for m in range(size**2)]
    rots = [[m//2, m%2] for m in range(8)]
    best_pos = [0, 0]
    best_score = -100*abs(eval(g, side))
    best_rot = [0, 0]
    for x in range(size):
        for y in range(size):
            if g[x][y] != 0:
                continue
            for n in range(4):
                for s in range(2):
                    g[x][y] = side
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], s)
                    g = miniGrilleToGrille(mg)
                    sum = 0
                    for i in range(MONTECARLO_NUM):
                        hist = []
                        _side = 2- (side + 1)%2
                        for j in range(MONTECARLO_DEPTH):
                            posspos = list(filter(filt,coups))
                            if posspos == []: 
                                break
                            c = choice(posspos)
                            r = choice(rots)
                            g[c[0]][c[1]] = _side
                            mg = grilleToMiniGrille(g)
                            mg[r[0]] = rotate_minigrid(mg[r[0]], r[1])
                            g = miniGrilleToGrille(mg)
                            _side = 2- (_side + 1)%2
                            hist.append([c, r])
                        sum += eval(g, side)
                        while hist != []:
                            coup = hist.pop()
                            mg = grilleToMiniGrille(g)
                            mg[coup[1][0]] = rotate_minigrid(mg[coup[1][0]], (coup[1][1] + 1)%2)
                            g = miniGrilleToGrille(mg)
                            g[coup[0][0]][coup[0][1]] = 0
                    if sum > best_score:
                        best_pos = [x, y]
                        best_rot = [n, s]
                        best_score = sum
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], (s + 1)%2)
                    g = miniGrilleToGrille(mg)
                    g[x][y] = 0
    return [best_pos, best_rot]

def s_min (g, side, eval, depth):
    size = len(g)
    pire_coup = False
    pire_evaluation = False
    for x in range(size):
        for y in range(size):
            for n in range(4):
                for s in range(2):
                    g[x][y] = side
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], s)
                    g = miniGrilleToGrille(mg)
                    if depth == 0: s = eval(g, side)
                    else: s = s_max(g, 2- (side+1)%2, eval, depth - 1)[0]
                    if (not pire_coup) or (s < pire_evaluation):
                        pire_coup = [[x, y], [n, s]]
                        pire_evaluation = s
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], (s + 1)%2)
                    g = miniGrilleToGrille(mg)
                    g[x][y] = 0
    return pire_evaluation, pire_coup

def s_max(g, side, eval, depth):
    size = len(g)
    meilleur_coup = False
    meilleur_evaluation = False
    for x in range(size):
        for y in range(size):
            for n in range(4):
                for s in range(2):
                    g[x][y] = side
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], s)
                    g = miniGrilleToGrille(mg)
                    if depth == 0: s = eval(g, side)
                    else: s = s_min(g, 2- (side+1)%2, eval, depth - 1)[0]
                    if (not meilleur_coup) or (s < meilleur_evaluation):
                        meilleur_coup = [[x, y], [n, s]]
                        meilleur_evaluation = s
                    mg = grilleToMiniGrille(g)
                    mg[n] = rotate_minigrid(mg[n], (s + 1)%2)
                    g = miniGrilleToGrille(mg)
                    g[x][y] = 0
    return meilleur_evaluation, meilleur_coup

def s_minimax (g, side, eval):
    return s_max(deepcopy(g), side, eval, MINIMAX_DEPTH)[1]

### FONCTIONS D'EVALUATION ###
def fe_alea (g, side):
    return randint(0, 400)

def fe_ordonee (g, side):
    return 0

def fe_naive (g, side):
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
            for k in autours:
                for l in autours:
                    if not bien_def(i+k, j+l, n): continue
                    if g[i][j] == g[i+k][j+l]: score += value
    return score

def fe_naive_aggressive (g, side):
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
            for k in autours:
                for l in autours:
                    if not bien_def(i+k, j+l, n): continue
                    if g[i][j] == g[i+k][j+l]: score += value
    return score

def fe_naive_defensive (g, side):
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
            for k in autours:
                for l in autours:
                    if not bien_def(i+k, j+l, n): continue
                    if g[i][j] == g[i+k][j+l]: score += value
    return score

function_map = {
    "eval": {
        "naive": fe_naive,
        "alea": fe_alea,
        "aggressive": fe_naive_aggressive,
        "defensive": fe_naive_defensive,
        "ordonee": fe_ordonee
    },
    "struct": {
        "evaluation": s_evaluation,
        "montecarlo": s_montecarlo,
        "minimax": s_minimax
    }
}