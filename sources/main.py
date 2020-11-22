import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import os

import gp_source_file as gp_source_file
import gp_ui as gp_ui
import gp_canvas as gp_canvas
from settings import *
from utils import *

# Профилирование памяти (из консоли)
    # pip install memory_profiler 
    # Рисование графика
        # pip install matplotlib
# Профилирование памяти
# pip install pympler
# Граф ссылок
    # pip install objgraph
    # Для рисования графа
        # pip install xdot
        # pip install graphvix

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

        from pympler import tracker
        memory_tracker = tracker.SummaryTracker()
        

    if debug_flag:
        debug_file = open('logs/########.log', 'wt')
        debug_init(debug_file)


    main()

    if debug_flag:
        debug_close()

    if profile:
        # Граф ссылок (.dot создает, но не находит рендерер (хотя я его ставил))
        # import objgraph
        # objgraph.show_refs(
        #     [
        #         gp_source_file.SF, 
        #         gp_ui.mainWindow, 
        #         gp_canvas.canvas,
        #     ], 
        #     filename='logs/refs-graph.png'
        # )

        # Вывод количества новых бъектов
        memory_tracker.print_diff()

        # Вывод в лог профилирование времени выполнения
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CALLS # CALLS CUMULATIVE FILENAME LINE NAME NFL PCALLS STDNAME TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        file = open('logs/time_profiling.log', 'wt')
        file.write(s.getvalue())
        file.close()
