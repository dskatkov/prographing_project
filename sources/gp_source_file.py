import tkinter as tk
import tkinter.ttk
from os import getcwd
#import math as m
#from PIL import Image, ImageTk

from settings import *

SF = ...

class SourceFile:
    def __init__(self):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = ''
        self.buildName = ''
        self.data = '---'
        self.lang = 'dab'

    def save(self, fileName):
        self.fileName = fileName
        file = open(fileName, 'wt')
        file.write(self.data + '\n')
        file.write(self.lang + '\n')
        file.write(self.buildName + '\n')
        for _, block in self.object_ids.items():
            file.write(block.convertToStr() + '\n')
        file.close()


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

    def build(self, fileName):
        self.buildName = fileName
        s = ''
        tab = ''
        for i, obj in self.object_ids.items():
            if self.parents(i) == []:
                s, tab = obj.build(s, tab)
        print(s)
        file = open(self.buildName, 'wt')
        file.write(s)
        file.close()


# classname id childs pos text
class Block:
    #__slots__ = "classname", "id", "childs", "pos", "text"
    classname = "_"
    incTab = 0
    hasPostfix = 0

    def __init__(self, SF, str='', r = 10, creating_type=0):
        self.SF = SF
        # creating_type == 0 - создание нового элемента
        # creating_type == 1 - парсинг элемента из файла
        if creating_type == 1:
            self.parseFromStr(str)
            self.SF.object_ids[self.id] = self
            self.SF.max_id = max(self.SF.max_id, self.id + 1)
        else:

            max_id = len(SF.object_ids) + 1

            self.id = max_id
            self.childs = []
            self.pos = (0, 0)
            self.text = ''

            self.SF.object_ids[self.id] = self
            self.SF.max_id += 1
            # self.title = ""
            # self.tooltip = ""
        self.SF.object_ids[self.id] = self
        self.r = r

    def __del__(self):
        self.SF.object_ids[self.id] = None

    def move(self, newpos):
        self.pos = newpos

    def edit(self):
        print('here edition window is opening')
        #self.text = newstr

    def convertToStr(self):
        return '{"type":"'+str(self.classname)+'", "id":'+str(self.id)+', "childs":'+str(self.childs)+', "pos":'+str(self.pos)+', "text1":"'+str(self.text1)+'"}'

    def parseFromStr(self, s):
        dct = eval(s)
        self.classname = dct["type"]
        self.id = dct["id"]
        self.childs = dct["childs"]
        self.pos = dct["pos"]
        # Возможность добавлять несколько текстовых полей в блок. Еще не реализовано
        self.text1 = dct["text1"] if "text1" in dct else ""
        self.text2 = dct["text2"] if "text2" in dct else ""
        self.text3 = dct["text3"] if "text3" in dct else ""


    def build(self, s, tab):
        self.sortChilds()

        langs = blockTypes[self.classname]
        if self.SF.lang in langs:
            behavior = langs[self.SF.lang]
        elif '*' in langs:
            behavior = langs['*']
        else:
            behavior = {}

        for token in ["incTab","hasPostfix","prefix","postfix",]:
            if not (token in behavior): behavior[token]=langs['*'][token]
       
        repl = lambda s: s.replace('<1>', self.text1).replace('<2>', self.text2).replace('<3>', self.text3)
        prefix = repl(behavior["prefix"])
        if behavior["hasPostfix"]:
            postfix = repl(behavior["postfix"])
        
        s += tab + prefix + '\n'
        if behavior["incTab"]:
            tab += '    '
        for child_id in self.childs:
            child = self.SF.object_ids[child_id]
            s, tab = child.build(s, tab)
        if behavior["incTab"]:
            tab = tab[:-4]
        if behavior["hasPostfix"]:
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

    def prefix(self):
        print("Not implemented!")
        return ''

    def postfix(self):
        print("Not implemented!")
        return ''

    def draw(self, canvas):
        x, y = self.pos
        r = self.r

        # photo_ = Image.open(getcwd() + '\\Image\\' + self.classname + '.bmp')
        # photo = ImageTk.PhotoImage(photo_)
        # photo = tk.PhotoImage(file='C:\\GitHub\\prographing_project\\sources\\Image\\' + self.classname + '.gif')
        # print("image size: %dx%d" % (photo.width(), photo.height()))
        # canvas.create_image(x, y, image=photo, anchor='center') #не работает


        ct = self.classname
        if ct in drawColores:
            color = drawColores[ct]
        elif '_' in drawColores:
            color = drawColores['_']
        else:
            color = '#000000'

        canvas.create_oval((x - r), (y - r), (x + r), (y + r), fill=color)
        canvas.create_text(x, y, text=self.id, font="Consolas 10")

    def drawLink(self, child, canvas):
        x1, y1 = self.pos
        x2, y2 = child.pos
        r1, r2 = self.r, child.r
        x1, y1 = x1, y1 #TODO scale
        x2, y2 = x2, y2
        
        # Поиск наиболее подходящего цвета из списка
        ct = child.classname
        pair = self.classname + '_' + ct
        left = self.classname + '_'
        right = '_' + ct
        if pair in linkColores:
            color = linkColores[pair]
        elif left in linkColores:
            color = linkColores[left]
        elif right in linkColores:
            color = linkColores[right]
        elif '_' in linkColores:
            color = linkColores['_']
        else:
            color = '#000000'
 
        canvas.create_line(x1, y1, x2, y2, fill=color)

if __name__ == "__main__":
    print("This module is not for direct call!")
