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

drawColores = {
	"_": "#ffffff",
	"Op": "#8080ff",
	"If": "#80ff80",
}

{
	"Op":{
		"incTab": 0,
    	"hasPostfix": 0,
    	"prefix": "self.text",
    	"postfix": "",
	},
	"If":{
		"incTab": 1,
    	"hasPostfix": 1,
    	"prefix": "'if (' + self.text + ') {'",
    	"postfix": "'}'",
	},
}

if __name__ == "__main__":
    print("This module is not for direct call!")
