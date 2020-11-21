import tkinter as tk
import tkinter.font
import time

from settings import *
from utils import *
import gp_source_file as gp_source_file
import gp_canvas as gp_canvas

# canvas - tk.Canvas
canvasFrame = panelFrame = stateFrame = canvas = mainWindow = ...

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
        mainWindow.title(fileName)


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
def redraw():
    gp_canvas.canvas.draw(gp_source_file.SF)

def find_block(click):
    print(f'handling click: ({click.x},{click.y})')
    sfclick = gp_canvas.canvas.unscale((click.x, click.y))
    for _, block in gp_source_file.SF.object_ids.items():
        print('checking block: '+block.convertToStr())
        distance2 = (block.pos[0] - sfclick[0]) ** 2 + (block.pos[1] - sfclick[1]) ** 2
        if distance2 <= 10 ** 2:
            print('ok')
            return block

b1_state = ''
b2_state = ''
b3_state = ''

def b1(click):
    b1_state = 'n'
    print (f'left click: ({click.x},{click.y})')
    block = find_block(click)
    if block:
        block.chosen = True
        gp_canvas.canvas.handling = block
        gp_canvas.canvas.touch = (click.x, click.y)
    redraw()

def b2(click):
    b2_state = 'n'
    print (f'wheel click: ({click.x},{click.y})')
    ...
    redraw()

def b3(click):
    b2_state = 'n'
    ...
    redraw()
    print (f'right click: ({click.x},{click.y})')


def b1_double(click):
    b1_state = 'd'
    print (f'left double click: ({click.x},{click.y})')

    block = find_block(click)
    if block:
        if not block.text_editor:
            block.edit(tk.Toplevel(canvasFrame), gp_canvas.canvas)
    else:
        block = gp_source_file.Block(gp_source_file.SF)
        block.pos = gp_canvas.canvas.unscale((click.x, click.y))

    redraw()

def b2_double(click):
    b2_state = 'd'
    print (f'wheel double click: ({click.x},{click.y})')
    ...
    redraw()

def b3_double(click):
    b3_state = 'd'
    print (f'right double click: ({click.x},{click.y})')
    ...
    redraw()


def b1_motion(click):
    b1_state = 'm'
    print (f'left motion: ({click.x},{click.y})')
    if gp_canvas.canvas.handling:
        shift = (click.x - gp_canvas.canvas.touch[0], click.y - gp_canvas.canvas.touch[1])
        gp_canvas.canvas.handling.move(shift)
        gp_canvas.canvas.touch = (click.x, click.y)
    redraw()

def b2_motion(click):
    b2_state = 'm'
    print (f'wheel motion:({click.x},{click.y})')
    ...
    redraw()

def b3_motion(click):
    b3_state = 'm'
    print (f'right motion:({click.x},{click.y})')
    ...
    redraw()


def b1_release(click):
    b1_state = ''
    print (f'left release:({click.x},{click.y})')
    ...
    redraw()

def b2_release(click):
    b2_state = ''
    print (f'wheel release:({click.x},{click.y})')
    ...
    redraw()

def b3_release(click):
    b3_state = ''
    print (f'right release:({click.x},{click.y})')
    ...
    redraw()


def wheel(click):
    print(f'wheel:({click.x},{click.y}) {click.delta}')
    k = 2.718281828459045 ** (0.1*click.delta/120)
    scale = gp_canvas.canvas.scale
    unscale = gp_canvas.canvas.unscale

    # Я не знаю, как и почему это работает, но оно работает (с какой-то погрешностью?!)
    pos = (click.x, click.y)
    pos = vecMul(pos, 1 / gp_canvas.canvas.viewzoom)
    sfpos = unscale(pos)
    gp_canvas.canvas.viewzoom *= k
    sfnewpos = unscale(pos)
    sfshift = vecSum(sfnewpos, vecMul(sfpos, -1))
    shift = vecMul(sfshift, -gp_canvas.canvas.viewzoom)
    gp_canvas.canvas.viewpos = vecSum(gp_canvas.canvas.viewpos, shift)

    redraw()

'''
Here work with mouse ended. spacetime is going back to normal
'''

def ui_init(root):
    global canvasFrame, panelFrame, stateFrame, canvas, mainWindow, chosen
    root.minsize(200, 200)

    root.columnconfigure(0, weight=1, minsize=200)
    root.rowconfigure([0,2], weight=0, minsize=20)
    root.rowconfigure(1, weight=1, minsize=100)

    panelFrame = tk.Frame(master=root, bg=panelBG)
    canvasFrame = tk.Frame(master=root, bg=textBG)
    stateFrame = tk.Frame(master=root, bg=stateBG)
    canvas = tk.Canvas(master=canvasFrame, bg=textBG)
    canvas.pack(fill='both', expand=1)

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

    canvas.bind("<Button-1>", b1)
    canvas.bind("<Button-2>", b2)
    canvas.bind("<Button-3>", b3)

    canvas.bind("<Double-Button-1>", b1_double)
    canvas.bind("<Double-Button-2>", b2_double)
    canvas.bind("<Double-Button-3>", b3_double)

    canvas.bind("<B1-Motion>", b1_motion)
    canvas.bind("<B2-Motion>", b2_motion)
    canvas.bind("<B3-Motion>", b3_motion)

    canvas.bind("<ButtonRelease-1>", b1_release)
    canvas.bind("<ButtonRelease-2>", b2_release)
    canvas.bind("<ButtonRelease-3>", b3_release)

    canvas.bind("<MouseWheel>", wheel)



if __name__ == "__main__":
    print("This module is not for direct call!")
