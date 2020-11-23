import gp_source_file as source_file
from settings import *
from utils import *

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
        """Рисует холст (блоки + линки)"""
        # Очистка
        self.SF = SF
        self.master.delete("all")
        self.master.create_rectangle(0, 0, 2000, 2000, fill=textBG)

        # Линки
        for _, block in SF.object_ids.items():
            for child in block.childs:
                self.drawLink(block, SF.object_ids[child])
        if self.link_creation:
            self.drawLink(self.handling, self.link_creation)

        # Блоки
        for _, block in SF.object_ids.items():
            self.drawBlock(block)

        # Подписи
        for _, block in SF.object_ids.items():
            self.drawBlockText(block)


    def scale(self, pos):
        """положение на холсте -> положение на экране"""
        return (pos - self.viewpos) * self.viewzoom # vecMul(vecSum(pos, vecMul(self.viewpos, -1)), self.viewzoom) # (pos-viewpos)*zoom

    def unscale(self, pos):
        """положение на экране -> положение на холсте"""
        return pos * (1 / self.viewzoom) + self.viewpos # vecSum(self.viewpos, vecMul(pos, 1/self.viewzoom)) # pos/zoom+viewpos

    def drawBlock(self, block):
        """Рисует блок"""
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


        if block.chosen:
            R = chosen_R * r
            self.master.create_oval((x - R), (y - R), (x + R), (y + R), fill=chosenCol)
        self.master.create_oval((x - r), (y - r), (x + r), (y + r), fill=color)

    def drawBlockText(self, block):
        x, y = self.scale(block.pos).tuple()
        r = blockR * self.viewzoom
        fontsize = round(font_size*self.viewzoom)
        text = block.getSub()
        if fontsize:
            self.master.create_text(x + 1.5 * r, y - fontsize, text=text, anchor='w', font="Consolas "+str(fontsize))


    def drawLink(self, block, child):
        """Рисует линк"""
        x1, y1 = self.scale(block.pos).tuple()
        thickness = link_width * self.viewzoom
        if isinstance(child, Point):
            x2, y2 = child.tuple()
            color = linkColores['_']
        else:
            x2, y2 = self.scale(child.pos).tuple()
            # Поиск наиболее подходящего цвета из списка
            pair = block.classname + '_' + child.classname
            left = block.classname + '_'
            right = '_' + child.classname
            if pair in linkColores:
                color = linkColores[pair]
            elif left in linkColores:
                color = linkColores[left]
            elif right in linkColores:
                color = linkColores[right]
            else:
                color = linkColores['_']

        self.master.create_line(x1, y1, x2, y2, fill=color, width=thickness)
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        if dist == 0:
            return
        l = arrow_length/dist*self.viewzoom
        dif = (blockR * self.viewzoom) / dist
        if not isinstance(child, Point):
            x2, y2 = dif * x1 + (1 - dif) * x2, dif * y1 + (1 - dif) * y2
        x3, y3 = (1 - l) * x2 + l * x1, (1 - l) * y2 + l * y1
        a = (x2 - x1)  # 1/A
        b = (y1 - y2)  # 1/B
        w = arrow_width * self.viewzoom
        # нормирование/normalizing
        n = 1 / (a ** 2 + b ** 2) ** 0.5
        w *= n
        x4, x5 = x3 + w * b, x3 - w * b
        y4, y5 = y3 + w * a, y3 - w * a
        self.master.create_line(x2, y2, x4, y4, fill=color, width=thickness)
        self.master.create_line(x2, y2, x5, y5, fill=color, width=thickness)


if __name__ == "__main__":
    print("This module is not for direct call!")
