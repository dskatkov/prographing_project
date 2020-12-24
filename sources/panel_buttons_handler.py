import tkinter as tk

from settings import *
from utils import *
import gp_source_file as source_file
import gp_canvas as gp_canvas
import coloring_module

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
        consoleWindow.title('Console')
        consoleWindow.protocol(
            "WM_DELETE_WINDOW", lambda: close(consoleWindow, entry))

def saveAs(root, mainWindow):
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


def open_button(root, mainWindow):
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
    ext = '*.*'  # '.b.'+source_file.SF.lang
    fileName = tk.filedialog.SaveAs(
        root, filetypes=[("Source code", ext)]).show()
    if fileName == '':
        return
    else:
        debug_return('Building to ' + fileName)
        # if not fileName.endswith(ext):
        #     fileName += ext
        source_file.SF.build(fileName)

def close(root):
    if source_file.SF.closeQ():
        del source_file.SF
        return 1
    else:
        ans = tk.messagebox.askyesnocancel("Save?", "Save changes?", parent=root)
        if ans is None:
            return 0
        if ans == 1:
            source_file.SF.save()
            del source_file.SF
            return 1
        if ans == 0:
            del source_file.SF
            return 1

def documentation(root):
    root = tk.Tk()
    root.title('Documentation')
    Scrollbar = tk.Scrollbar(root)
    doc_window = tk.Text(root, height=40, width=100, bg = textBG, fg = textFG)
    Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    doc_window.pack(side=tk.LEFT, fill=tk.Y)
    Scrollbar.config(command=doc_window.yview)
    doc_window.config(yscrollcommand=Scrollbar.set)
    doc_window.pack()

    file = open ("user_documentation.txt", "r")
    doc_text =  file.read()

    doc_window.insert(tk.END, doc_text)

def closeWindow(root):
    if close(root):
        root.destroy()

def newFile(root, mainWindow):
    """Обработчик кнопки new file/ handler of new file button"""
    if close(root):
        source_file.SF = source_file.SourceFile()
        gp_canvas.canvas.draw(source_file.SF)
        mainWindow.title('new file')





if __name__ == "__main__":
    print("This module is not for direct call!")
