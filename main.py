import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

from gp_source_file import *
from gp_ui import *
from gp_canvas import *



mainWindow = tk.Tk()

#print(tk.filedialog.Open(mainWindow, filetypes = [("Все файлы", "*.*")]).show())

canvas = Canvas(canvasFrame)


ui_init(mainWindow)


mainWindow.mainloop()

