import tkinter as tk
import tkinter.ttk
from os import getcwd
from ast import literal_eval

import text_editor
from settings import *
from utils import *

SF = ...

class SourceFile:
    """
    Класс графической программы
        max_id = 0 - максимальный id блоков
        object_ids = {} - словарь ссылок на блоки
        fileName = '' - файл для сохранение
        buildName = '' - файл для составления текста программы
        data = '---' - некоторые данные (пока не используется)
        lang = 'py' - язык составления программы
    """
    def __init__(self):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = ''
        self.buildName = ''
        self.data = '---'
        self.lang = 'py'


    def save(self, fileName, save=1):
        """Сохраняет в файл"""
        s = ''
        s += self.data + '\n'
        s += self.lang + '\n'
        s += self.buildName + '\n'
        for _, block in self.object_ids.items():
            s += block.convertToStr() + '\n'

        if save:
            self.fileName = fileName
            file = open(fileName, 'wt')
            file.write(s)
            file.close()
        else:
            print('Save log:')
            print(s)


    def open(self, fileName):
        """Загружает из файла"""
        self.max_id = 0
        self.object_ids = {}
        self.fileName = fileName

        file = open(fileName, 'rt')
        self.data = file.readline()[:-1]
        self.lang = file.readline()[:-1]
        self.buildName = file.readline()[:-1]
        for line in file:
            if len(line.strip()) == 0 or line.strip()[0] == ';':
                continue  # пустые строки и строки-комментарии пропускаем
            type = literal_eval(line)["type"]
            if type in allTypes:
                Block(self, line.strip(), creating_type=1)
            else:
                print(f'Unknown type of block! Line: "{line}"')

    def parents(self, id):
        """Возвращает id всех блоков, для которых данный является дочерним"""
        res = []
        for i, obj in self.object_ids.items():
            if id in obj.childs:
                res = res + [i]
        return res


    def build(self, fileName, save=1):
        """Составляет текст программы и сохраняет его в файл"""
        s = ''
        tab = ''

        rootBlock = Block(self, type='op')
        for i, _ in self.object_ids.items():
            if not self.parents(i):
                rootBlock.addLink(i)
        rootBlock.sortChilds()
        s, tab = rootBlock.build(s, tab)
        rootBlock.delete()

        if save:
            self.buildName = fileName
            file = open(self.buildName, 'wt')
            file.write(s)
            file.close()
        else:
            print('Build log:')
            print(s)


class Block:
    """
    Класс блока
    SF - SourceFile, в котором находится данный блок
    text_editor - tk окно редактора данного блока
    chosen - является ли блок выбран мышью для перетаскивания
    id - id
    childs - список id дочерних блоков
    pos - Point позиция блока на холсте
    classname - тип блока строкой
    data - словарь данных блока для подстановок
    """
    #__slots__ = "classname", "id", "childs", "pos", "text"
    def __init__(self, SF, str='', type='_', creating_type=0, chosen=False):
        self.SF = SF
        self.text_editor = None
        self.chosen = chosen
        self.shift_id = None
        # creating_type == 0 - создание нового элемента
        # creating_type == 1 - парсинг элемента из файла
        if creating_type == 1:
            self.parseFromStr(str)
            self.SF.object_ids[self.id] = self
            self.SF.max_id = max(self.SF.max_id, self.id + 1)
        else:
            max_id = len(SF.object_ids)

            self.id = SF.max_id
            self.childs = []
            self.pos = Point(0, 0)
            self.data = {}
            self.classname = type

            for key, val in allTypes[self.classname]['edit'].items():
                self.data[key] = ''

            SF.object_ids[self.id] = self
            SF.max_id += 1
            # self.title = ""
            # self.tooltip = ""
        self.SF.object_ids[self.id] = self


    def delete(self):
        """Удаляет ссылку на себя из SF и свой id из всех блоков"""
        SF.object_ids.pop(self.id)
        for _, block in SF.object_ids.items():
            if self.id in block.childs:
                block.childs.remove(self.id)

    def move(self, shift):
        """Сдвигает блок на холсте"""
        self.pos = (self.pos + shift).round()

    def edit(self, master, canvas):
        """Открывает редактор блока"""
        self.text_editor = master
        text_editor.TextEditor(master, self, canvas)
        #self.text = newstr

    def convertToStr(self):
        """Конвертирует блок в строку-словарь"""
        result = '{"type":"'+str(self.classname)+'", "id":'+str(self.id)+', "childs":'+str(self.childs)+', "pos":'+str(self.pos)+', "data":'+str(self.data)+'}'
        result = result.replace('\n', '\\n')
        return result

    def parseFromStr(self, s):
        """Распаковывает блок из строки-словаря"""
        dct = literal_eval(s)
        self.classname = dct["type"]
        self.id = dct["id"]
        self.childs = dct["childs"]
        self.pos = Point().fromTuple(dct["pos"])
        self.data = dct["data"]

        # self.data = None
        # for _, attr in data.items():
        #     if attr in dct:
        #         setattr(self.data, attr, dct[attr])


    def formatStr(self, s):
        """Применяет к строке s все подстановки из self.data"""
        res = s
        for key, val in self.data.items():
            if key in res:
                res = res.replace(key, val)
        return res

    def formatStrOp(self):
        """Операторная форма formatStr"""
        return lambda s: self.formatStr(s)

    def build(self, s, tab):
        """Возвращает строку: текст программы, которую описывает данный блок"""
        self.sortChilds()

        behavior = getSettingsByLang(self.SF.lang)[self.classname]['build']
       
        repl = self.formatStrOp()

        prefix = repl(behavior["prefix"])
        if behavior["hasPostfix"]:
            postfix = repl(behavior["postfix"])
        
        if behavior["multiline"]:
            for line in prefix.split('\n'):
                s += tab + line + '\n'
        else:
            s += tab + prefix + '\n'

        if behavior["incTab"]:
            tab += '    '

        for child_id in self.childs:
            child = self.SF.object_ids[child_id]
            s, tab = child.build(s, tab)
        if behavior["incTab"]:
            tab = tab[:-4]
        if behavior["hasPostfix"]:
            if behavior["multiline"]:
                for line in postfix.split('\n'):
                    s += tab + line + '\n'
            else:
                s += tab + postfix + '\n'
        return s, tab

    def sortChilds(self):
        """Сортирует дочерние элементы блока по положению на холсте"""
        self.childs.sort(key=lambda id: self.SF.object_ids[id].pos)

    def addLink(self, child):
        """Добавляет дочерний элемент"""
        if not (child in self.childs) and (child != self.id):
            self.childs.append(child)

    def delLink(self, child):
        """Удаляет дочерний элемент"""
        if child in self.childs:
            self.childs.remove(child)

    def parents(self):
        """Возвращает id всех блоков, для которых данный является дочерним"""
        return self.SF.parents(self.id)

    def shift(self, shift, desc=0, shift_id=0):
        if not desc:
            self.pos += shift
        else:
            if shift_id != self.shift_id:
                self.pos += shift
                self.shift_id = shift_id
                for child in self.childs:
                    self.SF.object_ids[child].shift(shift, desc, shift_id)

if __name__ == "__main__":
    print("This module is not for direct call!")
