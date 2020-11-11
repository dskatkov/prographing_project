import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

from gp_source_file import *
from gp_ui import *
from gp_canvas import *

if __name__ == "__main__":
	global SF
	SF = SourceFile()
	mainWindow = tk.Tk()
	ui_init(mainWindow, SF, canvas)
	canvas = Canvas(canvasFrame)
	mainWindow.mainloop()

