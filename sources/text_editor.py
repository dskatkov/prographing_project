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
        self.editFrame = tk.Frame(master=root)
        self.stateFrame = tk.Frame(master=root, bg=stateBG)

        self.panelFrame.grid(row=0, column=0, sticky='nsew')
        self.editFrame.grid(row=1, column=0, sticky='nsew')
        self.stateFrame.grid(row=2, column=0, sticky='nsew')

            # #placing textbox to editFrame
            # self.textBox1 = tk.Text(master=self.editFrame, bg=textBG, fg=textFG, wrap='word', undo=True, maxundo=0)
            # self.textBox1.pack(fill='both', expand=1)

        self.textAreas = {}

        d = allTypes[block.classname]['edit']
        for key, val in d.items():
            lbl = tk.Label(master=self.editFrame, bg=textBG, fg=textFG, text=val['header'])
            lbl.pack(fill='x', expand=0)
            if val['type'] == 'singleline':
                ta = tk.Entry(master=self.editFrame, bg=textBG, fg=textFG)
                ta.insert(0, block.data[key])
                ta.pack(fill='x', expand=0)
            elif val['type'] == 'multiline':
                ta = tk.Text(master=self.editFrame, bg=textBG, fg=textFG, wrap='word')
                ta.insert('1.0', block.data[key])
                ta.pack(fill='x', expand=1)
            else:
                raise '123'

            self.textAreas[key] = ta


        #placing buttons to panelFrame
        # panelFrameButtons = [
        #     ('open', lambda: print('open, not implemented')),
        #     ('save', lambda: print('save, not implemented')),
        # ]
        # placeButtons(self.panelFrame, panelFrameButtons)

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
        pass
        # self.textBox1.delete('1.0', 'end')
        # self.textBox1.insert('1.0', block.text1)
        # self.root.title(f'type: {block.classname} pos: {block.pos} childs: {block.childs} text1: {block.text1}')

    def close(self, state=-1):
        # state == -1 - спросить о закрытии и о сохранении
        # state == 0 - закрыть без сохранения
        # state == 1 - закрыть с сохранением
        if state == -1:
            if tk.messagebox.askyesno("close?", "Close window?", parent=self.root):
                if tk.messagebox.askyesno("save?", "Save changes?", parent=self.root):
                    state = 1
                else:
                    state = 0
            else:
                state = -1

        if state == 0:
            # не сохранить и закрыть
            self.root.destroy()
            self.block.text_editor = None

        if state == 1:
            # сохраниить и закрыть
            # self.block.text1 = self.textBox1.get('1.0', 'end')[:-1]
            # print('opening: '+str(self.block.data))
            d = allTypes[self.block.classname]['edit']
            for key, val in d.items():
                if isinstance(self.textAreas[key], tk.Entry):
                    self.block.data[key] = self.textAreas[key].get()
                elif isinstance(self.textAreas[key], tk.Text):
                    self.block.data[key] = self.textAreas[key].get('1.0', 'end')[:-1]
            self.root.destroy()
            self.block.text_editor = None

# def mainWindow(root):
#     #configuring main window
#     root.minsize(600, 400)
#     root.title('initial title')

#     root.columnconfigure(0, weight=1, minsize=200)
#     root.rowconfigure([0, 2], weight=0, minsize=30)
#     root.rowconfigure(1, weight=1, minsize=100)

#     #creating menu
#     mainMenu = tk.Menu(master=root)
#     createMenu(mainMenu, mainMenu_tree)
#     root.config(menu=mainMenu)

#     #creating and placing frames
#     panelFrame = tk.Frame(master=root, bg=panelBG)
#     spaceFrame = tk.Frame(master=root, bg=spaceBG)
#     stateFrame = tk.Frame(master=root, bg=stateBG)

#     panelFrame.grid(row=0, column=0, sticky='nsew')
#     spaceFrame.grid(row=1, column=0, sticky='nsew')
#     stateFrame.grid(row=2, column=0, sticky='nsew')

#     #placing buttons to panelFrame
#     panelFrameButtons = [
#         ('text', None),
#         ('save', None),
#         ('open', None),
#         ('build', None),
#     ]
#     placeButtons(panelFrame, panelFrameButtons, side='left')

#     #placing labels to stateFrame
#     stateLeftLabel = tk.Label(master=stateFrame, text="left label", bg=stateBG, fg=stateFG)
#     stateRightLabel = tk.Label(master=stateFrame, text="right label", bg=stateBG, fg=stateFG)
#     stateCenterLabel = tk.Label(master=stateFrame, text="right label", bg=stateFG, fg=stateFG)

#     stateLeftLabel.pack(side='left', fill='y')
#     stateRightLabel.pack(side='right', fill='y')
#     stateCenterLabel.pack(side='top', fill='both')
