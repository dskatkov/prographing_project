import tkinter as tk
import tkinter.font
import time

from settings import *
from utils import *
import gp_source_file as gp_source_file
import gp_canvas as gp_canvas

canvasFrame = panelFrame = stateFrame = canvas = ...

def saveAs(root):
    fileName = tk.filedialog.SaveAs(root, filetypes = [("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        if not fileName.endswith('.vrc'):
            fileName += '.vrc'
        gp_source_file.SF.save(fileName)

def save(root):
    if gp_source_file.SF.fileName == '':
        saveAs(root)
    else:
        gp_source_file.SF.save(gp_source_file.SF.fileName)

def open(root):
    fileName = tk.filedialog.Open(root, filetypes = [("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        if not fileName.endswith('.vrc'):
            fileName += '.vrc'
        gp_source_file.SF.open(fileName)
        gp_canvas.canvas.draw(gp_source_file.SF)

def build(root):
    if gp_source_file.SF.buildName == '':
        buildAs(root)
    else:
        gp_source_file.SF.build(gp_source_file.SF.buildName)

def buildAs(root):
    ext = '.'+gp_source_file.SF.lang
    fileName = tk.filedialog.SaveAs(root, filetypes = [("Source code", ext)]).show()
    if fileName == '':
        return
    else:
        if not fileName.endswith(ext):
            fileName += ext
        gp_source_file.SF.build(fileName)

def newFile(root=None):
    gp_source_file.SF = gp_source_file.SourceFile()
    gp_canvas.canvas.draw(gp_source_file.SF)

'''
Work with mouse begins. It is not Finished yet
'''


def click_hit(click):
    print(f'handling click: ({click.x},{click.y})')
    for _, block in gp_source_file.SF.object_ids.items():
        print('checking block: '+block.convertToStr())
        distance2 = (block.pos[0] - click.x) ** 2 + (block.pos[1] - click.y) ** 2
        if distance2 <= 10 ** 2:
            print('ok')
            return block

def b1_double(click):
    print ('left double click')
    block = click_hit(click)
    if block:
        if not block.text_editor:
            block.edit(tk.Toplevel(canvasFrame))
    else:
        block = gp_source_file.Block(gp_source_file.SF)
        block.pos = (click.x, click.y)
    gp_canvas.canvas.draw(gp_source_file.SF)

def b3_double(click):
    print ('right double click')

def button1(click):
    print ('left click')

def button3(click):
    print ('right click')

def b1_motion(click):
    print (f'left motion:({click.x},{click.y})')

def b3_motion(click):
    print (f'right motion:({click.x},{click.y})')

'''
Here work with mouse ended. spacetime is going back to normal
'''

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
    canvas.pack(expand=1)

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
        ('canvas redraw', lambda: gp_canvas.canvas.draw(gp_source_file.SF)),
        ('build log', lambda: gp_source_file.SF.build('', 0)),
        ('save log', lambda: gp_source_file.SF.save('', 0)),

    ]
    placeButtons(panelFrame, panelFrameButtons)

    mainMenu = tk.Menu(master=root)
    createMenu(mainMenu, mainMenu_tree)
    root.config(menu=mainMenu)

    canvas.bind("<Double-Button-1>", b1_double)
    canvas.bind("<Double-Button-2>", ...)
    canvas.bind("<Double-Button-3>", b3_double)
    canvas.bind("<Button-1>", button1)
    canvas.bind("<Button-2>", ...)
    canvas.bind("<Button-3>", button3)
    canvas.bind("<B1-Motion>", b1_motion)
    canvas.bind("<B2-Motion>", ...)
    canvas.bind("<B3-Motion>", b3_motion)
    # canvas.bind("<B1-Release>", b1_motion)
    # canvas.bind("<B2-Release>", ...)
    # canvas.bind("<B3-Release>", b3_motion)


if __name__ == "__main__":
    print("This module is not for direct call!")
