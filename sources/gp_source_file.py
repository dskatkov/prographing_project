from ast import literal_eval

import text_editor
from settings import *
from utils import *

SF = ...

class SourceFile:
    """
    Класс графической программы/ class of grafical program
        max_id = 0 - максимальный id блоков/ max block id
        object_ids = {} - словарь ссылок на блоки {<id>:<блок>}/ dictionary of links to blocks {<id>:<block>}
        fileName = '' - файл для сохранение/ File for saving
        buildName = '' - файл для составления текста программы/ file for experting program
        data = 0 - subversion
        lang = 'py' - язык составления программы/language of export
    """
    def __init__(self):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = ''
        self.buildName = ''
        self.data = 0
        self.lang = 'py'


    def save(self, fileName, save=1):
        """Сохраняет в файл/save into file"""
        self.data += 1
        s = ''
        s += str(self.data) + '\n'
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
        """Загружает из файла/ load from file"""
        self.max_id = 0
        self.object_ids = {}
        self.fileName = fileName

        file = open(fileName, 'rt')
        self.data = int(file.readline()[:-1])
        try:
            self.data = int(self.data)
        except ValueError:
            debug_return(f'bad subversion: {self.data}; setting subversion to {0}')
            self.data = 0
        self.lang = file.readline()[:-1]
        self.buildName = file.readline()[:-1]
        for line in file:
            if len(line.strip()) == 0 or line.strip()[0] == ';':
                continue  # пустые строки и строки-комментарии пропускаем/ leave empty and comment strings
            type = literal_eval(line)["type"]
            if type in allTypes:
                Block(self, line.strip(), creating_type=1)
            else:
                print(f'Unknown type of block! Line: "{line}"')

    def parents(self, id):
        """Возвращает id всех блоков, для которых данный является дочерним/ return ids of all child blocks"""
        res = []
        for i, obj in self.object_ids.items():
            if id in obj.childs:
                res = res + [i]
        return res


    def build(self, fileName, save=1):
        """Составляет текст программы и сохраняет его в файл/ create program text and save it to file"""

        rootBlock = Block(self, type='op')
        for i, _ in self.object_ids.items():
            if not self.parents(i):
                rootBlock.addLink(i)
        rootBlock.sortChilds()
        s = rootBlock.build('')
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
    Класс блока/ Block class
    SF - SourceFile, в котором находится данный блок/ SourceFile of this block
    text_editor - tk окно редактора данного блока/ tk redactor window of this block
    chosen - является ли блок выбран мышью для перетаскивания/ is this block chosen by mose for movement?
    id - id
    childs - список id дочерних блоков/ list of child's ids
    pos - Point позиция блока на холсте/ position on the canvas in Point format
    classname - тип блока строкой/ string of block type
    data - словарь данных блока для подстановок/ dictionary of block data for inserting
    """
    #__slots__ = "classname", "id", "childs", "pos", "text"
    def __init__(self, SF, str='', type='?', creating_type=0, chosen=False):
        self.SF = SF
        self.text_editor = None
        self.chosen = chosen
        self.shift_id = None
        # creating_type == 0 - создание нового элемента/creation of new element
        # creating_type == 1 - парсинг элемента из файла/ parcing from file
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

            for key, val in getDictValByPathDef(allTypes, f'<1>.edit.<2>', self.classname, self.SF.lang).items():
                self.data[key] = ''

            SF.object_ids[self.id] = self
            SF.max_id += 1
            # self.title = ""
            # self.tooltip = ""
        self.SF.object_ids[self.id] = self


    def delete(self):
        """Удаляет ссылку на себя из SF и свой id из всех блоков/ delete link to itself from SF and its id"""
        SF.object_ids.pop(self.id)
        for _, block in SF.object_ids.items():
            if self.id in block.childs:
                block.childs.remove(self.id)

    def move(self, shift):
        """Сдвигает блок на холсте/ move block on canvas"""
        self.pos = (self.pos + shift).round()

    def edit(self, master, canvas):
        """Открывает редактор блока/ open block redactor"""
        self.text_editor = master
        text_editor.TextEditor(master, self, canvas)

    def convertToStr(self):
        """Конвертирует блок в строку-словарь/ convert block into dictionary"""
        result = '{"type":"'+str(self.classname)+'", "id":'+str(self.id)+', "childs":'+str(self.childs)+', "pos":'+str(self.pos)+', "data":'+str(self.data)+'}'
        result = result.replace('\n', '\\n')
        return result

    def parseFromStr(self, s):
        """Распаковывает блок из строки-словаря/ parce block from dictionary - string"""
        dct = literal_eval(s)
        self.classname = dct["type"]
        self.id = dct["id"]
        self.childs = dct["childs"]
        self.pos = Point().fromTuple(dct["pos"])
        self.data = dct["data"]

    def formatStr(self, s):
        """Применяет к строке s все подстановки из self.data/ implement all implements of self.data to the string"""
        res = s
        for key, val in self.data.items():
            if key in res:
                res = res.replace(key, val)
        return res

    def formatStrOp(self):
        """Операторная форма formatStr/ operator form"""
        return lambda s: self.formatStr(s)

    def build(self, s, t='    '):
        """Возвращает строку: текст программы, которую описывает данный блок/ return string: text of the program which block describe"""
        self.sortChilds()

        tab = 0

        hasPrefix  = getDictValByPathDef(allTypes, '<1>.build.<2>.hasPrefix',  self.classname, self.SF.lang)
        prefix     = getDictValByPathDef(allTypes, '<1>.build.<2>.prefix',     self.classname, self.SF.lang)
        hasPostfix = getDictValByPathDef(allTypes, '<1>.build.<2>.hasPostfix', self.classname, self.SF.lang)
        postfix    = getDictValByPathDef(allTypes, '<1>.build.<2>.postfix',    self.classname, self.SF.lang)
        multiline  = getDictValByPathDef(allTypes, '<1>.build.<2>.multiline',  self.classname, self.SF.lang)
        incTab     = getDictValByPathDef(allTypes, '<1>.build.<2>.incTab',     self.classname, self.SF.lang)

        repl = self.formatStrOp()

        if hasPrefix:
            prefix = repl(prefix)
            if prefix:
                if multiline:
                    for line in prefix.split('\n'):
                        s += tab*t + line + '\n'
                else:
                    s += tab*t + prefix + '\n'

        tab += incTab

        ch_s = ''
        for child_id in self.childs:
            child = self.SF.object_ids[child_id]
            try:
                ch_s = child.build(ch_s)
            except Exception:
                print(f'Exception gp_source_file.py Block.build')


        for line in ch_s.split('\n'):
            if line:
                s += tab*t + line + '\n'

        tab -= incTab

        if hasPostfix:
            postfix = repl(postfix)
            if postfix:
                if multiline:
                    for line in postfix.split('\n'):
                        s += tab*t + line + '\n'
                else:
                    s += tab*t + postfix + '\n'

        return s

    def sortChilds(self):
        """Сортирует дочерние элементы блока по положению на холсте/ sort child elements by placement on the canvas"""
        self.childs.sort(key=lambda id: self.SF.object_ids[id].pos)

    def addLink(self, child):
        """Добавляет дочерний элемент/ add child"""
        if not (child in self.childs) and (child != self.id):
            self.childs.append(child)

    def delLink(self, child):
        """Удаляет дочерний элемент/ delete child"""
        if child in self.childs:
            self.childs.remove(child)

    def parents(self):
        """Возвращает id всех блоков, для которых данный является дочерним/Retern all parent blocks"""
        return self.SF.parents(self.id)

    def shift(self, shift, desc=0, shift_id=0):
        if not desc:
            self.pos += shift
        else:
            if shift_id != self.shift_id:
                self.pos += shift
                self.shift_id = shift_id
                for child in self.childs:
                    try:
                        self.SF.object_ids[child].shift(shift, desc, shift_id)
                    except Exception:
                        print(f'Exception gp_source_file.py Block.shift')
    def getTooltip(self):
        return self.formatStr(
            getDictValByPathDef(allTypes, f'<1>.canvas.<2>.tooltip', self.classname, self.SF.lang)
        )

    def getSub(self):
        return self.formatStr(
            getDictValByPathDef(allTypes, f'<1>.canvas.<2>.desc', self.classname, self.SF.lang)
        )

    def changeType(self, newType):
        self.classname = newType
        self.data = {}
        for key_, _ in getDictValByPathDef(allTypes, f'<1>.edit.<2>', self.classname, self.SF.lang).items():
            self.data[key_] = ''


if __name__ == "__main__":
    print("This module is not for direct call!")
