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