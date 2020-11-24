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
