class Canvas:
    def __init__(self, master):
        self.master = master
    def draw(self, SF):
        for _, block in SF.object_ids.items():
            print (1)
            block.draw(self.master)
            for child in block.childs:
                block.drawLink(child, screen)

if __name__ == "__main__":
    print("This module is not for direct call!")
