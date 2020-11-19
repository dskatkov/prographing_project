import math as m

SF = ...

class SourceFile:
    def __init__(self):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = ''
        self.buildName = ''
        self.data = "SOURCE FILE"

    def save(self, fileName):
        self.fileName = fileName
        file = open(fileName, 'wt')
        file.write(self.data)
        file.write(self.buildName)
        for _, block in self.object_ids.items():
            file.write(block.convertToStr() + '\n')


    def open(self, fileName):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = fileName

        file = open(fileName, 'rt')
        self.data = file.readline()
        self.buildName = file.readline()
        for line in file:
            if len(line.strip()) == 0 or line.strip()[0] == ';':
                continue  # пустые строки и строки-комментарии пропускаем
            type = eval(line)["type"]
            if type in classnames:
                classnames[type](self, line.strip(), creating_type=1)
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




    def addLink(self, beginBlock, endBlock):
        ...

    def delLink(self, beginBlock, endBlock):
        ...



# class Link:
#     def __init__(self, begin, end):
#         ...

#     def delLink():
#         ...



# classname id childs pos text
class Block:
    #__slots__ = "classname", "id", "childs", "pos", "text"
    classname = "TBlock"
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

    def edit(self, newstr):
        self.text = newstr

    def convertToStr(self):
        return '{"type":"'+str(self.classname)+'", "id":'+str(self.id)+', "childs":'+str(self.childs)+', "pos":'+str(self.pos)+', "text":"'+str(self.text)+'"}'

    def parseFromStr(self, s):
        dct = eval(s)
        self.id = dct["id"]
        self.childs = dct["childs"]
        self.pos = dct["pos"]
        self.text = dct["text"]


    def build(self, s, tab):
        print("Not implemented!")

    def draw(self, screen):
        print("Not implemented!")

    def drawLink(self, child):
        print("Not implemented!")

    def build(self, s, tab):
        s += tab + self.prefix() + '\n'
        if self.incTab:
            tab += ' ' * 4
        for child_id in self.childs:
            child = self.SF.object_ids[child_id]
            s, tab = child.build(s, tab)
        if self.incTab:
            tab = tab[:-4]
        if self.hasPostfix:
            s += tab + self.postfix() + '\n'
        return s, tab

    def prefix(self):
        print("Not implemented!")
        return ''

    def postfix(self):
        print("Not implemented!")
        return ''

class BlockOp(Block):
    #__slots__ = "classname", "id", "childs", "pos", "text"
    classname = "Op"
    incTab = 0
    hasPostfix = 0

    def prefix(self):
        return self.text

    def postfix(self):
        print("Not implemented!")
        return ''

    def draw(self, canvas):
        x, y = self.pos
        r = self.r
        canvas.create_oval((x - r), (y - r), (x + r), (y + r), fill="blue")
        canvas.create_text(x, y, text=self.id, font="Consolas 10")

    def drawLink(self, child, canvas):
        x1, y1 = self.pos
        x2, y2 = child.pos
        r1, r2 = self.r, child.r
        x1, y1 = x1, y1 #TODO scale
        x2, y2 = x2, y2
        
        ct = child.classname
        if ct == 'Op': color = 'green'
        elif ct == 'If': color = 'red'
        else: color = 'white'

        canvas.create_line(x1, y1, x2, y2, fill=color)


class BlockIf(Block):
    #__slots__ = "classname", "id", "childs", "pos", "text"
    classname = "If"
    incTab = 1
    hasPostfix = 1

    def prefix(self):
        return 'if (' + self.text + ') {'

    def postfix(self):
        return '}'

    def draw(self, canvas):
        x, y = self.pos
        r = self.r
        canvas.create_oval((x - r), (y - r), (x + r), (y + r), fill="orange")
        canvas.create_text(x, y, text=self.id, font="Consolas 10")

    def drawLink(self, child, canvas):
        x1, y1 = self.pos
        x2, y2 = child.pos
        r1, r2 = self.r, child.r
        x1, y1 = x1, y1 #TODO scale
        x2, y2 = x2, y2
        
        ct = child.classname
        if ct == 'Op': color = 'red'
        elif ct == 'If': color = 'green'
        else: color = 'white'

        canvas.create_line(x1, y1, x2, y2, fill=color)




classnames = {v.classname: v for v in (Block,BlockOp,BlockIf,)}

if __name__ == "__main__":
    print("This module is not for direct call!")
