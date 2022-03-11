def grilleToMiniGrille(g):
    L1,L2,L3,L4=[],[],[],[]
    n = len(g)
    for i in range(n):
        if i<n//2:
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

def rotate_minigrid (g, sens):
    n = len(g)
    tourne=[[0 for k in range(n)] for j in range(n)]
    if sens==1:
        for i in range(n):
            for j in range(n):
                tourne[i][j]=g[j][n-1-i]
    elif sens==0:
        for i in range(n):
            for j in range(n):
                tourne[i][j]=g[n-1-j][i]
    return tourne

def reverse (g, coup):
    if coup == []: return g
    if len(coup) > 1:
        mg = grilleToMiniGrille(g)
        mg[coup[1][0]] = rotate_minigrid(mg[coup[1][0]], (coup[1][1] + 1)%2)
        g = miniGrilleToGrille(mg)
    g[coup[0][0]][coup[0][1]] = 0
    return g