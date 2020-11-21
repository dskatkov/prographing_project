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
    canvasFrame=canvasframe

'''
Work with mouse begins. It is not Finished yet
'''
def redraw():
    gp_canvas.canvas.draw(gp_source_file.SF)

def downtree(block, marks):
    for id in block.childs:
        if gp_source_file.SF.object_ids[id] in marks:
            return True
        elif downtree(gp_source_file.SF.object_ids[id], marks):
            return True
    return False


def cycle_checkout(SF, block):
    marks = [block]
    cycle = False
    return downtree(block, marks)

def find_block(click):
    debug_return(f'handling click: ({click.x},{click.y})')
    sfclick = gp_canvas.canvas.unscale((click.x, click.y))
    for _, block in gp_source_file.SF.object_ids.items():
        debug_return('checking block: '+block.convertToStr())
        distance2 = (block.pos[0] - sfclick[0]) ** 2 + (block.pos[1] - sfclick[1]) ** 2
        if distance2 <= 10 ** 2:
            debug_return('ok')
            return block

b1_state = ''
b2_state = ''
b3_state = ''

def b1(click):
    b1_state = 'n'
    debug_return (f'left click: ({click.x},{click.y})')
    block = find_block(click)
    if block:
        block.chosen = True
        gp_canvas.canvas.handling = block
        gp_canvas.canvas.touch = (click.x, click.y)
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
        gp_canvas.canvas.link_creation = click.x, click.y
        gp_canvas.canvas.touch = (click.x, click.y)
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
        block.pos = gp_canvas.canvas.unscale((click.x, click.y))

    redraw()

def b2_double(click):
    b2_state = 'd'
    debug_return (f'wheel double click: ({click.x},{click.y})')
    ...
    redraw()

def b3_double(click):
    b3_state = 'd'
    debug_return (f'right double click: ({click.x},{click.y})')
    #for gp_source_file.
    redraw()


def b1_motion(click):
    b1_state = 'm'
    debug_return (f'left motion: ({click.x},{click.y})')
    if gp_canvas.canvas.handling:
        shift = (click.x - gp_canvas.canvas.touch[0], click.y - gp_canvas.canvas.touch[1])
        gp_canvas.canvas.handling.move(shift)
        gp_canvas.canvas.touch = (click.x, click.y)
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
        gp_canvas.canvas.link_creation = click.x, click.y
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
            print('ban cycle!!!')
    gp_canvas.canvas.touch = None
    gp_canvas.canvas.link_creation = False
    if gp_canvas.canvas.handling:
        gp_canvas.canvas.handling.chosen = False
    gp_canvas.canvas.handling = None
    redraw()


def wheel(click):
    debug_return(f'wheel:({click.x},{click.y}) {click.delta}')
    k = 2.718281828459045 ** (0.1*click.delta/120)
    scale = gp_canvas.canvas.scale
    unscale = gp_canvas.canvas.unscale

    # Я не знаю, как и почему это работает, но оно работает (с какой-то погрешностью?!)
    pos = (click.x, click.y)
    pos = vecMul(pos, 1 / gp_canvas.canvas.viewzoom)
    sfpos = unscale(pos)
    gp_canvas.canvas.viewzoom *= k
    sfnewpos = unscale(pos)
    sfshift = vecSum(sfnewpos, vecMul(sfpos, -1))
    shift = vecMul(sfshift, -gp_canvas.canvas.viewzoom)
    gp_canvas.canvas.viewpos = vecSum(gp_canvas.canvas.viewpos, shift)

    redraw()

'''
Here work with mouse ended. spacetime is going back to normal
'''