import tkinter as tk
from random import uniform

from settings import *
from utils import *
import gp_source_file as source_file
import gp_canvas as canvas
from gp_block_manager import *


def scale(pos): return canvas.canvas.scale(pos)


def unscale(pos): return canvas.canvas.unscale(pos)


canvasFrame = ...


def assign_canvas_frame(canvasframe):
    """Передает в модуль поверхность/ transmit surface into the module"""
    global canvasFrame
    canvasFrame = canvasframe


def redraw():
    """Перерисовывает холст/ Redrawing canvas"""
    canvas.canvas.draw(source_file.SF)


def find_block(click, mode=1):
    return find_block_(click, canvas.canvas, source_file.SF, mode=mode)


"""Обработчики нажатия клавиш/ Mouse and keys handlers"""


def b1(click):
    """левая кнопка мыши/ left mouse button"""
    debug_return(f'canvas view pos: {canvas.canvas.viewpos}')
    debug_return(f'left click: ({click.x},{click.y})')
    # установка перемещаемого блока/set of moving block
    block = find_block(click)
    if block:
        block.chosen = True
        canvas.canvas.handling = block
        canvas.canvas.touch = Point(click.x, click.y)
    else:
        canvas.canvas.group_of_blocks = None
        #выделение
        p = unscale(Point(click.x, click.y))
        canvas.canvas.selection = (Area(p, p))
    redraw()



def b2(click):
    """колесо/ wheel"""
    debug_return(f'wheel click: ({click.x},{click.y})')
    clickpos = Point(click.x, click.y)
    block = find_block(clickpos)
    # удаление блока/block deletion
    if block:
        if canvas.canvas.group_of_blocks:
            if tk.messagebox.askyesno(
                    "Delete?",
                    "Do you want to delete a group of " +
                    str(len(canvas.canvas.group_of_blocks))+ " blocks?",
                    parent=canvasFrame):
                for block in canvas.canvas.group_of_blocks:
                    block.delete()
                canvas.canvas.group_of_blocks = None
        else:
            if tk.messagebox.askyesno(
                    "Delete?",
                    "Do you want to delete block '" + block.getSub() + "'?",
                    parent=canvasFrame):
                block.delete()
    # удаление линка/link deletion
    else:
        canvas.canvas.group_of_blocks = None
        stop = 0
        for p in source_file.SF.object_ids:
            parent = source_file.SF.object_ids[p]
            begin = parent.pos
            for child in parent.childs:
                end = source_file.SF.object_ids[child].pos
                point = unscale(Point(click.x, click.y))
                if near_to_line(begin, end, point):
                    parent.delLink(child)
                    stop = 1
                    break
            if stop:
                break
    redraw()


def b3(click):
    debug_return(f'right click: ({click.x},{click.y})')
    block = find_block(click)
    # установка начальной точки стрелки/setting of the initial arrow point
    if block:
        block.chosen = True
        canvas.canvas.handling = block
        canvas.canvas.link_creation = Point(click.x, click.y)
        canvas.canvas.touch = Point(click.x, click.y)
    else:
        canvas.canvas.group_of_blocks = None
        canvas.canvas.move_eye = unscale(Point(click.x, click.y))
    redraw()


def b1_double(click):
    """левый двойной щелок/ left doubleclick"""
    debug_return(f'left double click: ({click.x},{click.y})')
    block = find_block(click)
    clickpos = Point(click.x, click.y)
    # открытие редактора/opening redactor
    block_round = find_block(scale(unscale(clickpos).round()))
    if block:
        if not block.text_editor:
            block.edit(tk.Toplevel(canvasFrame), canvas.canvas)
    # создание блока/ creating block
    if not block:
        if not block_round:
            block = source_file.Block(source_file.SF)
            block.pos = unscale(clickpos).round()
            if openEditorAfterCreating:
                block.edit(tk.Toplevel(canvasFrame), canvas.canvas)

    redraw()


def b2_double(click):
    """двойной щелчок колесом/wheel doubleclick"""
    debug_return(f'wheel double click: ({click.x},{click.y})')
    ...
    redraw()


def b3_double(click):
    """правый двойной щелчок/ right doubleclick"""
    debug_return(f'right double click: ({click.x},{click.y})')

    redraw()


def b1_motion(click):
    """движение с зажатой левой клавишей/ movement with pressed left button"""
    debug_return(f'left motion: ({click.x},{click.y})')
    # сдвиг блоков/block(s) movement
    if canvas.canvas.handling:
        clickpos = Point(click.x, click.y)
        if ban_impositions:
            block = find_block(scale(unscale(clickpos).round()))
        else:
            block = 0

        if not block:
            newpos = unscale(clickpos).round()
            shift = newpos - canvas.canvas.handling.pos
            canvas.canvas.handling.shift(
                shift, desc=descend_moving, shift_id=uniform(0, 1))
            canvas.canvas.touch = clickpos
            if canvas.canvas.group_of_blocks:
                for block in canvas.canvas.group_of_blocks:
                    if block != canvas.canvas.handling:
                        block.shift(shift, desc=descend_moving, shift_id=uniform(0, 1))
    # выделение/selection
    elif canvas.canvas.selection:
        clickpos = unscale(Point(click.x, click.y))
        canvas.canvas.selection.p2 = clickpos
    redraw()


def b2_motion(click):
    """движение с зажатым колесом/ movement with pressed wheel"""
    debug_return(f'wheel motion:({click.x},{click.y})')
    ...
    redraw()


def b3_motion(click):
    """движение с зажатой правой клавишей/ movement with pressed right button"""
    debug_return(f'right motion:({click.x},{click.y})')
    # сдвиг конца стрелки/ arrow end movement
    if canvas.canvas.handling:
        canvas.canvas.link_creation = Point(click.x, click.y)
    elif canvas.canvas.move_eye:
        clickpos = unscale(Point(click.x, click.y))
        shift = clickpos - canvas.canvas.move_eye
        canvas.canvas.viewpos -= shift
    redraw()



def b1_release(click):
    """отпускание левой клавиши/ release of the left button"""
    debug_return(f'left release:({click.x},{click.y})')
    # сброс таскаемого блока
    canvas.canvas.touch = None
    if canvas.canvas.handling:
        canvas.canvas.handling.chosen = False
    canvas.canvas.handling = None

    # копия b3_ctrl_release
    global descend_moving
    descend_moving = 0

    # действие выделения
    if canvas.canvas.selection:
        area = canvas.canvas.selection
        canvas.canvas.selection = None
        for _, block in source_file.SF.object_ids.items():
            if block.pos in area:
                if canvas.canvas.group_of_blocks == None:
                    canvas.canvas.group_of_blocks = []
                canvas.canvas.group_of_blocks.append(block)
    redraw()



def b2_release(click):
    """отпускание колеса/ release of the wheel"""
    debug_return(f'wheel release:({click.x},{click.y})')
    ...
    redraw()


def b3_release(click):
    """отпускание правой клавиши/ release of the right button"""
    debug_return(f'right release:({click.x},{click.y})')
    # создание линка/Link creation
    block = find_block(click)
    if canvas.canvas.handling:
        if block and (not block == canvas.canvas.handling) and (block not in canvas.canvas.handling.childs):
            block_id = None
            for obj in source_file.SF.object_ids:
                if source_file.SF.object_ids[obj] == block:
                    block_id = obj
            if block_id is not None:
                canvas.canvas.handling.addLink(block_id)
                if cycle_checkout(source_file.SF, block):
                    canvas.canvas.handling.delLink(block_id)
                    debug_return('ban cycle!!!')
    canvas.canvas.touch = None
    canvas.canvas.link_creation = False
    canvas.canvas.move_eye = False
    if canvas.canvas.handling:
        canvas.canvas.handling.chosen = False
    canvas.canvas.handling = None
    redraw()



def wheel(click):
    click.d = 0
    if hasattr(click, 'num') and click.num != '??':
        if click.num == 4:
            click.d = 1
        elif click.num == 5:
            click.d = -1
        else:
            print(f'Invalid mouse wheel event attribute: {click}, click.num={click.num}')
            return
    elif hasattr(click, 'delta'):
        click.d = click.delta
        if click.d % 120 == 0:
            click.d /= 120  # for Windows
    else:
        print(f'Unknown mouse wheel event: {click}')
        return
    debug_return(f'wheel:({click.x},{click.y}) {click.d}')
    k = e ** (zoomSpeed * click.d)

    clickpos = Point(click.x, click.y)
    SF_pos_old = unscale(clickpos)
    canvas.canvas.viewzoom *= k
    SF_pos_new = unscale(clickpos)
    SF_shift = SF_pos_new - SF_pos_old
    canvas.canvas.viewpos -= SF_shift

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
