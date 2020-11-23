import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

from settings import *
from utils import *
import gp_canvas as gp_canvas

def getText(textArea):
    """Возвращает содержимое поля"""
    if isinstance(textArea, tk.Entry):
        return textArea.get()
    elif isinstance(textArea, tk.Text):
        return textArea.get('1.0', 'end')[:-1]
    else:
        debug_return ('Unknown type of textarea')
        return ''


class TextEditor:
    """
    Класс редактора блока
    block - редактируемый блок
    canvas - холст, отрисовка которого произойдет при закрытии редактора
    root - окно редактора
    panelFrame - фрейм панели кнопок
    editFrame - фрейм всех полей для редактирования
    stateFrame - фрейм нижней строки
    textAreas - словарь {<название поля>:<tk объект для редактирования>}

    """
    def __init__(self, root, block, canvas):
        self.block = block
        self.root = root
        self.canvas = canvas

        #configuring main window
        #root.minsize(400, 200)

        root.columnconfigure(0, weight=1, minsize=0)
        root.rowconfigure(0, weight=0, minsize=20)
        root.rowconfigure(1, weight=1, minsize=0)
        root.rowconfigure(2, weight=0, minsize=20)

        #creating menu
        # mainMenu = tk.Menu(master=root)
        # createMenu(mainMenu, textEditorMenu_tree)
        # root.config(menu=mainMenu)

        #creating and placing frames
        self.panelFrame = tk.Frame(master=root, bg=panelBG)
        self.editFrame = tk.Frame(master=root)
        self.stateFrame = tk.Frame(master=root, bg=stateBG)

        #self.panelFrame.grid(row=0, column=0, sticky='nsew')
        self.editFrame.grid(row=1, column=0, sticky='nsew')
        self.stateFrame.grid(row=2, column=0, sticky='nsew')

        # Словарь со всеми полями для редактирования
        self.textAreas = {}


        focused = 0 # TODO: параметр для автофокуса
        debug_return('block fields: ' + str(getDictValByPathDef(allTypes, f'<1>.edit.<2>', block.classname, block.SF.lang)))
        for key, val in getDictValByPathDef(allTypes, f'[1].edit.[2]', block.classname, block.SF.lang, braces='[]').items():
            editing_type = getDictValByPathDef(allTypes, f'[1].edit.[2].{key}.type', block.classname, block.SF.lang, braces='[]')
            header = getDictValByPathDef(allTypes, f'[1].edit.[2].{key}.header', block.classname, block.SF.lang, braces='[]')

            if editing_type == 'invisible':
                pass
            elif editing_type == 'singleline':
                if header:
                    lbl = tk.Label(master=self.editFrame, bg=textBG, fg=textFG, text=header)
                    lbl.pack(fill='x', expand=0)

                ta = tk.Entry(master=self.editFrame, bg=textBG, fg=textFG)
                if key in block.data:
                    ta.insert(0, block.data[key])
                else:
                    debug_return (f'Wrong format of block: {block.convertToStr()}')
                ta.pack(fill='x', expand=0, side="top")

                self.textAreas[key] = ta

                if not focused:
                    ta.focus()
                    focused = 1
                    #ta.bind("Return", lambda: self.close(-1))
            elif editing_type == 'multiline':
                if header:
                    lbl = tk.Label(master=self.editFrame, bg=textBG, fg=textFG, text=header)
                    lbl.pack(fill='x', expand=0)

                ln = len(block.data[key].split('\n'))
                ta = tk.Text(master=self.editFrame, height=ln+2, bg=textBG, fg=textFG, wrap='word')
                ta.insert('1.0', block.data[key])
                ta.pack(fill='both', expand=1, side="top")

                self.textAreas[key] = ta
            else:
                debug_return ('Unknown type of editing field')


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

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close(-1))
        self.root.title(block.getSub())

# def dialogOpenFile(root, textArea):

#     textArea.delete('1.0', 'end')
#     textArea.insert('1.0', open(fileName, 'rt').read())
#     root.title(fileName)


# def dialogSaveFile(root, textArea):
#     open(fileName, 'wt').write(textArea.get('1.0', 'end'))

    def close(self, state=-1):
        """Закрывает редактор"""
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

            for key, val in getDictValByPathDef(allTypes, f'<1>.edit.<2>', self.block.classname, self.block.SF.lang).items():
                debug_return(f'saving key: {key}')
                if key == '<class>':
                    cn = getText(self.textAreas[key])
                    debug_return (f'changing type: {cn}')
                    if cn in allTypes:
                        self.block.changeType(cn)
                    else:
                        debug_return ('Unknown type of block')
                    break
                if key in self.textAreas:
                    self.block.data[key] = getText(self.textAreas[key])
            self.root.destroy()
            self.block.text_editor = None

        self.canvas.draw(self.block.SF)

if __name__ == "__main__":
    print("This module is not for direct call!")
