t_elif = {"elif": {
    "canvas": {
        '*': {
            "image": "",
            "tooltip": "",
            "desc":"elif",
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
            "prefix": "else if (<1>) {",
            "hasPostfix": 1,
            "postfix": "}",
            "multiline": 0,
        },
        'py': {
            'prefix': 'elif <1>:',
            'hasPostfix': 0,
        }
    },
    'langs': ['py'],
}}
