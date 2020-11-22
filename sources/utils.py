import tkinter as tk
from settings import *

class Point:
    """Класс точки-вектора"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(a, b):
        """a + b"""
        return Point(a.x+b.x, a.y+b.y)

    def __mul__(a, k):
        """a * k"""
        return Point(a.x*k, a.y*k)

    def __neg__(a):
        """-a"""
        return a*(-1)

    def __sub__(a, b):
        """a - b"""
        return a + (-b)

    def __str__(self):
        """str(self)"""
        return f'({self.x},{self.y})'

    def __eq__(a, b):
        """a == b"""
        return a.x == b.x and a.y == b.y

    def __lt__(a, b):
        """a < b"""
        if a.y < b.y:
            return True
        elif a.y == b.y and a.x < b.x:
            return True
        else:
            return False

    def abs(self):
        """Длина вектора"""
        return (self.x ** 2 + self.y ** 2) ** (1/2)

    def fromTuple(self, tup):
        """Создает Point из кортежа"""
        return Point(tup[0], tup[1])

    def tuple(self):
        """Создает кортеж из Point"""
        return self.x, self.y

    def round(self, s=1):
        """Округляет координаты до требуемой точности"""
        return Point(round(self.x/s)*s, round(self.y/s)*s)

debug_log = ...
def debug_init(file):
    """Установка файла для дебагового лога"""
    global debug_log
    debug_log = file

def debug_close():
    """Закрытие файла лога"""
    global debug_log
    debug_log.close()

def debug_return(s):
    """Вывод в дебаговый лог"""
    if debug_flag:
        debug_log.write(str(s) + '\n')

def createMenu(master, tree):
    """Создает меню и прикрепляет его к master"""
    for key, val in tree.items():
        m = tk.Menu(master=master, tearoff=0)
        if type(val)==type({}):
            createMenu(m, val)
        else:
            master.add_command(label=key, command=val)
            continue
        master.add_cascade(label=key, menu=m)

def placeButtons(master, buttons, side='left', fg=btnFG, bg=btnBG):
    """Располагает кнопки на фрейме"""
    for btn in buttons:
        b = tk.Button(master=master, text=btn[0], command=btn[1], fg=btnFG, bg=btnBG)
        b.pack(side=side, padx=3, pady=3)

def getSettingsByLang(lang):
    res = {}
    for type in t_all:
        res = dictMerge(
            res, 
            createDictByPath(
                f'{type}.build',
                dictMerge(
                    getDictValByPath(allTypes, f'{type}.build.{lang}')
                    , getDictValByPath(allTypes, f'{type}.build.*')
                )
            )
        )
        for key, val in allTypes[type].items():
            if not (key in ['build']):
                res = dictMerge(res, {type:{key:val}})
    return res

takeFirst = lambda x, y: x
takeSecond = lambda x, y: y

def normalMerge(a, b, f=takeFirst):
    """Функция слияния двух элементов"""
    if type(a) != dict or type(b) != dict:
        return f(a, b)
    return dictMerge(a, b)

def dictMerge(*dicts, f=lambda x,y: normalMerge(x,y,f=takeFirst)):
    """Соединяет несколько словарей в один"""
    res = {}

    if len(dicts) == 2:
        a, b = dicts

        for key, val in a.items():
            if not key in b:
                res[key] = val

        for key, val in b.items():
            if not key in a:
                res[key] = val

        for key, val in a.items():
            if key in b:
                res[key] = f(val, b[key])
    else:
        for d in dicts:
            res = dictMerge(res, d, f=f)

    return res

def getDictValByPath(d, path):
    """Возвращает значение элемента в словаре по пути к элементу"""
    val = d
    spl = path.split('.')
    for key in spl:
        if key in val:
            val = val[key]
        else:
            val = {}
            break
    return val

def createDictByPath(path, val):
    """Создает вложенный словарь с одним элементом по пути"""
    spl = path.split('.')
    spl.reverse()

    d = {spl[0]: val}

    for key in spl[1:]:
        d = {key: d}
    return d

def setDictValByPath(d, path, val):
    """Устанавливает значение во вложенном словаре по пути"""
    return dictMerge(d, createDictByPath(path, val), f=takeSecond)

# Словарь всех типов блоков
allTypes = dictMerge(t_default, t_op, t_if, t_for, t_class, t_function)



# def dictMergeSmall(a, b):
#     res = {}
#     for key, val in list(a.items())+list(b.items()):
#         res[key] = val
#     return res
# print(dictMergeSmall({1:2,3:4},{5:6,1:7}))

# Число Эйлера
e = 2.718281828459045

if __name__ == '__main__':
    p1 = Point(1, 2)
    p2 = Point(-5, -7)
    print(p1<p2)
    print(p1*10)
    print('This module is not for direct call!')
