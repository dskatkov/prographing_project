import tkinter as tk
import tkinter.font

textEditorMenu_tree = {
    "1": {
        "Сохранить изменения": 0,
        "Открыть...": 0,
        "Сохранить": {
            "A": 0,
            "B": 0,
            "C": 0,
        },
        "Сохранить как...": 0,
    },
    "Сборка": {
        "Собрать исходник": 0,
    },
    "Выход": 0,
}

mainMenu_tree = {
    "Файл": {
        "Новый файл": 0,
        "Открыть...": 0,
        "Сохранить": {
            "A": 0,
            "B": 0,
            "C": 0,
        },
        "Сохранить как...": 0,
    },
    "Сборка": {
        "Собрать исходник": 0,
    },
    "Выход": 0,
}

btnBG = '#202020'
btnFG = '#ffffff'

textBG = '#606060'
textFG = '#ffffff'

panelBG = '#404040'
panelFG = '#ffffff'

spaceBG = '#606060'
spaceFG = '#ffffff'

stateBG = '#404040'
stateFG = '#ffffff'


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

def ui_init(root):
    root.minsize(200, 200)

    root.columnconfigure(0, weight=1, minsize=200)
    root.rowconfigure([0,2], weight=0, minsize=20)
    root.rowconfigure(1, weight=1, minsize=100)

    panelFrame = tk.Frame(master=root, bg=panelBG)
    textFrame = tk.Frame(master=root, bg=textBG)
    stateFrame = tk.Frame(master=root, bg=stateBG)

    panelFrame.grid(row=0, column=0, sticky='nsew')
    textFrame.grid(row=1, column=0, sticky='nsew')
    stateFrame.grid(row=2, column=0, sticky='nsew')

    panelFrameButtons = [
        ('new', ...),
        ('open', ...),
        ('save', ...),
        ('saveas', ...),
        ('build', ...),
    ]
    placeButtons(panelFrame, panelFrameButtons)

    mainMenu = tk.Menu(master=root)
    createMenu(mainMenu, mainMenu_tree)
    root.config(menu=mainMenu)
    # обработчики нажатий мыши
    # обработчики кнопок


