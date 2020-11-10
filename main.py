import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

from gp_source_file import *
from gp_ui import *
from gp_canvas import *

mainWindow = tk.Tk()
ui_init(mainWindow)

sourceFile = SourceFile()

mainWindow.mainloop()

