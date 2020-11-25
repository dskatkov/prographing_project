import tkinter as tk

from settings import *

class Point:
    """Класс точки-вектора/ class of a point-vector"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(a, b):
        """a + b"""
        return Point(a.x+b.x, a.y+b.y)

    def __mul__(a, k):
        """a * k"""
        return Point(a.x*k, a.y*k)
    
    def __imul__(self, k):
        self.x *= k
        self.y *= k
        return self

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    # def __ineg__(self):
    #     self.x *= -1
    #     self.y *= -1

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __idiv__(self, k):
        """a * k"""
        if k:
            self.x /= k
            self.y /= k
        else:
            self.x = 0
            self.y = 0
        return self

    def __neg__(a):
        """-a"""
        return a * (-1)

    def __sub__(a, b):
        """a - b"""
        return a + (-b)

    def __truediv__(a, k):
        """a * k"""
        if k:
            return Point(a.x/k, a.y/k)
        else:
            return Point(0, 0)

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
        """Длина вектора/vector length"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def fromTuple(self, tup):
        """Создает Point из кортежа/ create point out of tuple"""
        return Point(*tup)

    def set(self, x, y):
        self.x = x
        self.y = y
        return self

    def tuple(self):
        """Создает кортеж из Point/ create tuple out of point"""
        return self.x, self.y

    def round(self, s=1):
        """Округляет координаты до требуемой точности/ round to the necessary accuracy"""
        return Point(round(self.x/s)*s, round(self.y/s)*s)

    def swap(self):
        return Point(self.y, self.x)

    def norm(self, k=1):
        return self / (self.abs()/k)

    def dist(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)**0.5

    def setInPlace(self, x, y):
        self.x = x
        self.y = y
        return self

    def sumInPlace(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def mulInPlace(self, k):
        self.x *= k
        self.y *= k
        return self

    def negInPlace(self, other):
        self.x *= -1
        self.y *= -1
        return self

    def subInPlace(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def divInPlace(self, k):
        """a * k"""
        if k:
            self.x /= k
            self.y /= k
        else:
            self.x = 0
            self.y = 0
        return self

    def roundInPlace(self, s=1):
        """Округляет координаты до требуемой точности/ round to the necessary accuracy"""
        self.x = round(self.x/s)*s,
        self.y = round(self.y/s)*s
        return self

    def swapInPlace(self):
        self.x, self.y = self.y, self.x
        return self


    def normInPlace(self):
        self.divInPlace(self.abs())
        return self

    def copy(self):
        return Point(self.x, self.y)




debug_log = ...
def debug_init(file):
    """Установка файла для дебагового лога/ set file for debug log"""
    global debug_log
    debug_log = file

def debug_close():
    """Закрытие файла лога/ Closing log file"""
    global debug_log
    debug_log.close()

def debug_return(s):
    """Вывод в дебаговый лог/ output to debug log"""
    if debug_to_console:
        print(s)
    if debug_flag:
        debug_log.write(str(s) + '\n')

def createMenu(master, tree):
    """Создает меню и прикрепляет его к master/ create menu and assign it to master"""
    for key, val in tree.items():
        m = tk.Menu(master=master, tearoff=0)
        if type(val)==type({}):
            createMenu(m, val)
        else:
            master.add_command(label=key, command=val)
            continue
        master.add_cascade(label=key, menu=m)

def placeButtons(master, buttons, side='left', fg=btnFG, bg=btnBG):
    """Располагает кнопки на фрейме/ place buttons on frame"""
    for btn in buttons:
        b = tk.Button(master=master, text=btn[0], command=btn[1], fg=btnFG, bg=btnBG)
        b.pack(side=side, padx=3, pady=3)

def getSettingsByLang(lang):
    """Устанавливает настройки в связи с языком программирования/Set setting associated with programming language"""
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

def normalMerge(a, b, f=None):
    """Функция слияния двух элементов/ Function of merging two elements"""
    if type(a) != dict or type(b) != dict:
        if a == b:
            return a
        elif f is not None:
            return f(a, b)
        else:
            raise Exception(f'Merge conflict: {a} and {b}')
            return a
    else:
        return dictMerge(a, b)

def dictMerge(*dicts, f=None):
    """Соединяет несколько словарей в один/ merge s number of dictionaries into one"""
    if len(dicts) == 2:
        a, b = dicts
        res = a
        for key, val in b.items():
            if key in a:
                val2 = a[key]
                if val == val2:
                    res[key] = val
                else:
                    if isinstance(val, dict) and isinstance(val2, dict):
                        res[key] = dictMerge(val, val2)
                    elif f is not None:
                        res[key] = f(val2, val)
                    else:
                        raise Exception(f'Merge conflict: {a} and {b}')
            else:
                res[key] = val
        return res
    elif len(dicts) > 2:
        return dictMerge(dictMerge(dicts[0:2]), dicts[2:])
    elif len(dicts) == 0:
        return {}
    elif len(dicts) == 1:
        return dicts[0]


def getDictValByPath(d, path, err=0):
    """Возвращает значение элемента в словаре по пути к элементу/ return element value in dictionary by path to the element"""
    val = d
    spl = path.split('.')
    for key in spl:
        if key in val:
            val = val[key]
        else:
            return err
    return val

def createDictByPath(path, val):
    """Создает вложенный словарь с одним элементом по пути/ create inserted dictionary with one element by path"""
    raise Exception('Warning')
    spl = path.split('.')
    spl.reverse()

    d = {spl[0]: val}

    for key in spl[1:]:
        d = {key: d}
    return d

def setDictValByPath(d, path, val):
    """Устанавливает значение во вложенном словаре по пути/ Set value in inserted dictionary by path"""
    return dictMerge(d, createDictByPath(path, val), f=takeSecond)

# Страшная вещь)/ Scary thing)
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
    if res == ...:
        raise Exception(f'Cannot get dict value by path: \ndict:{d} \npath:{form} \nargs: {args}')
    return res

def distance_to_line(begin, end, point):
    """Расстояние от отрезка (begin, end) до точки point/ distance from the segment (begin, end) to the point"""
    assert isinstance(begin, Point)
    assert isinstance(end, Point)
    assert isinstance(point, Point)
    
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
    """Проверяет близость точки прямой/ Check whether point is near to the line"""
    assert isinstance(begin, Point)
    assert isinstance(end, Point)
    assert isinstance(point, Point)

    eps = nearToLine
    d = distance_to_line(begin, end, point)
    x1, y1 = begin.tuple()
    x2, y2 = end.tuple()
    x, y = point.tuple()

    return (d < eps) and (min(x1, x2) - eps < x < max(x1, x2) + eps) and (min(y1, y2) - eps < y < max(y1, y2) + eps)

def findCycle(SF, block, root):
    """Проверяет существование цикла ссылок/ checking existance of cycle links"""
    for id in block.childs:
        child = SF.object_ids[id]
        if child is root:
            return True
        elif findCycle(SF, child, root):
            return True
    return False


def cycle_checkout(SF, block):
    """Проверяет существование цикла ссылок/ checking existance of cycle links"""
    return findCycle(SF, block, block)

def find_block_(click, canvas, SF, mode=1):
    """Находит блок по позиции клика/ Find block by its position"""
    scale = lambda pos: canvas.scale(pos)
    unscale = lambda pos: canvas.unscale(pos)
    clickpos = Point(click.x, click.y)
    sfclick = unscale(clickpos)
    debug_return(f'handling click: {clickpos}')
    if mode == 0: # находжение по радиусу блока
        for _, block in SF.object_ids.items():
            #debug_return('checking block: ' + block.convertToStr())
            distance = (block.pos - sfclick).abs()
            if distance <= blockR:
                debug_return(f'block found: {block.convertToStr()}')
                return block
    elif mode == 1: # нахождение по клетке клика
        for _, block in SF.object_ids.items():
            #debug_return('checking block: ' + block.convertToStr())
            d = block.pos - sfclick
            if abs(d.x) < 0.5 and abs(d.y) < 0.5:
                debug_return(f'block found: {block.convertToStr()}')
                return block


# Число Эйлера/ Eiler's number
e = 2.718281828459045
pi = 3.1415926535

if __name__ == '__main__':
    print('This module is not for direct call!')
