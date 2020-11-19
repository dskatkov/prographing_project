import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

from settings import *
from utils import *

class TextEditor:
    def __init__(self, root, block):
        self.block = block
        self.root = root
        #configuring main window
        root.minsize(200, 200)

        root.columnconfigure(0, weight=1, minsize=200)
        root.rowconfigure([0,2], weight=0, minsize=20)
        root.rowconfigure(1, weight=1, minsize=100)

        #creating menu
        # mainMenu = tk.Menu(master=root)
        # createMenu(mainMenu, textEditorMenu_tree)
        # root.config(menu=mainMenu)

        #creating and placing frames
        self.panelFrame = tk.Frame(master=root, bg=panelBG)
        self.textFrame = tk.Frame(master=root)
        self.stateFrame = tk.Frame(master=root, bg=stateBG)

        self.panelFrame.grid(row=0, column=0, sticky='nsew')
        self.textFrame.grid(row=1, column=0, sticky='nsew')
        self.stateFrame.grid(row=2, column=0, sticky='nsew')

        #placing textbox to textFrame
        self.textBox1 = tk.Text(master=self.textFrame, bg=textBG, fg=textFG, wrap='word', undo=True, maxundo=0)
        self.textBox1.pack(fill='both', expand=1)

        #placing buttons to panelFrame
        panelFrameButtons = [
            ('open', lambda: print('open, not implemented')),
            ('save', lambda: print('save, not implemented')),
        ]
        placeButtons(self.panelFrame, panelFrameButtons)

        #placing buttons to panelFrame
        stateFrameButtons = [
            ('✔ OK', lambda: self.close(1)),
            ('❌ Отмена', lambda: self.close(0)),
        ]
        placeButtons(self.stateFrame, stateFrameButtons, side='right')

        self.open(self.block)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

# def dialogOpenFile(root, textArea):

#     textArea.delete('1.0', 'end')
#     textArea.insert('1.0', open(fileName, 'rt').read())
#     root.title(fileName)


# def dialogSaveFile(root, textArea):
#     open(fileName, 'wt').write(textArea.get('1.0', 'end'))

    def open(self, block):
        self.textBox1.delete('1.0', 'end')
        self.textBox1.insert('1.0', block.text1)
        self.root.title(f'type: {block.classname} pos: {block.pos} childs: {block.childs} text1: {block.text1}')

    def close(self, state=-1):
        if state == -1:
            if tk.messagebox.askyesno("close?", "Close window?", parent=self.root):
                if tk.messagebox.askyesno("save?", "Save changes?", parent=self.root):
                    state = 1
                else:
                    state = 0
            else:
                state = -1

        if state == 0:
            # не сохранять
            self.root.destroy()
            self.block.text_editor = None

        if state == 1:
            # сохраниить
            self.block.text1 = self.textBox1.get('1.0', 'end')[:-1]
            print(self.block.text1)
            self.root.destroy()
            self.block.text_editor = None

def mainWindow(root):
    #configuring main window
    root.minsize(600, 400)
    root.title('initial title')

    root.columnconfigure(0, weight=1, minsize=200)
    root.rowconfigure([0, 2], weight=0, minsize=30)
    root.rowconfigure(1, weight=1, minsize=100)

    #creating menu
    mainMenu = tk.Menu(master=root)
    createMenu(mainMenu, mainMenu_tree)
    root.config(menu=mainMenu)

    #creating and placing frames
    panelFrame = tk.Frame(master=root, bg=panelBG)
    spaceFrame = tk.Frame(master=root, bg=spaceBG)
    stateFrame = tk.Frame(master=root, bg=stateBG)

    panelFrame.grid(row=0, column=0, sticky='nsew')
    spaceFrame.grid(row=1, column=0, sticky='nsew')
    stateFrame.grid(row=2, column=0, sticky='nsew')

    #placing buttons to panelFrame
    panelFrameButtons = [
        ('text', None),
        ('save', None),
        ('open', None),
        ('build', None),
    ]
    placeButtons(panelFrame, panelFrameButtons, side='left')

    #placing labels to stateFrame
    stateLeftLabel = tk.Label(master=stateFrame, text="left label", bg=stateBG, fg=stateFG)
    stateRightLabel = tk.Label(master=stateFrame, text="right label", bg=stateBG, fg=stateFG)
    stateCenterLabel = tk.Label(master=stateFrame, text="right label", bg=stateFG, fg=stateFG)

    stateLeftLabel.pack(side='left', fill='y')
    stateRightLabel.pack(side='right', fill='y')
    stateCenterLabel.pack(side='top', fill='both')
