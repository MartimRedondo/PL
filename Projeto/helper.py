import ply.lex as lex

tokens = ('NUM', 'SINAL', 'PRINT')

literals = [')', '(']


def t_NUM(t):
    r'\d+'
    t.value = float(t.value)
    return t

def t_SINAL(t):
    r'[\+\-\*\/\%\^]'
    return t

def t_PRINT(t):
    r'\.'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
t_ignore = " \t\n"

def t_error(t):
    print("Caráter inválido '%s'" % t.value[0])
    t.lexer.skip(1)

    


lexer = lex.lex()