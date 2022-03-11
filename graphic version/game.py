import tkinter as tk
from functools import partial
from IA import get_move, function_map
from grid_manipulation import miniGrilleToGrille, grilleToMiniGrille, rotate_minigrid

def is_winning (g, side):
    '''Savoir si le side gagne sur la g'''
    lg = len(g)
    for i in range(lg):
        if is_winning_column(g[i], side):
            return True
        if is_winning_column([c[i] for c in g], side):
            return True
    if is_winning_column([g[i][i] for i in range(lg)], side):
        return True
    if is_winning_column([g[i][lg-1-i] for i in range(lg)], side):
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

def is_winning_column (col, side):
    l = len(col) - 1
    if col[0] != side and col[l] != side:
        return False
    for i in range(1, l):
        if col[i] != side:
            return False
    return True

def click_grid (game, x, y):
    if game.turn[1] != 0:
        return
    if game.grid[x][y] != 0:
        return
    game.grid[x][y] = game.turn[0]
    if is_winning(game.grid, game.turn[0]):
        game.window.win(game.turn[0])
    game.turn[1] = 1
    game.historique.append([[x,y]])
    game.grid_update()

def make_cell (game, x, y):
    size = game.window.cell_size()
    frame = tk.Frame(game.Ggrid, width=size, height=size)
    cell = tk.Button(
        frame, 
        command= partial(click_grid, game, x, y),
        activebackground=game.window.colors["0"],
        bg=game.window.colors["0"],
        relief=tk.FLAT,
        borderwidth=0
    )
    game.window.widget_in_frame(cell, frame, x, y, False)
    frame.grid(row=x, column=y, padx=2, pady=2)
    return cell
    
class Game:
    def __init__(self, window):
        self.window = window
        self.grid_init()
        self.turn = [1, 0]
        self.is_ia = [False, False]
        self.ia_structure = [0, 0]
        self.ia_evaluation = [0, 0] 
        self.historique = [[]]
    
    def grid_init(self):
        size = self.window.params["size"]
        grid_size = self.window.params["size"] * (self.window.cell_size() + 4)
        self.Ggrid = tk.Frame(master=self.window.canvas, width=grid_size, height=grid_size, bg=self.window.colors["lines"])
        self.Ggrid.grid_propagate(False)
        self.grid = [[0 for i in range(size)] for j in range(size)]
        self.Gcells = [[make_cell(self, i, j) for i in range(size)] for j in range(size)]
        y = (self.window.params["height"] - grid_size)/2
        x = (2*self.window.params["width"]/3 - grid_size)/2
        self.Ggrid.place(x=x, y=y)

    def grid_update(self):
        size = self.window.params["size"]
        for i in range(size):
            for j in range(size):
                    self.Gcells[j][i].configure(bg = self.window.colors[str(self.grid[i][j])])
        self.window.turn_label.configure(bg=self.window.colors[str(self.turn[0])],text="Tour du Joueur {0}\n{1}".format(self.turn[0], ("Posez un pion", "Tournez une grille")[self.turn[1]]))
        if self.historique[-1] == []:
            self.window.Ghist.config(text="Personne n'a\nencore joué")
        else:
            last = self.historique[-1]
            l = "Coup en {0}, {1}".format(last[0][0] + 1, last[0][1] + 1)
            if len(last) > 1:
                l += "\nGrille {0} tournée dans le sens {1}".format(last[1][0], last[1][1])
            self.window.Ghist.config(text=l)

    def grid_rotate(self, num, sens):        
        if self.turn[1] != 1:
            return    
        self.turn[1] = 0
        self.historique[-1].append([num, sens])
        mg = grilleToMiniGrille(self.grid)
        mg[num] = rotate_minigrid(mg[num], sens)
        self.grid = miniGrilleToGrille(mg)
        if is_winning(self.grid, self.turn[0]):
            self.window.win(self.turn[0])
        self.turn[0] = (2,1)[self.turn[0] - 1]
        self.grid_update()
        if self.is_ia[self.turn[0] - 1]:
            self.play_IA()

    def play_IA(self):
        if self.turn[1] != 0:
            return
        move = get_move(self.grid, self.turn[0], self.ia_structure[self.turn[0]-1], self.ia_evaluation[self.turn[0]-1])
        click_grid(self, move[0][0], move[0][1])
        self.grid_rotate(move[1][0], move[1][1])

    def change_player_choice (self, side, b):
        if self.is_ia[side-1]:
            self.is_ia[side-1] = False
            b.configure(text="Joueur")
        else:
            self.is_ia[side-1] = True
            b.configure(text="IA")
            if self.turn[0] == side and self.turn[1] == 0:
                self.play_IA()

    def change_struct_choice (self, side, b):
        self.ia_structure[side-1] += 1
        if self.ia_structure[side-1] >= len(function_map["struct"].keys()):
            self.ia_structure[side-1] = 0
        b.configure(text="Structure:\n{0}".format(list(function_map["struct"].keys())[self.ia_structure[side-1]]))
    
    def change_eval_choice (self, side, b):
        self.ia_evaluation[side-1] += 1
        if self.ia_evaluation[side-1] >= len(function_map["eval"].keys()):
            self.ia_evaluation[side-1] = 0
        b.configure(text="Evaluation:\n{0}".format(list(function_map["eval"].keys())[self.ia_evaluation[side-1]]))