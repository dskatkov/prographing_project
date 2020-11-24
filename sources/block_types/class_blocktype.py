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