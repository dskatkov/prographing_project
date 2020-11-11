class Canvas:
    def __init__(self, master):
        ...
    def draw(self):
        for block in sourceFile.listOfBlocks:
            block.draw()
            for child in block.childs:
                block.drawLink(child)

if __name__ == "__main__":
    print("This module is not for direct call!")