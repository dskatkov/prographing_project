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
# A_B = A->B
# A_  = A->*
#  _B = *->B
#  _  = *->*
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
}


# Поведение блоков при сборке
blockTypeBehavior = {
    "*":{

    },
    "Op":{
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

    "If":{
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

    "For":{
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

}

if __name__ == "__main__":
    print("This module is not for direct call!")
