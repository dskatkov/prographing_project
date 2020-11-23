# Цвета различных элементов
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

    # "op_":"#000000",
    # "_op":"#000000",
    "op_op": "#ffffff",


    # "if_":"#000000",
    # "_if":"#000000",
    "if_if": "#ffffff",

    # "for_" :"",
    # "_for" :"",
    "for_for" :"#ffffff",

    # "function_" :"",
    # "_function" :"",
    "function_function" :"#ffffff",

    "class_" :"#0000ff",
    # "_class" :"",
    "class_class" :"#ffffff",

    # "op_if": "#ff0000",
    # "if_op": "#00ff00",
    "class_function" :"#8080ff",
    "class_op" :"#80ff80",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",

}

# Цвета кружков блоков разного типа
drawColores = {
    "_": "#404040",
    "op": "#FFFFFF",
    "if": "#F92472",
    "for": "#FD9622",
    "class": "#67D8EF",
    "function": "#A6E22B",
}


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


# Описания типов блоков
allTypes = {}

t_empty = {"*": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"<desc>",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
        },

    },
    "build": {
        "*": {
            "incTab": 0,
            "hasPrefix": 0,
            "prefix": "",
            "hasPostfix": 0,
            "postfix": "",
            "multiline": 0,
        },
    },
    'langs': ['*'],
}}
allTypes.update(t_empty)

t_undefined = {"?": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"Undefined type",
        },
    },
    "edit": {
        '*': {
            '<class>': {
                'header': 'type',
                'type': 'singleline',
            },
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
        },

    },
    "build": {
        "*": {
            "incTab": 0,
            "hasPrefix": 0,
            "prefix": "",
            "hasPostfix": 0,
            "postfix": "",
            "multiline": 0,
        },
    },
    'langs': ['*'],
}}
allTypes.update(t_undefined)

t_op = {"op": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"<desc>",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
            '<1>': {
                "header": '',
                'type': 'multiline',
            },
        },

    },
    "build": {
        "*": {
            "incTab": 0,
            "hasPrefix": 0,
            "prefix": "",
            "hasPostfix": 0,
            "postfix": "",
            "multiline": 1,
        },
    },
    'langs': ['*'],
}}
allTypes.update(t_op)

t_if = {"if": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"<desc>",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
            '<1>': {
                "header": 'condition',
                'type': 'singleline',
            },
        },

    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPrefix": 1,
            "prefix": "if (<1>) {",
            "hasPostfix": 1,
            "postfix": "}",
            "multiline": 0,
        },
        'py': {
            'prefix': 'if <1>:',
            'hasPostfix': 0,
        }
    },
    'langs': ['py'],
}}
allTypes.update(t_if)

t_for = {"for": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"<desc>",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
            '<1>': {
                "header": 'var',
                'type': 'singleline',
            },
            '<2>': {
                'header': 'range',
                'type': 'singleline'
            },
        },

    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPrefix": 1,
            "prefix": "for (<1>; <2>; <3>) {",
            "hasPostfix": 1,
            "postfix": "}",
            "multiline": 0,
        },
        'py': {
            'prefix': 'for <1> in <2>',
            'hasPostfix': 0,
        }
    },
    'langs': ['py'],
}}
allTypes.update(t_for)

t_fun = {"fun": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"<desc>",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
            '<1>': {
                "header": 'name',
                'type': 'singleline',
            },
            '<2>': {
                'header': 'params',
                'type': 'singleline'
            },
        },

    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPrefix": 1,
            "prefix": "function <1>(<2>) {",
            "hasPostfix": 1,
            "postfix": "}",
            "multiline": 0,
        },
        'py': {
            'prefix': 'def <1>(<2>):',
            'hasPostfix': 0,
        }
    },
    'langs': ['py'],
}}
allTypes.update(t_fun)

t_class = {"class": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"<desc>",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
            '<1>': {
                "header": 'name',
                'type': 'singleline',
            },
            '<2>': {
                'header': 'supers',
                'type': 'singleline'
            },
        },

    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPrefix": 1,
            "prefix": "class <1>(<2>) {",
            "hasPostfix": 1,
            "postfix": "}",
            "multiline": 0,
        },
        'py': {
            'prefix': 'class <1>(<2>):',
            'hasPostfix': 0,
        }
    },
    'langs': ['py'],
}}
allTypes.update(t_class)



# Радиус блока (1 - размер клетки)
blockR = 0.4
# Что-то связанное с проверкой принадлежности линии
nearToLine = 0.05
# Скорость зума колесом мыши
zoomSpeed = 0.1

# Флаг дебага
debug_flag = 1
# Флаг профилирования
profile = 0

openEditorAfterCreating = 1

descend_moving = 1

if __name__ == "__main__":
    print("This module is not for direct call!")
