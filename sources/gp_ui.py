import tkinter as tk
# import tkinter.font
# import time

import gp_source_file as source_file
import gp_canvas as gp_canvas
from gp_mouse_binding import *
from settings import *
from utils import *
from panel_buttons_handler import*
canvasFrame = panelFrame = stateFrame = canvas = mainWindow = ...

consoleWindow = None

def ui_init(root):
    """Инициализирует UI: кнопки + обработчики/ initialize user interface: buttons + handlers"""
    global canvasFrame, panelFrame, stateFrame, canvas, mainWindow, chosen
    # Объект, умеющий рисовать наше поле/ object to draw the field
    gp_canvas.canvas = gp_canvas.Canvas()

    root.minsize(200, 200)

    root.columnconfigure(0, weight=1, minsize=200)
    root.rowconfigure([0, 2], weight=0, minsize=20)
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
        ('New', lambda: newFile(root, mainWindow)),
        ('Open...', lambda: open_button(root, mainWindow)),
        ('Save', lambda: save(root)),
        ('Save as...', lambda: saveAs(root, mainWindow)),
        ('Build', lambda: build(root)),
        ('Build as...', lambda: buildAs(root)),
        ('Build log', lambda: source_file.SF.build('', 0)),
        ('Help', lambda: documentation(root))
    ]
    if debug_flag:
        panelFrameButtons += [
            ('Canvas redraw', lambda: gp_canvas.canvas.draw(source_file.SF)),
            ('Save log', lambda: source_file.SF.save('', 0)),
            ('Console', lambda: openConsole(root)),
            ('Hard exit', lambda: root.destroy()),
        ]
    root.protocol("WM_DELETE_WINDOW", lambda: closeWindow(root))

    placeButtons(panelFrame, panelFrameButtons)

    mainMenu_tree = {
        "File": {
            "New file": lambda: newFile(root),
            "Open file...": lambda: open_button(root),
            "Save file": lambda: save(root),
            "Save file as...": lambda: lambda: saveAs(root),
        },
        "Build": {
            "Build": lambda: build(root),
            "Build as...": lambda: buildAs(root),
        },
        "Exit": lambda: closeWindow(root),
    }
    if debug_flag:
        mainMenu_tree["Debug"] = {
            "Hard exit": lambda: root.destroy(),
            "Lang": {
                "-> python": lambda: change_lang("python"),
                "-> rscript": lambda: change_lang("rscript"),
                "-> default": lambda: change_lang("default"),
            },

        }
    mainMenu = tk.Menu(master=root)
    createMenu(mainMenu, mainMenu_tree)
    root.config(menu=mainMenu)

    assign_canvas_frame(canvasFrame)
    # Указываем нашему холсту на tk.Canvas, на котором он будет рисовать/ assign canvas to tk.canvas to draw on
    gp_canvas.canvas.master = canvas

    try:
        root.state('zoomed')
    except Exception:
        print('Cannot zoom window (non-Windows OS)')

    # Создание нового файла (инициализация source_file.SF)/Creation of the new file(initialization new source_file.SF)
    source_file.SF = source_file.SourceFile()
    gp_canvas.canvas.draw(source_file.SF)
    mainWindow.title('new file')

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

    canvas.bind("<MouseWheel>", wheel)  # for Windows, MacOS
    canvas.bind("<Button-4>", wheel)  # for Linux # TODO: видимо это не работает, нужно почитать и починить
    canvas.bind("<Button-5>", wheel)  # for Linux

    canvas.bind("<Control-3>", b3_ctrl)
    canvas.bind("<Control-ButtonRelease-3>", b3_ctrl_release)


if __name__ == "__main__":
    print("This module is not for direct call!")
