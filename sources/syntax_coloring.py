class states:
    NONE           = 0
    SINGLE_QUOTE   = 1 # 'string'
    DOUBLE_QUOTE   = 2 # "string"
    ML_QUOTE       = 3 # `string`
    REGEX_LITERAL  = 4 # /regex/
    SL_COMMENT     = 5 # // single line comment
    ML_COMMENT     = 6 # /* multiline comment */
    NUMBER_LITERAL = 7 # 123
    KEYWORD        = 8 # function, var etc.
    SPECIAL        = 9 # null, true etc.


class colors:
    NONE           = '#000'
    SINGLE_QUOTE   = '#aaa' # 'string'
    DOUBLE_QUOTE   = '#aaa' # "string"
    ML_QUOTE       = '#aaa' # `string`
    REGEX_LITERAL  = '#707' # /regex/
    SL_COMMENT     = '#0a0' # // single line comment
    ML_COMMENT     = '#0a0' # /* multiline comment */
    NUMBER_LITERAL = '#a00' # 123
    KEYWORD        = '#00a' # function, var etc.
    SPECIAL        = '#055' # null, true etc.
    SYMBOLS        = '#07f' # +-/*=&|%!<>?:


keywords = ('async|await|break|case|class|const|continue|debugger|default|delete|do|else|enum|export|extends|for|from|function|' +
'get|if|implements|import|in|instanceof|interface|let|new|of|package|private|protected|public|return|set|static|super|' +
'switch|throw|try|typeof|var|void|while|with|yield|catch|finally').split('|')
specials = 'this|null|true|false|undefined|NaN|Infinity'.split('|')
digits = '0123456789abcdefABCDEF'
symbols = r'+-/*=&|%!<>?:.,@(){}[];%^~'
letters = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '_' + '0123456789'

def isAlphaNumericChar(char):
    return char in letters or char in digits

i = 0
def highlight(code):
    output = ''
    state = states.NONE
    global i
    for i in range(0, len(code)):
        char = code[i]
        prev = code[i-1]
        if i+1 < len(code):
            next = code[i+1]
        else:
            next = ' '

        if (state == states.NONE and char == '/' and next == '/'):
            state = states.SL_COMMENT
            output += startTag(code, i, colors.SL_COMMENT) + char
            continue
        
        if (state == states.SL_COMMENT and char == '\n'):
            state = states.NONE
            output += char + endTag(code, i)
            continue
        

        if (state == states.NONE and char == '/' and next == '*'):
            state = states.ML_COMMENT
            output += startTag(code, i, colors.ML_COMMENT) + char
            continue
        
        if (state == states.ML_COMMENT and char == '/' and prev == '*'):
            state = states.NONE
            output += char + endTag(code, i)
            continue
        

        closingCharNotEscaped = prev != '\\' or prev == '\\' and code[i-2] == '\\'
        if (state == states.NONE and char == '\''):
            state = states.SINGLE_QUOTE
            output += startTag(code, i, colors.SINGLE_QUOTE) + char
            continue
        
        if (state == states.SINGLE_QUOTE and char == '\'' and closingCharNotEscaped):
            state = states.NONE
            output += char + endTag(code, i+1)
            continue
        

        if (state == states.NONE and char == '"'):
            state = states.DOUBLE_QUOTE
            output += startTag(code, i, colors.DOUBLE_QUOTE) + char
            continue
        
        if (state == states.DOUBLE_QUOTE and char == '"' and closingCharNotEscaped):
            state = states.NONE
            output += char + endTag(code, i+1)
            continue
        

        if (state == states.NONE and char == '`'):
            state = states.ML_QUOTE
            output += startTag(code, i, colors.ML_QUOTE) + char
            continue
        
        if (state == states.ML_QUOTE and char == '`' and closingCharNotEscaped):
            state = states.NONE
            output += char + endTag(code, i+1)
            continue
        

        if (state == states.NONE and char == '/'):
            word = ''
            j = 0
            isRegex = True
            while (i + j >= 0):
                j-=1
                if (code[i+j] in symbols):
                    break
                if (not isAlphaNumericChar(code[i+j]) and len(word) > 0):
                    break
                if (isAlphaNumericChar(code[i+j])):
                    word = code[i+j] + word
                if (code[i+j] in ')]}'):
                    isRegex = False
                    break
                
            
            if (len(word) > 0 and not (word in keywords)):
                isRegex = False
            if (isRegex):
                state = states.REGEX_LITERAL
                output += startTag(code, i, colors.REGEX_LITERAL) + char
                continue
            
        
        if (state == states.REGEX_LITERAL and char == '/' and closingCharNotEscaped):
            state = states.NONE
            output += char + endTag(code, i)
            continue
        

        if (state == states.NONE and (char in digits) and not isAlphaNumericChar(prev)):
            state = states.NUMBER_LITERAL
            output += startTag(code, i, colors.NUMBER_LITERAL) + char
            continue
        
        if (state == states.NUMBER_LITERAL and not isAlphaNumericChar(char)):
            state = states.NONE
            output += endTag(code, i)
        

        if (state == states.NONE and not isAlphaNumericChar(prev)):
            word = ''
            j = 0
            while (code[i + j] and isAlphaNumericChar(code[i + j])):
                word += code[i + j]
                j+=1
            
            if (word in keywords):
                state = states.KEYWORD
                output += startTag(code, i, colors.KEYWORD)
            
            if (word in specials):
                state = states.SPECIAL
                output += startTag(code, i, colors.SPECIAL)
            
        
        if ((state == states.KEYWORD or state == states.SPECIAL) and not isAlphaNumericChar(char)):
            state = states.NONE
            output += endTag(code, i)
        

        if (state == states.NONE and (char in symbols)):
            output += startTag(code, i, colors.SYMBOLS) + char + endTag(code, i+1)
            continue
        

        output += char.replace('<', '&lt')
    
    return output #output.replace(/\n/gm, '<br>').replace(/\t/g, new Array(8).join('&nbsp'))
    #.replace(/^\s+|\s{2,}/g, (a) => new Array(a.length+1).join('&nbsp'))

code = r'''
(function () {

const states = {
    NONE           : 0,
    SINGLE_QUOTE   : 1, // 'string'
    DOUBLE_QUOTE   : 2, // "string"
    ML_QUOTE       : 3, // `string`
    REGEX_LITERAL  : 4, // /regex/
    SL_COMMENT     : 5, // // single line comment
    ML_COMMENT     : 6, // /* multiline comment */
    NUMBER_LITERAL : 7, // 123
    KEYWORD        : 8, // function, var etc.
    SPECIAL        : 9 // null, true etc.
};

const colors = {
    NONE           : '#000',
    SINGLE_QUOTE   : '#aaa', // 'string'
    DOUBLE_QUOTE   : '#aaa', // "string"
    ML_QUOTE       : '#aaa', // `string`
    REGEX_LITERAL  : '#707', // /regex/
    SL_COMMENT     : '#0a0', // // single line comment
    ML_COMMENT     : '#0a0', // /* multiline comment */
    NUMBER_LITERAL : '#a00', // 123
    KEYWORD        : '#00a', // function, var etc.
    SPECIAL        : '#055' // null, true etc.
};

const keywords = ('async|await|break|case|class|const|continue|debugger|default|delete|do|else|enum|export|extends|for|from|function|' +
'get|if|implements|import|in|instanceof|interface|let|new|of|package|private|protected|public|return|set|static|super|' +
'switch|throw|try|typeof|var|void|while|with|yield|catch|finally').split('|');
const specials = 'this|null|true|false|undefined|NaN|Infinity'.split('|');

function isAlphaNumericChar(char) {
    return char && /[0-9a-z_\$]/i.test(char);
}

function highlight(code) {
    let output = '';
    let state = states.NONE;
    for (let i = 0; i < code.length; i++) {
        let char = code[i], prev = code[i-1], next = code[i+1];

        if (state == states.NONE && char == '/' && next == '/') {
            state = states.SL_COMMENT;
            output += '<span style="color: ' + colors.SL_COMMENT + '">' + char;
            continue;
        }
        if (state == states.SL_COMMENT && char == '\n') {
            state = states.NONE;
            output += char + '</span>';
            continue;
        }

        if (state == states.NONE && char == '/' && next == '*') {
            state = states.ML_COMMENT;
            output += '<span style="color: ' + colors.ML_COMMENT + '">' + char;
            continue;
        }
        if (state == states.ML_COMMENT && char == '/' && prev == '*') {
            state = states.NONE;
            output += char + '</span>';
            continue;
        }

        const closingCharNotEscaped = prev != '\\' || prev == '\\' && code[i-2] == '\\';
        if (state == states.NONE && char == '\'') {
            state = states.SINGLE_QUOTE;
            output += '<span style="color: ' + colors.SINGLE_QUOTE + '">' + char;
            continue;
        }
        if (state == states.SINGLE_QUOTE && char == '\'' && closingCharNotEscaped) {
            state = states.NONE;
            output += char + '</span>';
            continue;
        }

        if (state == states.NONE && char == '"') {
            state = states.DOUBLE_QUOTE;
            output += '<span style="color: ' + colors.DOUBLE_QUOTE + '">' + char;
            continue;
        }
        if (state == states.DOUBLE_QUOTE && char == '"' && closingCharNotEscaped) {
            state = states.NONE;
            output += char + '</span>';
            continue;
        }

        if (state == states.NONE && char == '`') {
            state = states.ML_QUOTE;
            output += '<span style="color: ' + colors.ML_QUOTE + '">' + char;
            continue;
        }
        if (state == states.ML_QUOTE && char == '`' && closingCharNotEscaped) {
            state = states.NONE;
            output += char + '</span>';
            continue;
        }

        if (state == states.NONE && char == '/') {
            let word = '', j = 0, isRegex = true;
            while (i + j >= 0) {
                j--;
                if ('+/-*=|&<>%,({[?:;'.indexOf(code[i+j]) != -1) break;
                if (!isAlphaNumericChar(code[i+j]) && word.length > 0) break;
                if (isAlphaNumericChar(code[i+j])) word = code[i+j] + word;
                if (')]}'.indexOf(code[i+j]) != -1) {
                    isRegex = false;
                    break;
                }
            }
            if (word.length > 0 && !keywords.includes(word)) isRegex = false;
            if (isRegex) {
                state = states.REGEX_LITERAL;
                output += '<span style="color: ' + colors.REGEX_LITERAL + '">' + char;
                continue;
            }
        }
        if (state == states.REGEX_LITERAL && char == '/' && closingCharNotEscaped) {
            state = states.NONE;
            output += char + '</span>';
            continue;
        }

        if (state == states.NONE && /[0-9]/.test(char) && !isAlphaNumericChar(prev)) {
            state = states.NUMBER_LITERAL;
            output += '<span style="color: ' + colors.NUMBER_LITERAL + '">' + char;
            continue;
        }
        if (state == states.NUMBER_LITERAL && !isAlphaNumericChar(char)) {
            state = states.NONE;
            output += '</span>'
        }

        if (state == states.NONE && !isAlphaNumericChar(prev)) {
            let word = '', j = 0;
            while (code[i + j] && isAlphaNumericChar(code[i + j])) {
                word += code[i + j];
                j++;
            }
            if (keywords.includes(word)) {
                state = states.KEYWORD;
                output += '<span style="color: ' + colors.KEYWORD + '">';
            }
            if (specials.includes(word)) {
                state = states.SPECIAL;
                output += '<span style="color: ' + colors.SPECIAL + '">';
            }
        }
        if ((state == states.KEYWORD || state == states.SPECIAL) && !isAlphaNumericChar(char)) {
            state = states.NONE;
            output += '</span>';
        }

        if (state == states.NONE && '+-/*=&|%!<>?:'.indexOf(char) != -1) {
            output += '<span style="color: #07f">' + char + '</span>';
            continue;
        }

        output += char.replace('<', '&lt;');
    }
    return output.replace(/\n/gm, '<br>').replace(/\t/g, new Array(8).join('&nbsp;'))
    .replace(/^\s+|\s{2,}/g, (a) => new Array(a.length+1).join('&nbsp;'));
}

window.highlight = highlight;

})();

const formatted = document.getElementById('formatted');
document.getElementById('code').addEventListener('input', function () {
    formatted.innerHTML = highlight(this.value) //.replace(/<(?!\/?span)/gi, '&lt;');
});'''

# print(highlighted_code)
# print(f'\nCopy this text to "https://codebeautify.org/htmlviewer/" and click "Run"')

import tkinter as tk
from random import uniform
root = tk.Tk()

text = tk.Text(root)
text.insert('1.0', code)
text.pack(expand=1, fill='both')

tags = {}
current_id = 0
def startTag(code, i, color):
    global current_id
    #current_id = uniform(0, 1)
    tags[current_id] = {}
    tags[current_id][0] = pos(code, i)
    tags[current_id][1] = None
    tags[current_id][2] = color
    return f'<span style="color: {color}">'

def endTag(code, i):
    global current_id
    tags[current_id][1] = pos(code, i)
    current_id += 1
    return '</span>'

def applyTags():
    for tag_id, val in tags.items():
        text.tag_add(tag_id, val[0], val[1])
        text.tag_config(tag_id, background="#ffffff", foreground=val[2])

def pos(code, i):
    prefix = code[:i+1]
    lines = prefix.count('\n') + 1
    line = prefix.split('\n')[-1:][0]
    symbol = len(line)-1
    if line == '':
        lines -= 1
        line = prefix.split('\n')[-2:][0]
        symbol = len(line)
    #print(line)
    return f'{lines}.{symbol}'

# def spanBegin(color):
#     startTag(pos(code, i), color)
#     return f'<span style="color: {color}">'

# def spanEnd():
#     endTag(pos(code, i+1))
#     return '</span>'

highlighted_code = highlight(code)
#print(highlighted_code)
# for key, val in tags.items():
#     print(f'{key}: {val}')
#     pass
#tags = {0.5485641193019221: {0: '2.0', 2: '#a00', 1: '2.0'}, 0.03320118734389155: {0: '4.0', 2: '#a00', 1: '4.0'}, 0.21376615060703807: {0: '4.0', 2: '#07f', 1: '4.0'}, 0.35581874333918884: {0: '5.0', 2: '#07f', 1: '5.0'}, 0.7172854564534954: {0: '5.0', 2: '#a00', 1: '5.0'}, 0.35811572109976286: {0: '6.0', 2: '#07f', 1: '6.0'}, 0.0043848946680763445: {0: '6.0', 2: '#a00', 1: '6.0'}, 0.5544906435977103: {0: '6.0', 2: '#0a0', 1: '7.0'}, 0.3838113987576849: {0: '7.0', 2: '#a00', 1: '7.0'}, 0.06299645913344831: {0: '7.0', 2: '#07f', 1: '7.0'}, 0.35750763037567856: {0: '7.0', 2: '#a00', 1: '7.0'}, 0.459146378657625: {0: '7.0', 2: '#0a0', 1: '8.0'}, 0.4968312132900061: {0: '8.0', 2: '#07f', 1: '8.0'}, 0.1298755974875032: {0: '8.0', 2: '#a00', 1: '8.0'}, 0.2207261627416678: {0: '8.0', 2: '#0a0', 1: '9.0'}, 0.8450197159475159: {0: '9.0', 2: '#07f', 1: '9.0'}, 0.7425456486756302: {0: '9.0', 2: '#a00', 1: '9.0'}, 0.25649925266324825: {0: '9.0', 2: '#0a0', 1: '10.0'}, 0.23255529834869992: {0: '10.0', 2: '#07f', 1: '10.0'}, 0.5229080358316757: {0: '10.0', 2: '#a00', 1: '10.0'}, 0.7772063356260552: {0: '10.0', 2: '#0a0', 1: '11.0'}, 0.677713280239061: {0: '11.0', 2: '#07f', 1: '11.0'}, 0.9081128446860832: {0: '11.0', 2: '#a00', 1: '11.0'}, 0.9627211941965985: {0: '11.0', 2: '#0a0', 1: '12.0'}, 0.8632954906005789: {0: '12.0', 2: '#07f', 1: '12.0'}, 0.09893915895972394: {0: '12.0', 2: '#a00', 1: '12.0'}, 0.18165195587915273: {0: '12.0', 2: '#0a0', 1: '13.0'}, 0.5795976483684049: {0: '13.0', 2: '#07f', 1: '13.0'}, 0.6369941496814311: {0: '13.0', 2: '#a00', 1: '13.0'}, 0.3294986425667238: {0: '13.0', 2: '#0a0', 1: '14.0'}, 0.28677214465381373: {0: '14.0', 2: '#07f', 1: '14.0'}, 0.10420425658419463: {0: '14.0', 2: '#a00', 1: '14.0'}, 0.8227479187939138: {0: '14.0', 2: '#0a0', 1: '15.0'}, 0.30487919310820366: {0: '17.0', 2: '#a00', 1: '17.0'}, 0.6152729637175643: {0: '17.0', 2: '#a00', 1: '17.0'}, 0.4465429481377553: {0: '17.0', 2: '#07f', 1: '17.0'}, 0.0008783395361959823: {0: '18.0', 2: '#07f', 1: '18.0'}, 0.6003529811533995: {0: '18.0', 2: '#aaa', 1: '18.0'}, 0.6419643495480217: {0: '19.0', 2: '#07f', 1: '19.0'}, 0.5318532969116394: {0: '19.0', 2: '#aaa', 1: '19.0'}, 0.933583233593235: {0: '19.0', 2: '#0a0', 1: '20.0'}, 0.8424196392418403: {0: '20.0', 2: '#a00', 1: '20.0'}, 0.43038398490754715: {0: '20.0', 2: '#07f', 1: '20.0'}, }
# startTag('5.1', 'red')
# endTag('10.1')

# startTag('15.1', 'green')
# endTag('20.1')

applyTags()

root.mainloop()
