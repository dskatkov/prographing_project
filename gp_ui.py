import tkinter as tk
import tkinter.font

from settings import *
from gp_source_file import *

canvasFrame, panelFrame, stateFrame = ..., ..., ...

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

def saveAs(root):
    fileName = tk.filedialog.SaveAs(root, filetypes = [("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        # if not fileName.endswith(".txt"):
        #     fileName += ".txt"
        SF.save(fileName)

def save(root):
    if SF.fileName == "":
        saveAs(root)
    else:
        SF.save(SF.fileName)

def open(root):
    fileName = tk.filedialog.Open(root, filetypes = [("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        SF.open(fileName)

def buildAs(root):
    fileName = tk.filedialog.SaveAs(root, filetypes = [("Source code", ".py")]).show()
    if fileName == '':
        return
    else:
        SF.build(fileName)

def build(root):
    if SF.buildName == "":
        buildAs(root)
    else:
        SF.build(SF.fileName)

def newFile(root):
    SF = SourceFile()

def ui_init(root):
    global canvasFrame, panelFrame, stateFrame
    root.minsize(200, 200)

    root.columnconfigure(0, weight=1, minsize=200)
    root.rowconfigure([0,2], weight=0, minsize=20)
    root.rowconfigure(1, weight=1, minsize=100)

    panelFrame = tk.Frame(master=root, bg=panelBG)
    canvasFrame = tk.Frame(master=root, bg=textBG)
    stateFrame = tk.Frame(master=root, bg=stateBG)

    panelFrame.grid(row=0, column=0, sticky='nsew')
    canvasFrame.grid(row=1, column=0, sticky='nsew')
    stateFrame.grid(row=2, column=0, sticky='nsew')

    panelFrameButtons = [
        ('new', lambda: newFile(root)),
        ('open', lambda: open(root)),
        ('save', lambda: save(root)),
        ('save as', lambda: saveAs(root)),
        ('build', lambda: build(root)),
        ('build as', lambda: buildAs(root)),

    ]
    placeButtons(panelFrame, panelFrameButtons)

    mainMenu = tk.Menu(master=root)
    createMenu(mainMenu, mainMenu_tree)
    root.config(menu=mainMenu)

    canvasFrame.bind("<Button-1>", ...)
    canvasFrame.bind("<Button-2>", ...)
    canvasFrame.bind("<Button-3>", ...)
    canvasFrame.bind("<B1-Motion>", ...)
    canvasFrame.bind("<B2-Motion>", ...)
    canvasFrame.bind("<B3-Motion>", ...)

if __name__ == "__main__":
    print("This module is not for direct call!")
