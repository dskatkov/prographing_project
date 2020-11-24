import tkinter as tk
import tkinter.font
import time
from random import uniform

from gp_mouse_binding import *
from settings import *
from utils import *
import gp_source_file as gp_source_file
import gp_canvas as gp_canvas

scale = lambda pos: gp_canvas.canvas.scale(pos)
unscale = lambda pos: gp_canvas.canvas.unscale(pos)

def assign_canvasFrame(canvasframe):
    """Передает в модуль поверхность/ transmit surface into the module"""
    global canvasFrame
    canvasFrame = canvasframe

def redraw():
    """Перерисовывает холст/ Redrawing canvas"""
    gp_canvas.canvas.draw(gp_source_file.SF)

def find_block(click):
    return find_block_(click, gp_canvas.canvas, gp_source_file.SF)

"""Обработчики нажатия клавиш/ Mouse and keys handlers"""

b1_state = ''
b2_state = ''
b3_state = ''

def b1(click):
    """левая кнопка мыши/ left mouse button"""
    b1_state = 'n'
    debug_return (f'canvas view pos: {gp_canvas.canvas.viewpos}')
    debug_return (f'left click: ({click.x},{click.y})')
    block = find_block(click)
    # установка начальной точки стрелки/setting of the initial arrow point
    if block:
        block.chosen = True
        gp_canvas.canvas.handling = block
        gp_canvas.canvas.link_creation = Point(click.x, click.y)
        gp_canvas.canvas.touch = Point(click.x, click.y)
    redraw()

def b2(click):
    '''колесо/ wheel'''
    b2_state = 'n'
    debug_return (f'wheel click: ({click.x},{click.y})')
    clickpos = Point(click.x, click.y)
    block = find_block(clickpos)
    #gp_canvas.canvas.handling = block
    # удаление блока/block deletion
    if block:
        if tk.messagebox.askyesno("Delete?", "Do you want to delete block '" + block.getSub() + "'?", parent=canvasFrame):
            block.delete()
    # удаление линка/link deletion
    if not block:
        stop = 0
        for p in gp_source_file.SF.object_ids:
            parent = gp_source_file.SF.object_ids[p]
            begin = parent.pos
            for child in parent.childs:
                end = gp_source_file.SF.object_ids[child].pos
                point = unscale(Point(click.x, click.y))
                if near_to_line(begin, end, point):
                    parent.delLink(child)
                    stop = 1
                    break
            if stop:
                break
    redraw()

def b3(click):
    b2_state = 'n'
    debug_return (f'right click: ({click.x},{click.y})')
    block = find_block(click)
    # установка перемещаемого блока/set of moving block
    if block:
        block.chosen = True
        gp_canvas.canvas.handling = block
        gp_canvas.canvas.touch = Point(click.x, click.y)
    redraw()


def b1_double(click):
    """левый двойной щелок/ left doubleclick"""
    b1_state = 'd'
    debug_return (f'left double click: ({click.x},{click.y})')
    block = find_block(click)
    clickpos = Point(click.x, click.y)
    # открытие редактора/opening redactor
    block_round = find_block(scale(unscale(clickpos).round()))
    if block:
        if not block.text_editor:
            block.edit(tk.Toplevel(canvasFrame), gp_canvas.canvas)
    # создание блока/ creating block
    if not block:
        if not block_round:
            block = gp_source_file.Block(gp_source_file.SF)
            block.pos = unscale(clickpos).round()
            if openEditorAfterCreating:
                block.edit(tk.Toplevel(canvasFrame), gp_canvas.canvas)

    redraw()

def b2_double(click):
    """двойной щелчок колесом/wheel doubleclick"""
    b2_state = 'd'
    debug_return (f'wheel double click: ({click.x},{click.y})')
    ...
    redraw()

def b3_double(click):
    """правый двойной щелчок/ right doubleclick"""
    b3_state = 'd'
    debug_return (f'right double click: ({click.x},{click.y})')

    redraw()


def b1_motion(click):
    """движение с зажатой левой клавишей/ movement with pressed left button"""
    b1_state = 'm'
    debug_return (f'left motion: ({click.x},{click.y})')
    # сдвиг конца стрелки/ arrow end movement
    if gp_canvas.canvas.handling:
        gp_canvas.canvas.link_creation = Point(click.x, click.y)
    redraw()

def b2_motion(click):
    """движение с зажатым колесом/ movement with pressed wheel"""
    b2_state = 'm'
    debug_return (f'wheel motion:({click.x},{click.y})')
    ...
    redraw()

def b3_motion(click):
    """движение с зажатой правой клавишей/ movement with pressed right button"""
    b3_state = 'm'
    debug_return (f'right motion:({click.x},{click.y})')
    clickpos = Point(click.x, click.y)
    # сдвиг блоков/block movement
    if gp_canvas.canvas.handling:
        newpos = unscale(clickpos).round()
        shift = newpos - gp_canvas.canvas.handling.pos
        gp_canvas.canvas.handling.shift(shift, desc=descend_moving, shift_id=uniform(0,1))
        gp_canvas.canvas.touch = clickpos
    redraw()

def b1_release(click):
    """отпускание левой клавиши/ release of the left button"""
    b3_state = ''
    debug_return (f'left release:({click.x},{click.y})')
    block = find_block(click)
    # создание линка/Link creation
    if gp_canvas.canvas.handling:
        if (block) and (not block == gp_canvas.canvas.handling) and (not block in gp_canvas.canvas.handling.childs):
            for obj in gp_source_file.SF.object_ids:
                if gp_source_file.SF.object_ids[obj] == block:
                    id = obj
            gp_canvas.canvas.handling.addLink(id)
            if cycle_checkout(gp_source_file.SF, block):
                gp_canvas.canvas.handling.delLink(id)
                debug_return ('ban cycle!!!')
    gp_canvas.canvas.touch = None
    gp_canvas.canvas.link_creation = False
    if gp_canvas.canvas.handling:
        gp_canvas.canvas.handling.chosen = False
    gp_canvas.canvas.handling = None
    redraw()

def b2_release(click):
    """отпускание колеса/ release of the wheel"""
    b2_state = ''
    debug_return (f'wheel release:({click.x},{click.y})')
    ...
    redraw()

def b3_release(click):
    """отпускание правой клавиши/ release of the right button"""
    b1_state = ''
    debug_return (f'right release:({click.x},{click.y})')
    # сброс таскаемого блока
    gp_canvas.canvas.touch = None
    if gp_canvas.canvas.handling:
        gp_canvas.canvas.handling.chosen = False
    gp_canvas.canvas.handling = None
    redraw()


def wheel(click):
    debug_return (f'wheel:({click.x},{click.y}) {click.delta}')
    k = e ** (zoomSpeed*click.delta/120)

    clickpos = Point(click.x, click.y)
    SF_pos_old = unscale(clickpos)
    gp_canvas.canvas.viewzoom *= k
    SF_pos_new = unscale(clickpos)
    SF_shift = SF_pos_new - SF_pos_old
    gp_canvas.canvas.viewpos -= SF_shift

    redraw()

def b3_ctrl(click):
    debug_return('left click + ctrl')
    global descend_moving
    descend_moving = 1
    b3(click)

def b3_ctrl_release(click):
    debug_return('left click + ctrl release')
    global descend_moving
    descend_moving = 0
    b3_release(click)



if __name__ == "__main__":
    print("This module is not for direct call!")
