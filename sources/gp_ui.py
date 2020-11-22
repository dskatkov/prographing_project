import tkinter as tk
import tkinter.font
import time

import gp_source_file as gp_source_file
import gp_canvas as gp_canvas
from gp_mouse_binding import *
from settings import *
from utils import *

# canvas - tk.Canvas
canvasFrame = panelFrame = stateFrame = canvas = mainWindow = ...

def saveAs(root):
    """Обработчик кнопки save as"""
    fileName = tk.filedialog.SaveAs(root, filetypes = [("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        if not fileName.endswith('.vrc'):
            fileName += '.vrc'
        gp_source_file.SF.save(fileName)

def save(root):
    """Обработчик кнопки save"""
    if gp_source_file.SF.fileName == '':
        saveAs(root)
    else:
        gp_source_file.SF.save(gp_source_file.SF.fileName)

def open(root):
    """Обработчик кнопки open"""
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

    """Обработчик кнопки build"""
    if gp_source_file.SF.buildName == '':
        buildAs(root)
    else:
        gp_source_file.SF.build(gp_source_file.SF.buildName)

def buildAs(root):
    """Обработчик кнопки build as"""
    ext = '.b.'+gp_source_file.SF.lang
    fileName = tk.filedialog.SaveAs(root, filetypes = [("Source code", ext)]).show()
    if fileName == '':
        return
    else:
        debug_return ('Building to '+fileName)
        if not fileName.endswith(ext):
            fileName += ext
        gp_source_file.SF.build(fileName)

def newFile(root=None):
    """Обработчик кнопки new file"""
    gp_source_file.SF = gp_source_file.SourceFile()
    gp_canvas.canvas.draw(gp_source_file.SF)



def ui_init(root):
    """Инициализирует UI: кнопки + обработчики"""
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



    mainMenu_tree = {
        "Файл": {
            "Новый файл": lambda: print('new file, not implemented'),
            "Открыть...": lambda: print('open, not implemented'),
            "Сохранить": lambda: print('save, not implemented'),
            "Сохранить как...": lambda: print('save as, not implemented'),
        },
        "Сборка": {
            "Собрать исходник": lambda: print('build, not implemented'),
        },
        "Выход": lambda: print('exit, not implemented'),
        "Язык": {
            "py": lambda: print('py file, not implemented'),
            "c": lambda: print('c file, not implemented'),
            "pas": lambda: print('pas file, not implemented'),
        },
    }
    mainMenu = tk.Menu(master=root)
    createMenu(mainMenu, mainMenu_tree)
    root.config(menu=mainMenu)

    assign_canvasFrame(canvasFrame)

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
    debug_return("This module is not for direct call!")
