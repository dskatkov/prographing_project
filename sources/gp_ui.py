import tkinter as tk
#import tkinter.font
import time

import gp_source_file as source_file
import gp_canvas as gp_canvas
from gp_mouse_binding import *
from settings import *
from utils import *
from gp_block_manager import *

# canvas - tk.Canvas
canvasFrame = panelFrame = stateFrame = canvas = mainWindow = ...


def saveAs(root):
    """Обработчик кнопки save as handler of save as button"""
    fileName = tk.filedialog.SaveAs(
        root, filetypes=[("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        if not fileName.endswith('.vrc'):
            fileName += '.vrc'
        source_file.SF.save(fileName)
        mainWindow.title(fileName)


def save(root):
    """Обработчик кнопки save/ handler of save button"""
    if source_file.SF.fileName == '':
        saveAs(root)
    else:
        source_file.SF.save(source_file.SF.fileName)


def open(root):
    """Обработчик кнопки open/ handler of open button"""
    fileName = tk.filedialog.Open(
        root, filetypes=[("Visual script", ".vrc")]).show()
    if fileName == '':
        return
    else:
        if not fileName.endswith('.vrc'):
            fileName += '.vrc'
        source_file.SF.open(fileName)
        gp_canvas.canvas.draw(source_file.SF)
        mainWindow.title(fileName)


def build(root):
    """Обработчик кнопки build/ handler of build button"""
    if source_file.SF.buildName == '':
        buildAs(root)
    else:
        source_file.SF.build(source_file.SF.buildName)


def buildAs(root):
    """Обработчик кнопки build as/ handler of build as button"""
    ext = '.b.'+source_file.SF.lang
    fileName = tk.filedialog.SaveAs(
        root, filetypes=[("Source code", ext)]).show()
    if fileName == '':
        return
    else:
        debug_return('Building to '+fileName)
        if not fileName.endswith(ext):
            fileName += ext
        source_file.SF.build(fileName)

def close(root):
    if source_file.SF.closeQ():
        del source_file.SF
        return 1
    else:
        ans = tk.messagebox.askyesnocancel("save?", "Save file?", parent=root)
        if ans == None:
            return 0
        if ans == 1:
            source_file.SF.save()
            del source_file.SF
            return 1
        if ans == 0:
            del source_file.SF
            return 1

def newFile(root):
    """Обработчик кнопки new file/ handler of new file button"""
    if close(root):
        source_file.SF = source_file.SourceFile()
        gp_canvas.canvas.draw(source_file.SF)
        mainWindow.title('new file')


def closeWindow(root):
    if close(root):
        root.destroy()

consoleWindow = None


def openConsole(root):
    def close(window, entry):
        if entry.get():
            eval(str(entry.get()))
        window.destroy()
    global consoleWindow
    if not consoleWindow:
        consoleWindow = tk.Toplevel(root)
        entry = tk.Entry(master=consoleWindow)
        entry.pack()
        entry.focus()
        consoleWindow.title('console')
        consoleWindow.protocol(
            "WM_DELETE_WINDOW", lambda: close(consoleWindow, entry))


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
        ('new', lambda: newFile(root)),
        ('open', lambda: open(root)),
        ('save', lambda: save(root)),
        ('save as', lambda: saveAs(root)),
        ('build', lambda: build(root)),
        ('build as', lambda: buildAs(root)),
    ]
    if debug_flag:
        panelFrameButtons += [
            ('canvas redraw', lambda: gp_canvas.canvas.draw(source_file.SF)),
            ('build log', lambda: source_file.SF.build('', 0)),
            ('save log', lambda: source_file.SF.save('', 0)),
            ('console', lambda: openConsole(root)),
            ('exit', lambda: root.destroy()),
        ]
    root.protocol("WM_DELETE_WINDOW", lambda: closeWindow(root))

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
            "py": lambda: change_lang("python"),
            "rs": lambda: change_lang("rscript"),
            "default": lambda: change_lang("default"),
        },
    }
    mainMenu = tk.Menu(master=root)
    createMenu(mainMenu, mainMenu_tree)
    root.config(menu=mainMenu)

    assign_canvasFrame(canvasFrame)
    # Указываем нашему холсту на tk.Canvas, на котором он будет рисовать/ assign canvas to tk.canvas to draw on
    gp_canvas.canvas.master = canvas

    try:
        root.state('zoomed')
    except Exception:
        print('Cannot zoom window')

    # Создание нового файла (инициализация source_file.SF)
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

    canvas.bind("<MouseWheel>", wheel) # for Windows, MacOS
    canvas.bind("<Button-4>", wheel) # for Linux
    canvas.bind("<Button-5>", wheel) # for Linux

    canvas.bind("<Control-3>", b3_ctrl)
    canvas.bind("<Control-ButtonRelease-3>", b3_ctrl_release)


if __name__ == "__main__":
    print("This module is not for direct call!")
