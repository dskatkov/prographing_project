import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
from os import getcwd

import gp_source_file as gp_source_file
import gp_ui as gp_ui
import gp_canvas as gp_canvas
from settings import *
from utils import *

def main():
    gp_source_file.SF = gp_source_file.SourceFile()
    gp_ui.mainWindow = tk.Tk()
    gp_canvas.canvas = gp_canvas.Canvas()
    gp_ui.ui_init(gp_ui.mainWindow)
    gp_canvas.canvas.master = gp_ui.canvas
    gp_ui.mainWindow.mainloop()


if __name__ == "__main__":

    if profile:
        import cProfile, pstats, io
        from pstats import SortKey
        pr = cProfile.Profile()
        pr.enable()

    if debug_flag:
        debug_file = open('########.log', 'wt')
        debug_init(debug_file)


    main()

    if debug_flag:
        debug_close()

    if profile:
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()

        file = open('Profiling.log', 'wt')
        file.write(s.getvalue())
        file.close()
