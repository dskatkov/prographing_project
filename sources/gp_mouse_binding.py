import tkinter as tk
import tkinter.font
import time

from gp_mouse_binding import *
from settings import *
from utils import *
import gp_source_file as gp_source_file
import gp_canvas as gp_canvas

def assign_canvasFrame(canvasframe):
    global canvasFrame
    canvasFrame = canvasframe


def redraw():
    gp_canvas.canvas.draw(gp_source_file.SF)

def distance_to_line(begin, end, point):
    x1, y1 = begin.tuple()
    x2, y2 = end.tuple()
    x, y = point.tuple()
    #a, b, c are factors of ax+by+c=0 equation
    a = 1 / (x2 - x1 + 0.001)
    b = 1 / (y1 - y2 + 0.001)
    c = -x1*a -y1*b
    dist = (a*x + b*y + c) / (a**2 + b**2)**0.5
    return dist

def near_to_line(begin, end, point):
    eps = nearToLine
    d = distance_to_line(begin, end, point)
    x1, y1 = begin.tuple()
    x2, y2 = end.tuple()
    x, y = point.tuple()
    if x2<x1:
        x2, x1 = x1, x2
    if y2 < y1:
        y2, y1 = y1, y2
    if d < eps:
        if (x1-eps < x < x2+eps) and (y1-eps < y < y2+eps):
            return True
    return False

def findCycle(SF, block, root):
    for id in block.childs:
        child = SF.object_ids[id]
        if child is root:
            return True
        elif findCycle(SF, child, root):
            return True
    return False

def allChilds(SF, block):
    res = [block]
    for b in block.childs:
        child = SF.object_ids[b]
        res.append(child)

def cycle_checkout(SF, block):
    return findCycle(SF, block, block)

def find_block(click):
    debug_return(f'handling click: ({click.x},{click.y})')
    sfclick = gp_canvas.canvas.unscale(Point(click.x, click.y))
    for _, block in gp_source_file.SF.object_ids.items():
        debug_return('checking block: '+block.convertToStr())
        distance = (block.pos - sfclick).abs()
        if distance <= blockR:
            debug_return('check ok')
            return block

b1_state = ''
b2_state = ''
b3_state = ''

def b1(click):
    b1_state = 'n'
    debug_return (gp_canvas.canvas.viewpos)
    debug_return (f'left click: ({click.x},{click.y})')
    block = find_block(click)
    if block:
        block.chosen = True
        gp_canvas.canvas.handling = block
        gp_canvas.canvas.touch = Point(click.x, click.y)
    redraw()

def b2(click):
    b2_state = 'n'
    debug_return (f'wheel click: ({click.x},{click.y})')
    ...
    redraw()

def b3(click):
    b2_state = 'n'
    block = find_block(click)
    if block:
        block.chosen = True
        gp_canvas.canvas.handling = block
        gp_canvas.canvas.link_creation = Point(click.x, click.y)
        gp_canvas.canvas.touch = Point(click.x, click.y)
    redraw()
    debug_return (f'right click: ({click.x},{click.y})')


def b1_double(click):
    b1_state = 'd'
    debug_return (f'left double click: ({click.x},{click.y})')

    block = find_block(click)
    if block:
        if not block.text_editor:
            block.edit(tk.Toplevel(canvasFrame), gp_canvas.canvas)
    else:
        block = gp_source_file.Block(gp_source_file.SF)
        block.pos = gp_canvas.canvas.unscale(Point(click.x, click.y)).round()

    redraw()

def b2_double(click):
    b2_state = 'd'
    debug_return (f'wheel double click: ({click.x},{click.y})')
    ...
    redraw()

def b3_double(click):
    b3_state = 'd'
    debug_return (f'right double click: ({click.x},{click.y})')
    block = find_block(click)
    gp_canvas.canvas.handling = block

    for p in gp_source_file.SF.object_ids:
        parent = gp_source_file.SF.object_ids[p]
        for child in parent.childs:
            begin = parent.pos
            end = gp_source_file.SF.object_ids[child].pos
            point = Point(click.x, click.y)
            if near_to_line(begin, end, point):
                parent.delLink(child)

    if block:
        if tk.messagebox.askyesno("Delete?", "Do you want to delete block '" + block.data['<desc>'] + "'?", parent=canvasFrame):
            block.delete()
    redraw()


def b1_motion(click):
    b1_state = 'm'
    debug_return (f'left motion: ({click.x},{click.y})')
    clickpos = Point(click.x, click.y)
    if gp_canvas.canvas.handling:
        shift = clickpos - gp_canvas.canvas.touch
        #gp_canvas.canvas.handling.move(shift*(1/gp_canvas.canvas.viewzoom))
        gp_canvas.canvas.handling.pos = gp_canvas.canvas.unscale(clickpos).round()
        gp_canvas.canvas.touch = clickpos
    redraw()

def b2_motion(click):
    b2_state = 'm'
    debug_return (f'wheel motion:({click.x},{click.y})')
    ...
    redraw()

def b3_motion(click):
    b3_state = 'm'
    debug_return (f'right motion:({click.x},{click.y})')
    if gp_canvas.canvas.handling:
        gp_canvas.canvas.link_creation = Point(click.x, click.y)
    redraw()

def b1_release(click):
    b3_state = ''
    debug_return (f'left release:({click.x},{click.y})')

    gp_canvas.canvas.touch = None
    if gp_canvas.canvas.handling:
        gp_canvas.canvas.handling.chosen = False
    gp_canvas.canvas.handling = None
    redraw()

def b2_release(click):
    b2_state = ''
    debug_return (f'wheel release:({click.x},{click.y})')
    ...
    redraw()

def b3_release(click):
    b1_state = ''
    debug_return (f'right release:({click.x},{click.y})')
    block = find_block(click)
    if (block) and (not block == gp_canvas.canvas.handling) and (not block in gp_canvas.canvas.handling.childs):
        for obj in gp_source_file.SF.object_ids:
            if gp_source_file.SF.object_ids[obj] == block:
                id = obj
        gp_canvas.canvas.handling.childs.append(id)
        if cycle_checkout(gp_source_file.SF, block):
            gp_canvas.canvas.handling.delLink(id)
            debug_return ('ban cycle!!!')
    gp_canvas.canvas.touch = None
    gp_canvas.canvas.link_creation = False
    if gp_canvas.canvas.handling:
        gp_canvas.canvas.handling.chosen = False
    gp_canvas.canvas.handling = None
    redraw()


def wheel(click):
    debug_return (f'wheel:({click.x},{click.y}) {click.delta}')
    k = e ** (zoomSpeed*click.delta/120)
    scale = gp_canvas.canvas.scale
    unscale = gp_canvas.canvas.unscale

    clickpos = Point(click.x, click.y)
    SF_pos_old = unscale(clickpos)
    gp_canvas.canvas.viewzoom *= k
    SF_pos_new = unscale(clickpos)
    SF_shift = SF_pos_new - SF_pos_old
    gp_canvas.canvas.viewpos -= SF_shift

    redraw()
