import tkinter as tk
import tkinter.font

from settings import *
import gp_source_file as gp_source_file
import gp_canvas as gp_canvas

canvasFrame, panelFrame, stateFrame, canvas = ..., ..., ..., ...

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
        gp_source_file.SF.save(fileName)

def save(root):
    if gp_source_file.SF.fileName == "":
        saveAs(root)
    else:
        gp_source_file.SF.save(gp_source_file.SF.fileName)

def open(root):
    fileName = tk.filedialog.Open(root, filetypes = [("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        gp_source_file.SF.open(fileName)
        gp_canvas.canvas.draw(gp_source_file.SF)

def buildAs(root):
    fileName = tk.filedialog.SaveAs(root, filetypes = [("Source code", ".py")]).show()
    if fileName == '':
        return
    else:
        gp_source_file.SF.build(fileName)

def build(root):
    if gp_source_file.SF.buildName == "":
        buildAs(root)
    else:
        gp_source_file.SF.build(gp_source_file.SF.fileName)

def newFile(root=None):
    gp_source_file.SF = SourceFile()
    gp_canvas.canvas.draw(gp_source_file.SF)

def ui_init(root):
    global canvasFrame, panelFrame, stateFrame, canvas
    root.minsize(200, 200)

    root.columnconfigure(0, weight=1, minsize=200)
    root.rowconfigure([0,2], weight=0, minsize=20)
    root.rowconfigure(1, weight=1, minsize=100)

    panelFrame = tk.Frame(master=root, bg=panelBG)
    canvasFrame = tk.Frame(master=root, bg=textBG)
    stateFrame = tk.Frame(master=root, bg=stateBG)
    canvas = tk.Canvas(master=canvasFrame, bg=textBG)
    canvas.pack()

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

    # mainMenu = tk.Menu(master=root)
    # createMenu(mainMenu, mainMenu_tree)
    # root.config(menu=mainMenu)

    canvasFrame.bind("<Button-1>", ...)
    canvasFrame.bind("<Button-2>", ...)
    canvasFrame.bind("<Button-3>", ...)
    canvasFrame.bind("<B1-Motion>", ...)
    canvasFrame.bind("<B2-Motion>", ...)
    canvasFrame.bind("<B3-Motion>", ...)

if __name__ == "__main__":
    print("This module is not for direct call!")
