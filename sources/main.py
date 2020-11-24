import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import os

import gp_source_file as source_file
import gp_ui as ui
import gp_canvas as canvas
from settings import *
from utils import *

# Используемые библиотеки: # TODO: вынести в отдельный файл
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
    # Главное окно/main window
    ui.mainWindow = tk.Tk()
    # Инициализация UI (создание и расположение фреймов + обработчики мыши)/ UI initialization (creation and placement of frames + handlers)
    ui.ui_init(ui.mainWindow)
    # Создание нового файла (инициализация source_file.SF)
    ui.newFile()
    # Цикл событий tkinter/ tkinter event loop
    ui.mainWindow.mainloop()

if __name__ == "__main__":
    # Профилирование/Profiling
    if profile:
        # from heartrate import trace, files
        # trace(files=files.all)

        import cProfile, pstats, io
        from pstats import SortKey
        pr = cProfile.Profile()
        pr.enable()

        # from pympler import tracker
        # memory_tracker = tracker.SummaryTracker()
        
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
        #         source_file.SF, 
        #         ui.mainWindow, 
        #         canvas.canvas,
        #     ], 
        #     filename='logs/refs-graph.png'
        # )

        # Вывод количества новых бъектов/ output of the number of new objects
        #memory_tracker.print_diff()

        # Вывод в лог профилирование времени выполнения/ output to profiling log worktime
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE # CALLS CUMULATIVE FILENAME LINE NAME NFL PCALLS STDNAME TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        file = open('logs/time_profiling.log', 'wt')
        file.write(s.getvalue())
        file.close()
