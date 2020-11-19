textEditorMenu_tree = {
    "OK": 1,
    "Отмена": 0,
}

mainMenu_tree = {
    "Файл": {
        "Новый файл": 0,
        "Открыть...": 0,
        "Сохранить": ...,
        "Сохранить как...": 0,
    },
    "Сборка": {
        "Собрать исходник": 0,
    },
    "Выход": 0,
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
blockTypes = {
    "Op":{
        "*": {
            "incTab": 0,
            "hasPostfix": 0,
            "prefix": "self.text1",
            "postfix": "",
        },
        "py": {
        },
    },
    "If":{
        "*": {
            "incTab": 1,
            "hasPostfix": 1,
            "prefix": "'if (' + self.text1 + ') {'",
            "postfix": "'}'",
        },
        "py": {
            "hasPostfix": 0,
            "prefix": "'if ' + self.text1 + ':'",
            "postfix": "",
        },
    },
    "For":{
        "*": {
            "incTab": 1,
            "hasPostfix": 1,
            "prefix": "'for ('+self.text1+'; '+self.text2+'; '+self.text3+') {'",
            "postfix": "'}'",
        },
        "py": {
            "hasPostfix": 0,
            "prefix": "'for '+self.text1+' in '+self.text2+':'",
            "postfix": "",
        },
    },

}

if __name__ == "__main__":
    print("This module is not for direct call!")
