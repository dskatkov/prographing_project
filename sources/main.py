import tkinter as tk

import gp_ui as ui
from settings import *
from utils import *


def main():
    # Главное окно/main window
    ui.mainWindow = tk.Tk()
    # Инициализация UI (создание и расположение фреймов + обработчики мыши)
    # / UI initialization (creation and placement of frames + handlers)
    ui.ui_init(ui.mainWindow)

    # Цикл событий tkinter/ tkinter event loop
    ui.mainWindow.mainloop()


if __name__ == "__main__":
    # Профилирование/Profiling
    if profile:

        import cProfile
        import pstats
        import io
        from pstats import SortKey
        pr = cProfile.Profile()
        pr.enable()

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

        # Вывод в лог профилирование времени выполнения/ output to profiling log worktime
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.FILENAME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        file = open('logs/time_profiling.log', 'wt')
        file.write(s.getvalue())
        file.close()
