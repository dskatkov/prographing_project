import tkinter as tk
from settings import *
from gp_block_types import *

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
        if a.y > b.y:
            return False
        return a.x < b.x

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
    if debug_to_console:
        print(s)
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
    raise Exception
    res = {}
    for type in allTypes:
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

def getDictValByPath(d, path, err=0):
    """Возвращает значение элемента в словаре по пути к элементу"""
    val = d
    spl = path.split('.')
    for key in spl:
        if key in val:
            val = val[key]
        else:
            return err
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

# Страшная вещь)
def getDictValByPathDef(d, form, *args, braces='<>', default='*'):
    lb, rb = braces[0], braces[1]
    n = 0
    res = ...
    while (res == ...) and n < 2 ** len(args):
        s = form
        for i in range(len(args)-1, -1, -1):
            if not (n & (1 << (len(args) - i - 1))):
                s = s.replace(f'{lb}{i+1}{rb}', args[i])
            else:
                s = s.replace(f'{lb}{i+1}{rb}', default)
        v = getDictValByPath(d, s, err=...)
        if v != ...:
            res = v
        n += 1
    return res

def distance_to_line(begin, end, point):
    """Расстояние от прямой (begin, end) до точки point"""
    x1, y1 = begin.tuple()
    x2, y2 = end.tuple()
    x, y = point.tuple()
    if begin == end:
        dist = (begin - end).abs()
    else:
        #A, B, C are factors of Ax+By+C=0 equation
        a = (x2 - x1) # 1/A
        b = (y1 - y2) # 1/B
        c = -x1*b -y1*a # C/AB
        dist = (b*x + a*y + c) / (a**2 + b**2)**0.5
        dist = abs(dist)
    return dist

def near_to_line(begin, end, point):
    """Проверяет близость точки прямой"""
    eps = nearToLine
    d = distance_to_line(begin, end, point)
    x1, y1 = begin.tuple()
    x2, y2 = end.tuple()
    x, y = point.tuple()

    if d < eps:
        if (min(x1, x2) - eps < x < max(x1, x2) + eps) and (min(y1, y2) - eps < y < max(y1, y2) + eps):
            return True
    return False

def findCycle(SF, block, root):
    """Проверяет существование цикла ссылок"""
    for id in block.childs:
        child = SF.object_ids[id]
        if child is root:
            return True
        elif findCycle(SF, child, root):
            return True
    return False


def cycle_checkout(SF, block):
    """Проверяет существование цикла ссылок"""
    return findCycle(SF, block, block)

def find_block_(click, canvas, SF):
    """Находит блок по позиции клика"""
    scale = lambda pos: canvas.scale(pos)
    unscale = lambda pos: canvas.unscale(pos)

    debug_return(f'handling click: ({click.x},{click.y})')
    sfclick = unscale(Point(click.x, click.y))
    for _, block in SF.object_ids.items():
        #debug_return('checking block: ' + block.convertToStr())
        distance = (block.pos - sfclick).abs()
        if distance <= blockR:
            debug_return(f'block found: {block.convertToStr()}')
            return block


# Число Эйлера
e = 2.718281828459045

if __name__ == '__main__':
    print('This module is not for direct call!')
