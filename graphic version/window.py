import tkinter as tk
from game import Game
from math import floor
from functools import partial
from grid_manipulation import reverse

colors = {
    "0": "#ffeead",
    "2": "#ff6f69",
    "1": "#88d8b0",
    "lines": "#ffcc5c",
    "arrows": "#9b9b9b"
}

def make_arrow (window, frame, sens, place):
    arrow = tk.Button(
        frame, 
        command=partial(window.game.grid_rotate, place, sens),
        activebackground=window.colors["arrows"],
        bg=window.colors["arrows"],
        relief=tk.FLAT,
        borderwidth=0
    )
    return arrow

def make_player_choice (window, frame, side, w):
    button = tk.Button(
        frame, 
        activebackground=window.colors[str(side)],
        bg=window.colors[str(side)],
        relief=tk.FLAT,
        text="Joueur",
        borderwidth=0,
        font=(window.params["police"], floor(w/8))
    )
    button.configure(command=partial(window.game.change_player_choice, side, button))
    return button

def make_struct_choice (window, frame, side, w):
    button = tk.Button(
        frame, 
        activebackground=window.colors[str(side)],
        bg=window.colors[str(side)],
        relief=tk.FLAT,
        text="Structure:\nevaluation",
        borderwidth=0,
        font=(window.params["police"], floor(w/10))
    )
    button.configure(command=partial(window.game.change_struct_choice, side, button))
    return button

def make_eval_choice (window, frame, side, w):
    button = tk.Button(
        frame, 
        activebackground=window.colors[str(side)],
        bg=window.colors[str(side)],
        relief=tk.FLAT,
        text="Evaluation:\nnaive",
        borderwidth=0,
        font=(window.params["police"], floor(w/10))
    )
    button.configure(command=partial(window.game.change_eval_choice, side, button))
    return button

def back(window):
    if len(window.game.historique) <= 1: return
    coup = window.game.historique.pop()
    window.game.grid = reverse(window.game.grid, coup)
    if len(coup) > 1:
        window.game.turn = [2- (window.game.turn[0] + 1)%2, 0]
    else:
        window.game.turn[1] = 0
    window.game.grid_update()

def restart(window):
    size = window.params["size"]
    window.game.historique = [[]]
    window.game.grid = [[0 for i in range(size)] for j in range(size)]
    window.game.turn = [1,0]
    if window.won != None:
        window.won[0].destroy()
        window.won[1].destroy()
    window.game.grid_update()

class Window:
    def __init__(self, params):
        self.canvas = tk.Tk()
        self.won = None
        self.canvas.minsize(params["width"], params["height"])
        self.canvas.maxsize(params["width"], params["height"])
        self.params = params
        self.colors = colors
        self.game = Game(self)
        self.arrows_init()
        self.turn_label_init()
        self.sepline_init()
        self.hist_init()
        self.player_choice_init()
        self.ia_choice_init()
        self.reverse_init()
        self.restart_init()
        self.canvas.mainloop()

    def cell_size(self):
        return min(floor((2*self.params["width"]/3 - 2*self.params["size"])/(self.params["size"]+2.5)), floor((self.params["height"] - 2*self.params["size"])/(self.params["size"]+2.5)))

    def widget_in_frame (self, widget, frame, x, y, place = True):
        frame.grid_propagate(False)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0,weight=1)
        widget.grid(sticky="wens")
        if place: frame.place(x=x, y=y)

    def turn_label_init(self):
        x = 17*self.params["width"]/24
        w = self.params["width"]/4
        h = self.params["height"]/10
        frame = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["1"])
        self.turn_label = tk.Label(
            frame,
            bg=self.colors["1"],
            text="Tour du Joueur 1\nPosez un pion",
            borderwidth=0,
            font=(self.params["police"], floor(w/17))
        )
        self.widget_in_frame(self.turn_label, frame, x, h/2)

    def sepline_init(self):
        x = 2*self.params["width"]/3
        frame = tk.Frame(self.canvas, width=1, height=self.params["height"], bg=self.colors["arrows"])
        frame.place(x=x, y=0)

    def arrows_init(self):
        size = self.cell_size()
        grid_size = self.params["size"] * (size + 4)
        for i in range(2):
            for j in range(2):
                frame0 = tk.Frame(self.canvas, width=size, height=size/2, bg=self.colors["arrows"])
                frame1 = tk.Frame(self.canvas, width=size/2, height=size, bg=self.colors["arrows"])
                y0 = (self.params["height"] - grid_size)/2 + (grid_size + size)*i - 3*size/4
                x0 = (2*self.params["width"]/3 - grid_size)/2 + size/2 + (grid_size - 2*size)*j
                x1 = (2*self.params["width"]/3 - grid_size)/2 + (grid_size + size)*i - 3*size/4
                y1 = (self.params["height"] - grid_size)/2 + size/2 + (grid_size - 2*size)*j
                arrow0 = make_arrow(self, frame0, (i+j) % 2, i*2 + j)
                arrow1 = make_arrow(self, frame1, (i+j+1) % 2, j*2 + i)
                self.widget_in_frame(arrow0, frame0, x0, y0)
                self.widget_in_frame(arrow1, frame1, x1, y1)

    def player_choice_init(self):
        x1 = 17*self.params["width"]/24
        x2 = x1 + 3*self.params["width"]/20
        w = self.params["width"]/10
        h = self.params["height"]/10
        frame1 = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["1"])
        b1 = make_player_choice(self, frame1, 1, w)
        self.widget_in_frame(b1, frame1, x1, h*2)
        frame2 = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["2"])
        b2 = make_player_choice(self, frame2, 2, w)
        self.widget_in_frame(b2, frame2, x2, h*2)

    def ia_choice_init(self):
        x1 = 17*self.params["width"]/24
        x2 = x1 + 3*self.params["width"]/20
        w = self.params["width"]/10
        h = self.params["height"]/10
        sframe1 = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["1"])
        sb1 = make_struct_choice(self, sframe1, 1, w)
        self.widget_in_frame(sb1, sframe1, x1, h*3.5)
        sframe2 = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["2"])
        sb2 = make_struct_choice(self, sframe2, 2, w)
        self.widget_in_frame(sb2, sframe2, x2, h*3.5)
        eframe1 = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["1"])
        eb1 = make_eval_choice(self, eframe1, 1, w)
        self.widget_in_frame(eb1, eframe1, x1, h*5)
        eframe2 = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["2"])
        eb2 = make_eval_choice(self, eframe2, 2, w)
        self.widget_in_frame(eb2, eframe2, x2, h*5)

    def reverse_init(self):
        x = 17*self.params["width"]/24     
        w = self.params["width"]/10
        h = self.params["height"]/10   
        frame = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["lines"])
        b = tk.Button(
            frame, 
            command=partial(back, self),
            activebackground=self.colors["lines"],
            bg=self.colors["lines"],
            relief=tk.FLAT,
            text="Retour\narriere",
            borderwidth=0,
            font=(self.params["police"], floor(w/8))
        )
        self.widget_in_frame(b, frame, x, h*8)

    def restart_init(self):
        x = 17*self.params["width"]/24 + 3*self.params["width"]/20    
        w = self.params["width"]/10
        h = self.params["height"]/10   
        frame = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["lines"])
        b = tk.Button(
            frame, 
            command=partial(restart, self),
            activebackground=self.colors["lines"],
            bg=self.colors["lines"],
            relief=tk.FLAT,
            text="Recom-\n-mencer",
            borderwidth=0,
            font=(self.params["police"], floor(w/8))
        )
        self.widget_in_frame(b, frame, x, h*8)

    def hist_init(self):
        x = 17*self.params["width"]/24    
        w = self.params["width"]/4
        h = self.params["height"]/10   
        frame = tk.Frame(self.canvas, width=w, height=h, bg=self.colors["lines"])
        self.Ghist = tk.Label(
            frame, 
            activebackground=self.colors["lines"],
            bg=self.colors["lines"],
            relief=tk.FLAT,
            text="Personne n'a encore joué",
            borderwidth=0,
            font=(self.params["police"], floor(w/25))
        )
        self.widget_in_frame(self.Ghist, frame, x, h*6.5)

    def win(self, side):
        h = 2*self.params["height"]//5
        w = 4*self.params["width"]//5
        frame = tk.Frame(self.canvas, width=w, height=h)
        y = 3*self.params["height"]//10
        x = 1*self.params["width"]//10
        winscreen = tk.Label(
            frame, 
            bg=self.colors[str(side)], 
            fg="black", 
            text="player " + str(side) + " won",
            borderwidth=0,
            font=(self.params["police"], w//13)
        )
        self.won = [winscreen, frame]
        self.widget_in_frame(winscreen, frame, x, y)