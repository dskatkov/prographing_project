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

# Профилирование памяти (из консоли)/Profiling from memory
    # pip install memory_profiler 
    # Рисование графика/graph drawing
        # pip install matplotlib
# Профилирование памяти/Memory profiling
# pip install pympler
# Граф ссылок/ link graph
    # pip install objgraph
    # Для рисования графа/drawing graph
        # pip install xdot
        # pip install graphvix

def main():
    # Создаем единственный экземпляр исходника, далее работать будем с ним/ create the only source to work with it
    gp_source_file.SF = gp_source_file.SourceFile()
    # Главное окно/main window
    gp_ui.mainWindow = tk.Tk()
    # Объект, умеющий рисовать наше поле/ object to draw the field
    gp_canvas.canvas = gp_canvas.Canvas()
    # Инициализация UI (создание и расположение фреймов + обработчики мыши)/ UI initialization (creation and placement of frames + handlers)
    gp_ui.ui_init(gp_ui.mainWindow)
    # Указываем нашему холсту на tk.Canvas, на котором он будет рисовать/ assign canvas to tk.canvas to draw on
    gp_canvas.canvas.master = gp_ui.canvas
    # Цикл событий tkinter/ tkinter event loop
    gp_ui.mainWindow.mainloop()



if __name__ == "__main__":
    # Профилирование/Profiling
    if profile:
        # from heartrate import trace, files
        # trace(files=files.all)

        import cProfile, pstats, io
        from pstats import SortKey
        pr = cProfile.Profile()
        pr.enable()

        from pympler import tracker
        memory_tracker = tracker.SummaryTracker()
        
    # Лог дебага/ Debug log
    if debug_flag:
        debug_file = open('logs/########.log', 'wt')
        debug_init(debug_file)


    main()

    # Лог дебага/ Debug log
    if debug_flag:
        debug_close()

    # Профилирование/profiling
    if profile:
        # Граф ссылок (.dot создает, но не находит рендерер (хотя я его ставил))/graph of links
        # import objgraph
        # objgraph.show_refs(
        #     [
        #         gp_source_file.SF, 
        #         gp_ui.mainWindow, 
        #         gp_canvas.canvas,
        #     ], 
        #     filename='logs/refs-graph.png'
        # )

        # Вывод количества новых бъектов/ output of the number of new objects
        memory_tracker.print_diff()

        # Вывод в лог профилирование времени выполнения/ output to profiling log worktime
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.TIME # CALLS CUMULATIVE FILENAME LINE NAME NFL PCALLS STDNAME TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        file = open('logs/time_profiling.log', 'wt')
        file.write(s.getvalue())
        file.close()
