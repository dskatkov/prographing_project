from settings import *
from utils import *
from gp_block_manager import *

canvas = ...

class Canvas:
    def __init__(self, master=None):
        self.master = master
        self.viewpos = Point(0, 0)
        self.viewzoom = 10
        self.handling = None
        self.touch = None
        self.link_creation = None

    def draw(self, SF):
        """Рисует холст (блоки + линки)/ drawing canvas (blocks + links)"""
        # Очистка/Cleaning
        self.SF = SF
        try:
            self.master.delete("all")
        except Exception:
            print('Cannot delete all figures')
        self.master.create_rectangle(0, 0, 2000, 2000, fill=textBG)

        # Выбранный блок / Chosen block
        if self.handling:
            self.drawBlock(self.handling, chosen=1)

        # Линки/ Links
        for _, block in SF.object_ids.items():
            for child in block.childs:
                self.drawLink(block, SF.object_ids[child])
        if self.link_creation:
            self.drawLink(self.handling, self.link_creation, creating=1)

        # Блоки/Blocks
        for _, block in SF.object_ids.items():
            self.drawBlock(block)

        # Подписи/Subscription
        for _, block in SF.object_ids.items():
            self.drawBlockText(block)


    def scale(self, pos):
        """положение на холсте -> положение на экране/ Placement on canvas -> placement on screen"""
        return (pos - self.viewpos) * self.viewzoom

    def unscale(self, pos):
        """положение на экране -> положение на холсте/ placement on screen -> placement on canvas"""
        return pos * (1 / self.viewzoom) + self.viewpos

    def drawBlock(self, block, chosen=0):
        """Рисует блок/ Drawing block"""
        x, y = self.scale(block.pos).tuple()
        r = blockR * self.viewzoom

        # photo_ = Image.open(getcwd() + '\\Image\\' + block.classname + '.bmp')
        # photo = ImageTk.PhotoImage(photo_)
        # photo = tk.PhotoImage(file='C:\\GitHub\\prographing_project\\sources\\Image\\' + block.classname + '.gif')
        # print("image size: %dx%d" % (photo.width(), photo.height()))
        # canvas.create_image(x, y, image=photo, anchor='center') #не работает


        ct = block.classname
        if ct in drawColores:
            color = drawColores[ct]
        else:
            color = drawColores['?']

        if chosen:
            chosen_color = drawColores['chosen']
            R = chosen_R * self.viewzoom
            self.master.create_oval((x - R), (y - R), (x + R), (y + R), fill=chosen_color)
        else:
            self.master.create_oval((x - r), (y - r), (x + r), (y + r), fill=color)

    def drawBlockText(self, block):
        """делает подпись блока/Making block subscription"""
        x, y = self.scale(block.pos).tuple()
        r = blockR * self.viewzoom
        fontsize = round(font_size*self.viewzoom)
        text = block.getSub()
        if fontsize:
            self.master.create_text(x + 1.5 * r, y - fontsize, text=text, anchor='w', font="Consolas "+str(fontsize))


    def drawLink(self, block, child, creating=0):
        """Рисует линк/ Drawing link"""
        p1 = self.scale(block.pos)
        thickness = link_width * self.viewzoom
        if creating:
            p2 = child
            color = getDictValByPathDef(linkColores, '<1>_',  'creating', default='')
        else:
            p2 = self.scale(child.pos)
            color = getDictValByPathDef(linkColores, '<1>_<2>',  block.classname, child.classname, default='')

        if p1 == p2:
            return

        dist = p1.dist(p2)

        l = arrow_length * self.viewzoom / dist
        if not creating:
            l *= dist / (dist - blockR * self.viewzoom)

        if not creating:
            dif = (blockR * self.viewzoom) / dist
            p2 += (p1 - p2) * dif

        p3 = p2 - (p2 - p1) * l

        delta = p2.copy()
        delta -= p1
        delta.y *= -1
        delta.swapInPlace()

        w = arrow_width * self.viewzoom
        # нормирование/normalizing
        n = delta.norm() * w
        p4 = p3 + n
        p5 = p3 - n

        line_end = (p4 + p5)
        line_end /= 2
        line_end += (line_end - p1).norm() # костыль для отсутствия просвета

        self.master.create_line(*p1.tuple(), *line_end.tuple(), fill=color, width=thickness)
        self.master.create_polygon([*p2.tuple(), *p4.tuple(), *p5.tuple()], fill=color)




if __name__ == "__main__":
    print("This module is not for direct call!")
