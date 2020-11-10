class Canvas:
    def __init__(self, master):
        ...
    def draw(self):
        for block in sourceFile.listOfBlocks:
            block.draw()
            for child in block.childs:
                block.drawLink(child)

