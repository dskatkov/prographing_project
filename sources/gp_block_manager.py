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


# Описания типов блоков
allTypes = {}

from sources.block_types.empty_blocktype import *
allTypes.update(t_empty)
from sources.block_types.undefined_blocktype import *
allTypes.update(t_undefined)
from sources.block_types.op_blocktype import *
allTypes.update(t_op)
from sources.block_types.if_blocktype import *
allTypes.update(t_if)
from sources.block_types.elif_blocktype import *
allTypes.update(t_elif)
from sources.block_types.else_blocktype import *
allTypes.update(t_else)
from sources.block_types.for_blocktype import *
allTypes.update(t_for)
from sources.block_types.fun_blocktype import *
allTypes.update(t_fun)
from sources.block_types.class_blocktype import *
allTypes.update(t_class)
from sources.block_types.dict_blocktype import *
allTypes.update(t_dict)
from sources.block_types.dict_pair_blocktype import *
allTypes.update(t_dict_pair)
from sources.block_types.dict_long_pair_blocktype import *
allTypes.update(t_dict_long_pair)

