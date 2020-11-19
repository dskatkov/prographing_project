import gp_source_file as source_file

canvas = ...

class Canvas:
    def __init__(self, master=None):
        self.master = master

    def draw(self, SF):
    	#self.master.clear()
        for _, block in SF.object_ids.items():
            for child in block.childs:
                block.drawLink(SF.object_ids[child], self.master)
            block.draw(self.master)

if __name__ == "__main__":
    print("This module is not for direct call!")