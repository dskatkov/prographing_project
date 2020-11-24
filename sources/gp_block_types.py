# Цвета соединяющих линий
# A_B = A-->B
# A_  = A-->*
#  _B = *-->B
#  _  = *-->*
linkColores = {
    "_": "#000000",

	"creating_": "#ffff00",

    # "op_":"#000000",
    # "_op":"#000000",
    "op_op": "#ffffff",


    # "if_":"#000000",
    # "_if":"#000000",
    "if_if": "#ffffff",

    # "for_" :"",
    # "_for" :"",
    "for_for" :"#ffffff",

    # "fun_" :"",
    # "_fun" :"",
    "fun_fun" :"#ffffff",

    "class_" :"#0000ff",
    # "_class" :"",
    "class_class" :"#ffffff",

    # "op_if": "#ff0000",
    # "if_op": "#00ff00",
    "class_fun" :"#8080ff",
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
	'chosen': '#00ff00',
    "?": "#00ff00",
    '*': '#000000',
    "op": "#FFFFFF",
    "if": "#F92472",
    "else": "#C90452",
    "for": "#FD9622",
    "class": "#67D8EF",
    "fun": "#A6E22B",

    'dict': 'red',
    'dict_pair': 'yellow',
    'dict_long_pair': 'pink',
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
            "desc":"",
        },
    },
    "edit": {
        '*': {
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
            "hasPrefix": 1,
            "prefix": "<1>",
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
            "desc":"if",
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

t_else = {"else": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"else",
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
            "incTab": 1,
            "hasPrefix": 1,
            "prefix": "else {",
            "hasPostfix": 1,
            "postfix": "}",
            "multiline": 0,
        },
        'py': {
            'prefix': 'else:',
            'hasPostfix': 0,
        }
    },
    'langs': ['py'],
}}
allTypes.update(t_else)



t_for = {"for": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"for",
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
            "desc":"def <1>",
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
            'hasPostfix': 1,
            'postfix': ''
        }
    },
    'langs': ['py'],
}}
allTypes.update(t_fun)

t_class = {"class": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "class <1>(<2>):",
            "desc":"class <1>",
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

t_dict = {"dict": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "dict",
            "desc":"dict",
        },
    },
    "edit": {
        '*': {
        },
    },
    "build": {
        "*": {
            "incTab": 1,
            "hasPrefix": 1,
            "prefix": "{",
            "hasPostfix": 1,
            "postfix": "}",
            "multiline": 0,
        },
    },
    'langs': ['py'],
}}
allTypes.update(t_dict)

t_dict_pair = {"dict_pair": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "dict_pair",
            "desc":"dict_pair",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
            '<1>': {
                "header": 'key',
                'type': 'singleline',
            },
            '<2>': {
                "header": 'val',
                'type': 'singleline',
            },
        },
    },
    "build": {
        "*": {
            "incTab": 0,
            "hasPrefix": 1,
            "prefix": "<1>: <2>,",
            "hasPostfix": 0,
            "postfix": "",
            "multiline": 0,
        },
    },
    'langs': ['py'],
}}
allTypes.update(t_dict_pair)

t_dict_long_pair = {"dict_long_pair": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "dict_long_pair",
            "desc":"dict_long_pair",
        },
    },
    "edit": {
        '*': {
            "<desc>": {
                "header": "",
                "type": "invisible",
            },
            '<1>': {
                "header": 'key',
                'type': 'singleline',
            },
        },
    },
    "build": {
        "*": {
            "incTab": 0,
            "hasPrefix": 1,
            "prefix": "<1>: ",
            "hasPostfix": 1,
            "postfix": ",",
            "multiline": 0,
        },
    },
    'langs': ['py'],
}}
allTypes.update(t_dict_long_pair)

