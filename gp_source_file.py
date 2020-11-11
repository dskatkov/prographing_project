
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
                classnames[type](line.strip())
            else:
                print(f'Unknown type of block! Line: "{line}"')

    def build(self, fileName):
        self.buildName = fileName
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
            self.pos = (0, 0)
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

    # def convertToStr(self):
    #     print("Not implemented!")

    # def parseFromStr(self, str):
    #     print("Not implemented!")

    def convertToStr(self):
        return '{"type":"'+str(self.classname)+'", "id":'+str(self.id)+', "childs":'+str(self.childs)+', "pos":'+str(self.pos)+', "text":"'+str(self.text)+'"}'

    def parseFromStr(self, s):
        dct = eval(s)
        self.id = dct["id"]
        self.childs = dct["childs"]
        self.pos = dct["pos"]
        self.text = dct["text"]

        SF.object_ids[self.id] = self
        SF.max_id = max(SF.max_id, self.id + 1)

    def draw(self):
        print("Not implemented!")

    def drawLink(self, child):
        print("Not implemented!")


class BlockOp(Block):
    #__slots__ = "classname", "id", "childs", "pos", "text"
    classname = "Op"

    def draw(self):
        print("Not implemented!")

    def drawLink(self, child):
        print("Not implemented!")




SF = SourceFile()
classnames = {v.classname: v for v in (Block,BlockOp,)}

if __name__ == "__main__":
    print("This module is not for direct call!")
