from utils import Point

class SourceFile:
    def __init__(self):
        self.fileName = ""
        self.type = ""
        self.listOfBlocks = []

    def save(self, fileName):
        self.fileName = fileName
        ...

    def open(self, fileName):
        ...

    def build(self, fileName):
        ...

    def addLink(self, beginBlock, endBlock):
        ...

    def delLink(self, beginBlock, endBlock):
        ...

# class Link:
#     def __init__(self, begin, end):
#         ...

#     def delLink():
#         ...

class Block:
    classname = "TBlock"

    def __init__(self, str=''):
        if str:
            self.parseFromStr(str)
        else:
            self.pos = Point(0, 0)
            self.childs = []
            self.text = ""
            # self.title = ""
            # self.tooltip = ""
        SF.listOfBlocks.append(self)

    def __del__():
        SF.listOfBlocks.remove(self)

    def move():
        ...

    def edit():
        ...

    def saveToFile(self):
        print("Not implemented!")

    def parseFromStr(self, str):
        print("Not implemented!")

    def draw(self):
        print("Not implemented!")

    def drawLink(self, child):
        print("Not implemented!")

