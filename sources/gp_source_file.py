import tkinter as tk
import tkinter.ttk
from os import getcwd
#import math as m
from PIL import Image, ImageTk

import text_editor
from settings import *
from utils import *

SF = ...

class SourceFile:
    def __init__(self):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = ''
        self.buildName = ''
        self.data = '---'
        self.lang = 'py'

    def save(self, fileName, save=1):
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
            type = eval(line)["type"]
            if type in blockTypes:
                Block(self, line.strip(), creating_type=1)
            else:
                print(f'Unknown type of block! Line: "{line}"')

    def parents(self, id):
        res = []
        for i, obj in self.object_ids.items():
            if id in obj.childs:
                res = res + [i]
        return res

    def build(self, fileName, save=1):
        s = ''
        tab = ''
        for i, obj in self.object_ids.items():
            if not self.parents(i):
                s, tab = obj.build(s, tab)

        if save:
            self.buildName = fileName
            file = open(self.buildName, 'wt')
            file.write(s)
            file.close()
        else:
            print('Build log:')
            print(s)

# {
#     "type": "Op",
#     "id": 8,
#     "childs": [],
#     "pos": (325, 150),
#     "data": {
#         "text1": "op_8"
#     }
# }
class Block:
    #__slots__ = "classname", "id", "childs", "pos", "text"
    def __init__(self, SF, str = '', type = '_', creating_type = 0, chosen = False):
        self.SF = SF
        self.text_editor = None
        self.chosen = chosen
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
            self.pos = (0, 0)
            self.data = {}
            self.classname = type

            for key, val in allTypes[self.classname]['edit'].items():
                self.data[key] = ''

            SF.object_ids[self.id] = self
            SF.max_id += 1
            # self.title = ""
            # self.tooltip = ""
        self.SF.object_ids[self.id] = self

    def __del__(self):
        self.SF.object_ids.remove(self.id)

    def move(self, shift):
        self.pos = (self.pos[0] + shift[0], self.pos[1] + shift[1])

    def edit(self, master, canvas):
        print('here edition window is opening')
        self.text_editor = master
        text_editor.TextEditor(master, self, canvas)
        #self.text = newstr

    def convertToStr(self):
        result = '{"type":"'+str(self.classname)+'", "id":'+str(self.id)+', "childs":'+str(self.childs)+', "pos":'+str(self.pos)+', "data":'+str(self.data)+'}'
        result = result.replace('\n', '\\n')
        return result

    def parseFromStr(self, s):
        dct = eval(s)
        self.classname = dct["type"]
        self.id = dct["id"]
        self.childs = dct["childs"]
        self.pos = dct["pos"]
        self.data = dct["data"]

        # self.data = None
        # for _, attr in data.items():
        #     if attr in dct:
        #         setattr(self.data, attr, dct[attr])

    def formatStrOp(self):
        return lambda s: self.formatStr(s)

    def formatStr(self, s):
        res = s
        for key, val in self.data.items():
            if key in res:
                res = res.replace(key, val)
        return res


    def build(self, s, tab):
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
        self.childs.sort(key=lambda id: self.SF.object_ids[id].pos)

    def addLink(self, child):
        if not (child in self.childs):
            self.childs.append(child)

    def delLink(self, child):
        if child in self.childs:
            self.childs.remove(child)

    def parents(self):
        return self.SF.parents(self.id)

if __name__ == "__main__":
    print("This module is not for direct call!")
