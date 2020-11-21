

textEditorMenu_tree = {
    "OK": lambda: print('ok, not implemented'),
    "Отмена": lambda: print('cancel, not implemented'),
}

mainMenu_tree = {
    "Файл": {
        "Новый файл": lambda: print('new file, not implemented'),
        "Открыть...": lambda: print('open, not implemented'),
        "Сохранить": lambda: print('save, not implemented'),
        "Сохранить как...": lambda: print('save as, not implemented'),
    },
    "Сборка": {
        "Собрать исходник": lambda: print('build, not implemented'),
    },
    "Выход": lambda: print('exit, not implemented'),
    "Язык": {
        "py": lambda: print('py file, not implemented'),
        "c": lambda: print('c file, not implemented'),
        "pas": lambda: print('pas file, not implemented'),
    },
}


btnBG = '#202020'
btnFG = '#ffffff'

textBG = '#606060'
textFG = '#ffffff'

panelBG = '#404040'
panelFG = '#ffffff'

spaceBG = '#606060'
spaceFG = '#ffffff'

stateBG = '#404040'
stateFG = '#ffffff'

# Цвета соединяющих линий
# A_B = A-->B
# A_  = A-->*
#  _B = *-->B
#  _  = *-->*
linkColores = {
    "_": "#000000",

    "op_":"#000000",
    "_op":"#000000",
    "op_op": "#ffffff",
    "op_if": "#ff0000",

    "if_":"#000000",
    "_if":"#000000",
    "if_if": "#0000ff",
    "if_op": "#00ff00",
}

# Цвета кружков блоков разного типа
drawColores = {
    "_": "White",
    "op": "Blue",
    "if": "Green",
    "for": "Orange",
    "class": "Black",
    "function": "Pink",
}

# Получение строки из объекта 
# "if (<1>) {".replace(key, eval(val))
# keyWords = {
#     "<1>": "text1", # текстовые блоки для подстановок
#     "<2>": "text2",
#     "<3>": "text3",
#     "<4>": "text4",
#     "<5>": "text5",
#     "<desc>": "desc", # описание блока на канвасе

#     #"<>": "self.",
# }

languagePrePostfix = {
    "*": {
        "prefix": "",
        "postfix": "",
    },
    "c": {
        "prefix": "",
        "postfix": "",
    },
    "py": {
        "prefix": "",
        "postfix": "",
    },
    "pas": {
        "prefix": "BEGIN",
        "postfix": "END.",
    },
}


t_default = {"_": {
    "canvas": {
        "image": "undef.bmp",
        "tooltip": "UNDEF TYPE",
    },
    "edit": {
        "<desc>": {
            "header": "name",
            "type": "invisible"
        },
        "<class>": {
            "header": "TYPE",
            "type": "singleline",
        },
    },
    "build": {
        "*": {
            "incTab": 0,
            "hasPostfix": 0,
            "prefix": "",
            "postfix": "",
            "multiline": 0,
        },
    },
}}

t_op = {"op": {
    "canvas": {
        "image": "Op.bmp",
        "tooltip": "<1>",
    },
    "edit": {
        "<desc>": {
            "header": "name",
            "type": "singleline",
        },
        "<1>": {
            "header": "code",
            "type": "multiline",
        },
    },
    "build": {
        "*": {
            "incTab": 0,
            "hasPostfix": 0,
            "prefix": "<1>",
            "postfix": "",
            "multiline": 1,
        },
        "py": {
        },
    },
}}

t_if = {"if": {
    "canvas": {
        "image": "If.bmp",
        "tooltip": "if (<1>)",
    },
    "edit": {
        "<desc>": {
            "header": "name",
            "type": "singleline",
        },
        "<1>": {
            "header": "condition",
            "type": "singleline",
        },
    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPostfix": 1,
            "prefix": "if (<1>) {",
            "postfix": "}",
            "multiline": 0,
        },
        "py": {
            "hasPostfix": 0,
            "prefix": "if <1>:",
            "postfix": "",
        },
    },
}}



t_for =  {"for": {
    "canvas": {
        "image": "For.bmp",
        "tooltip": "for (<1>; <2>; <3>)",
    },
    "edit": {
        "<desc>": {
            "header": "name",
            "type": "singleline",
        },
        "<1>": {
            "header": "init",
            "type": "singleline",
        },
        "<2>": {
            "header": "condition",
            "type": "singleline",
        },
        "<3>": {
            "header": "iter",
            "type": "singleline",
        },
    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPostfix": 1,
            "prefix": "for (<1>; <2>; <3>) {",
            "postfix": "}",
            "multiline": 0,
        },
        "py": {
            "hasPostfix": 0,
            "prefix": "for <1> in <2>:",
            "postfix": "",
        },
    },
}}

t_class =  {"class": {
    "canvas": {
        "image": "class.bmp",
        "tooltip": "class <1>",
    },
    "edit": {
        "<desc>": {
            "header": "name",
            "type": "singleline",
        },
        "<1>": {
            "header": "class name",
            "type": "singleline",
        },
    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPostfix": 1,
            "prefix": "class <1> {",
            "postfix": "}",
            "multiline": 0,
        },
        "py": {
            "hasPostfix": 0,
            "prefix": "class <1>:",
            "postfix": "",
        },
    },
}}

t_function =  {"function": {
    "canvas": {
        "image": "function.bmp",
        "tooltip": "function <1>(<2>)",
    },
    "edit": {
        "<desc>": {
            "header": "name",
            "type": "singleline",
        },
        "<1>": {
            "header": "fn name",
            "type": "singleline",
        },
        "<2>": {
            "header": "fn params",
            "type": "singleline",
        },
    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPostfix": 1,
            "prefix": "function <1>(<2>) {",
            "postfix": "}",
            "multiline": 0,
        },
        "py": {
            "hasPostfix": 0,
            "prefix": "def <1>(<2>):",
            "postfix": "",
        },
    },
}}

blockR = 0.4
nearToLine = 0.1

t_all = ["_", "op", "if", "for", 'class', 'function']

debug_flag = True
profile = True

if __name__ == "__main__":
    print("This module is not for direct call!")
