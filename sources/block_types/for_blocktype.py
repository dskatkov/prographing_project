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