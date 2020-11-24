import json
import os

from utils import dictMerge

# Цвета соединяющих линий
# A_B = A-->B
# A_  = A-->*
#  _B = *-->B
#  _  = *-->*
linkColores = {
    "_": "#000000",

    "creating_": "#ffff00",

    # "op_":"#000000",
    # "_op":"#000000",
    "op_op": "#ffffff",


    # "if_":"#000000",
    # "_if":"#000000",
    "if_if": "#ffffff",

    # "for_" :"",
    # "_for" :"",
    "for_for" :"#ffffff",

    # "fun_" :"",
    # "_fun" :"",
    "fun_fun" :"#ffffff",

    "class_" :"#0000ff",
    # "_class" :"",
    "class_class" :"#ffffff",

    # "op_if": "#ff0000",
    # "if_op": "#00ff00",
    "class_fun" :"#8080ff",
    "class_op" :"#80ff80",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",
    # "_" :"",

}

# Цвета кружков блоков разного типа
drawColores = {
    'chosen': '#00ff00',
    "?": "#00ff00",
    '*': '#000000',
    "op": "#FFFFFF",
    "if": "#F92472",
    "else": "#C90452",
    "for": "#FD9622",
    "class": "#67D8EF",
    "fun": "#A6E22B",

    'dict': 'red',
    'dict_pair': 'yellow',
    'dict_long_pair': 'pink',
}


languagePrePostfix = {
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

type_list = [
    'undefined',
    'empty', 
    'op', 

    'if', 
    'else', 
    'elif',

    'for', 
    'class', 
    'fun', 

    'dict', 
    'dict_long_pair', 
    'dict_pair', 
]
# Описания типов блоков
def json_load():
    allTypes = {}
    for type in type_list:
        fp = open(f'block_types/{type}.json', 'rt')
        obj = json.load(fp)
        fp.close()
        allTypes = dictMerge(allTypes, obj)
    return allTypes

allTypes = json_load()

# print(json.dumps(allTypes, indent=4))

