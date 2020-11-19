import tkinter as tk
from settings import *

# class Point:
#     def __init__(self, x=0, y=0):
#         self.x = x
#         self.y = y

#     def __repr__(self):
#         return f"Point({self.x}, {self.y})"

#     def __str__(self):
#         return f"({self.x},{self.y})"

#     def fromStr(self, str):
#         self.x, self.y = eval(str)

#     def fromTuple(self, tpl):
#         self.x, self.y = tpl

def createMenu(master, tree):
    for key, val in tree.items():
        m = tk.Menu(master=master, tearoff=0)
        if type(val)==type({}):
            createMenu(m, val)
        else:
            master.add_command(label=key, command=val)
            continue
        master.add_cascade(label=key, menu=m)

def placeButtons(master, buttons, side='left', fg=btnFG, bg=btnBG):
    for btn in buttons:
        b = tk.Button(master=master, text=btn[0], command=btn[1], fg=btnFG, bg=btnBG)
        b.pack(side=side, padx=3, pady=3)


if __name__ == "__main__":
    print("This module is not for direct call!")
