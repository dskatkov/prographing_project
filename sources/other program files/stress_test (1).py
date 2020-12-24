import json
from random import randint

def block(id, childs, pos):
    return {
    	'type': 'op',
    	'id': id,
    	'childs': childs,
    	'pos': list(pos),
    	'data': {
    		'<desc>': '',
    		'<1>': '',
    	},
    }

n = 1000
k = 2 * round(n ** 0.5)

blocks = []

blocks.append(block(0, [1], (randint(0, k), randint(0, k))))

for i in range(1, n):
	blocks.append(block(i, [i+1], (randint(0, k), randint(0, k))))

blocks.append(block(n, [], (randint(0, k), randint(0, k))))

data = {
	'subversion': 0,
	'lang': 'python',
	'build_path': '',
	'blocks': blocks
}

# print(json.dumps(data, indent=4))

with open('big_file.vrc', 'w') as outfile:
    json.dump(data, outfile)

