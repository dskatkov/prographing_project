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
