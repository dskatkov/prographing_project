from utils import Point


class SourceFile:
    def __init__(self):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = ""
        self.type = "SOURCE FILE"

    def save(self, fileName):
        self.fileName = fileName
        file = open(fileName, 'rt')

    def open(self, fileName):
        self.max_id = 0
        self.object_ids = {}
        self.fileName = fileName
        file = open(fileName, 'rt')
        for s in file:
            if s:
                classnames[s.split()[0]](s)

    def build(self, fileName):
        ...

    def addLink(self, beginBlock, endBlock):
        ...

    def delLink(self, beginBlock, endBlock):
        ...


SF = SourceFile()

# class Link:
#     def __init__(self, begin, end):
#         ...

#     def delLink():
#         ...



# classname id childs pos text
class Block:
    #__slots__ = "classname", "id", "childs", "pos", "text"
    classname = "TBlock"
    def __init__(self, str=''):
        if str != '':
            self.parseFromStr(str)
        else:
            self.id = max_id
            self.childs = []
            self.pos = Point(0, 0)
            self.text = ''

            SF.object_ids[self.id] = self
            SF.max_id += 1
            # self.title = ""
            # self.tooltip = ""
        SF.object_ids[self.id] = self

    def __del__(self):
        SF.object_ids[self.id] = None

    def move(self, newpos):
        self.pos = newpos

    def edit(self, newstr):
        self.text = newstr

    def convertToStr(self):
        print("Not implemented!")

    def parseFromStr(self, str):
        print("Not implemented!")

    def draw(self):
        print("Not implemented!")

    def drawLink(self, child):
        print("Not implemented!")


class BlockOp(Block):
    #__slots__ = "classname", "id", "childs", "pos", "text"
    classname = "Op"

    def convertToStr(self):
        return f"{self.classname} {self.id} {self.childs} {self.pos} {self.text}"

    def parseFromStr(self, str):
        tokens = str.split()
        # if tokens[0].lower() != self.classname:
        #     return
        # if len(tokens) != 8:
        #     return
        self.id = int(tokens[1])
        self.childs = eval(tokens[2])
        self.pos = Point().fromStr(tokens[3])
        self.text = tokens[4]

        SF.object_ids[self.id] = self
        SF.max_id = max(SF.max_id, self.id + 1)

    def draw(self):
        print("Not implemented!")

    def drawLink(self, child):
        print("Not implemented!")



classnames = {v.classname: v for v in (Block,BlockOp,)}
