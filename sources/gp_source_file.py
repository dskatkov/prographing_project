import text_editor
from settings import *
from utils import *
from gp_block_manager import *

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
        self.changeLang('python')
        self.wasEdited = False

    def changeLang(self, lang):
        self.lang = lang
        change_lang(lang)

    def save(self, fileName='', save=1):
        """Сохраняет в файл/save into file"""
        self.wasEdited = False

        self.data += 1

        data = {
            'subversion': self.data,
            'lang': self.lang,
            'build_path': self.buildName,
            'blocks': [val.toDict() for key, val in self.object_ids.items()]
        }

        if save:
            if fileName:
                self.fileName = fileName
                with open(self.fileName, 'w') as outfile:
                    json.dump(data, outfile, indent=4)
        else:
            print('Save log:')
            print(json.dumps(data, indent=4))

    def open(self, fileName):
        """Загружает из файла/ load from file"""
        self.wasEdited = False

        obj = json_load(fileName)

        self.max_id = 0
        self.object_ids = {}
        self.fileName = fileName

        self.data = obj["subversion"]
        if isinstance(self.data, int):
            self.data = int(self.data)
        else:
            debug_return(f'Bad subversion: {self.data}; setting subversion to {0}')
            self.data = 0

        self.changeLang(obj["lang"])
        self.buildName = obj["build_path"]
        blocks = obj["blocks"]
        for b in blocks:
            block_type = b['type']
            if block_type in allTypes:
                Block(self, b, creating_type=1)
            else:
                raise Exception(f'Unknown type of block: {block_type}! \nBlock: "{b}\nallTypes: {allTypes}"')

            # line = str(b)
            # if len(line.strip()) == 0 or line.strip()[0] == ';':
            #     continue  # пустые строки и строки-комментарии пропускаем/ leave empty and comment strings
            # type = literal_eval(line)["type"]
            # if type in allTypes:
            #     Block(self, line.strip(), creating_type=1)
            # else:

    def parents(self, block_id):
        """Возвращает id всех блоков, для которых данный является дочерним/ return ids of all child blocks"""
        res = []
        for i, obj in self.object_ids.items():
            if block_id in obj.childs:
                res = res + [i]
        return res

    def build(self, fileName, save=1):
        """Составляет текст программы и сохраняет его в файл/ create program text and save it to file"""

        rootBlock = Block(self, block_type='empty')
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

    def closeQ(self):
        return not self.wasEdited

    def __del__(self):
        for _, block in self.object_ids.items():
            del block
        self.object_ids = {}


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
    # __slots__ = "classname", "id", "childs", "pos", "text"

    def __init__(self, SF, data=None, block_type='undefined', creating_type=0, chosen=False):
        self.SF = SF
        self.text_editor = None
        self.chosen = chosen
        self.shift_id = None
        # creating_type == 0 - создание нового элемента/creation of new element
        # creating_type == 1 - парсинг элемента из файла/ parcing from file
        if creating_type == 1:
            self.fromDict(data)
            self.SF.object_ids[self.id] = self
            self.SF.max_id = max(self.SF.max_id, self.id + 1)
        else:
            self.id = SF.max_id
            self.childs = []
            self.pos = Point(0, 0)
            self.data = {}
            self.classname = block_type

            for key, val in getDictValByPath(allTypes, f'{self.classname}.edit').items():
                self.data[key] = ''

            SF.object_ids[self.id] = self
            SF.max_id += 1
            # self.title = ""
            # self.tooltip = ""
        self.SF.object_ids[self.id] = self

    def delete(self):
        """Удаляет ссылку на себя из SF и свой id из всех блоков/ delete link to itself from SF and its id"""
        self.SF.wasEdited = True
        if self.id in self.SF.object_ids:
            self.SF.object_ids.pop(self.id)
        for _, block in SF.object_ids.items():
            if self.id in block.childs:
                block.childs.remove(self.id)
        if self.text_editor:
            self.text_editor.destroy()

    def move(self, shift):
        """Сдвигает блок на холсте/ move block on canvas"""
        self.SF.wasEdited = True
        self.pos = (self.pos + shift).round()

    def edit(self, master, canvas):
        """Открывает редактор блока/ open block redactor"""
        self.SF.wasEdited = True
        self.text_editor = master
        text_editor.TextEditor(master, self, canvas)

    def convertToStr(self):
        """Конвертирует блок в строку-словарь/ convert block into dictionary"""
        result = '{"type":"'+str(self.classname)+'", "id":'+str(self.id)+', "childs":'+str(
            self.childs)+', "pos":'+str(self.pos)+', "data":'+str(self.data)+'}'
        result = result.replace('\n', '\\n')
        return result

    def fromDict(self, d):
        """Распаковывает блок из строки-словаря/ parse block from dictionary - string"""
        # dct = literal_eval(s)
        self.classname = d["type"]
        self.id = d["id"]
        self.childs = d["childs"]
        self.pos = Point().fromTuple(d["pos"])
        self.data = d["data"]

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
        """Возвращает строку: текст программы, которую описывает данный блок
        / return string: text of the program which block describe"""
        self.sortChilds()

        tab = 0

        hasPrefix = getDictValByPath(
            allTypes, f'{self.classname}.build.hasPrefix'
        )
        prefix = getDictValByPath(
            allTypes, f'{self.classname}.build.prefix'
        )
        hasPostfix = getDictValByPath(
            allTypes, f'{self.classname}.build.hasPostfix'
        )
        postfix = getDictValByPath(
            allTypes, f'{self.classname}.build.postfix'
        )
        multiline = getDictValByPath(
            allTypes, f'{self.classname}.build.multiline'
        )
        incTab = getDictValByPath(
            allTypes, f'{self.classname}.build.incTab'
        )

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
        self.childs.sort(key=lambda block_id: self.SF.object_ids[block_id].pos)

    def addLink(self, child):
        """Добавляет дочерний элемент/ add child"""
        self.SF.wasEdited = True
        if not (child in self.childs) and (child != self.id):
            self.childs.append(child)

    def delLink(self, child):
        """Удаляет дочерний элемент/ delete child"""
        self.SF.wasEdited = True
        if child in self.childs:
            self.childs.remove(child)

    def parents(self):
        """Возвращает id всех блоков, для которых данный является дочерним/Return all parent blocks"""
        return self.SF.parents(self.id)

    def shift(self, shift, desc=0, shift_id=0):
        self.SF.wasEdited = True
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
            getDictValByPath(allTypes, f'{self.classname}.canvas.tooltip')
        )

    def getSub(self):
        return self.formatStr(
            getDictValByPath(allTypes, f'{self.classname}.canvas.desc')
        )

    def changeType(self, newType):
        self.SF.wasEdited = True
        self.classname = newType
        self.data = {}
        for key_, _ in getDictValByPath(allTypes, f'{self.classname}.edit').items():
            self.data[key_] = ''

    def toDict(self):
        return {
            'type': self.classname,
            'id': self.id,
            'childs': self.childs,
            'pos': list(self.pos.tuple()),
            'data': self.data,
        }


if __name__ == "__main__":
    print("This module is not for direct call!")
