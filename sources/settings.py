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

blockTypes = ["Op", "If", "For"]

# Цвета соединяющих линий
# A_B = A-->B
# A_  = A-->*
#  _B = *-->B
#  _  = *-->*
linkColores = {
    "_": "#000000",

    "Op_":"#000000",
    "_Op":"#000000",
    "Op_Op": "#ffffff",
    "Op_If": "#ff0000",

    "If_":"#000000",
    "_If":"#000000",
    "If_If": "#0000ff",
    "If_Op": "#00ff00",
}
# Цвета кружков блоков разного типа
drawColores = {
    "_": "#ffffff",
    "Op": "#8080ff",
    "If": "#80ff80",
    "For": "Orange",
}

# Получение строки из объекта 
# "if (<1>) {".replace(key, eval(val))
keyWords = {
    "<1>": "self.text1", # текстовые блоки для подстановок
    "<2>": "self.text2",
    "<3>": "self.text3",
    "<4>": "self.text4",
    "<5>": "self.text5",
    "<desc>": "self.desc", # описание блока на канвасе

    #"<>": "self.",
}

languages = {
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

allSettings = {
    "Op": {
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
    },
    "If": {
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
    },
    "For": {
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
    },
}

settings = {}

def getSettingsByLang(lang):
    ... # достать все настройки только для этого языка

if __name__ == "__main__":
    print("This module is not for direct call!")
