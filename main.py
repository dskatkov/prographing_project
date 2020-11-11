import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

import gp_source_file as gp_source_file
import gp_ui as gp_ui
import gp_canvas as gp_canvas

if __name__ == "__main__":
    gp_source_file.SF = gp_source_file.SourceFile()
    mainWindow = tk.Tk()
    gp_canvas.canvas = gp_canvas.Canvas()
    gp_ui.ui_init(mainWindow)
    gp_canvas.canvas.master = gp_ui.canvas
    mainWindow.mainloop()

