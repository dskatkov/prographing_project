import tkinter as tk
from settings import *

# class Point:
#     def __init__(self, x=0, y=0):
#         self.x = x
#         self.y = y

#     def __repr__(self):
#         return f'Point({self.x}, {self.y})'

#     def __str__(self):
#         return f'({self.x},{self.y})'

#     def fromStr(self, str):
#         self.x, self.y = eval(str)

#     def fromTuple(self, tpl):
#         self.x, self.y = tpl

def vecSum(a, b):
	return a[0] + b[0], a[1] + b[1]

def vecMul(a, k):
	return a[0] * k, a[1] * k

def createMenu(master, tree):
    for key, val in tree.items():
        m = tk.Menu(master=master, tearoff=0)
        if type(val)==type({}):
            createMenu(m, val)
        else:
            master.add_command(label=key, command=val)
            continue
        master.add_cascade(label=key, menu=m)

def placeButtons(master, buttons, side='left', fg=btnFG, bg=btnBG):
    for btn in buttons:
        b = tk.Button(master=master, text=btn[0], command=btn[1], fg=btnFG, bg=btnBG)
        b.pack(side=side, padx=3, pady=3)

def getSettingsByLang(lang):
    res = {}
    for type in t_all:
        res = dictMerge(
            res, 
            createDictByPath(
                f'{type}.build',
                dictMerge(
                    getDictValByPath(allTypes, f'{type}.build.{lang}')
                    , getDictValByPath(allTypes, f'{type}.build.*')
                )
            )
        )
        for key, val in allTypes[type].items():
            if not (key in ['build']):
                res = dictMerge(res, {type:{key:val}})
    return res

takeFirst = lambda x, y: x
takeSecond = lambda x, y: y

def normalMerge(a, b, f=takeFirst):
    if type(a) != dict or type(b) != dict:
        return f(a, b)
    return dictMerge(a, b)

def dictMerge(*dicts, f=lambda x,y: normalMerge(x,y,f=takeFirst)):
    res = {}

    if len(dicts) == 2:
        a, b = dicts

        for key, val in a.items():
            if not key in b:
                res[key] = val

        for key, val in b.items():
            if not key in a:
                res[key] = val

        for key, val in a.items():
            if key in b:
                res[key] = f(val, b[key])
    else:
        for d in dicts:
            res = dictMerge(res, d, f=f)

    return res



def getDictValByPath(d, path):
    val = d
    spl = path.split('.')
    for key in spl:
        if key in val:
            val = val[key]
        else:
            val = {}
            break
    return val

def createDictByPath(path, val):
    spl = path.split('.')
    spl.reverse()

    d = {spl[0]: val}

    for key in spl[1:]:
        d = {key: d}
    return d

def setDictValByPath(d, path, val):
    return dictMerge(d, createDictByPath(path, val), f=takeSecond)

allTypes = dictMerge(t_default, t_op, t_if, t_for)



# def dictMergeSmall(a, b):
#     res = {}
#     for key, val in list(a.items())+list(b.items()):
#         res[key] = val
#     return res
# print(dictMergeSmall({1:2,3:4},{5:6,1:7}))




if __name__ == '__main__':
    print('This module is not for direct call!')
