import re
from ply.lex import lex
from ply.yacc import yacc
import math
import sys

tokens = ('NUM', 'ID', 'FUNC', 'LER', 'STRING')

literals = ['+', '-', '*', '/', '(', ')', '^', '=', ';']

fs = {'log' : math.log, 'exp' : math.exp, 'sin' : math.sin, 'cos' : math.cos, 'tan' : math.tan, 'inc' : lambda x: x + 1, 'dec' : lambda x: x - 1}


def t_NUM (t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_LER (t):
    r'ler\b'
    return t

def t_ID (t):
    r'[A-Za-z]\w*'
    if (t.value in fs):
        t.type = 'FUNC'
        t.value = fs[t.value]
    return t

def t_STRING (t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t\n'

def t_error(t):
    print("Caracter inválido: ", t.value[0])
    t.lexer.skip(1)


lexer = lex()

def lexer_debug (exemplo):

    lexer.input(exemplo)

    while token := lexer.token():
        print(token)

#lexer_debug(exemplo)

### GRAMÁTICA ### 
        
vars = {}

def p_z1 (t)           : 
    """z          : programa"""                    
    t[0] = f'{despejaVars(vars)}\nSTART\n{t[1]}\nSTOP'



def p_programa1 (t)     : 
    """programa    : programa instrucao ';'"""    
    t[0] = f'{t[1]}\n{t[2]}'
def p_programa2 (t)     : 
    """programa    : instrucao ';'"""            
    t[0] = t[1]




def p_instrucao1 (t)    : 
    """instrucao    : expression"""              
    t[0] = f'{t[1]}\n writef\n'
def p_instrucao2 (t)    : 
    """instrucao    : ID '=' expression"""      
    t[0] = f'{t[3]}\n storeg {getoffSet(t[1])}'



def p_expression1 (t) : 
    """expression : parcela"""                      
    t[0] = t[1]
def p_expression2(t):
    """expression : expression parcela '+' """
    t[0] = f'{t[1]} \n {t[2]} \n fadd'
def p_expression3(t):
    """expression : expression parcela '-' """
    t[0] = f'{t[1]} \n {t[2]} \n fsub'



def p_parcela1 (t)    :
    """parcela    : fator"""                        
    t[0] = t[1]
def p_parcela2 (t)    : 
    """parcela    : parcela fator '*' """            
    t[0] = f'pushf 0 \n {t[1]} \n {t[2]} \n fmul'
def p_parcela3 (t)    : 
    """parcela    : parcela fator '/' """            
    t[0] = f'pushf 0 \n {t[1]} \n {t[2]} \n fdiv'




def p_fator1 (t)      : 
    """fator      : termo"""                        
    t[0] = t[1]
#def p_fator2 (t)      : 
#    """fator      : termo '^' fator"""              
#    t[0] = t[1] ** t[3]




def p_termo1 (t)      :
    """termo      : NUM"""                          
    t[0] = f'pushf {t[1]}'
def p_termo2 (t)      :    
    """termo      : '(' expression ')'"""
    t[0] = t[2]
def p_termo3 (t)      : 
    """termo      : '-' termo"""                    
    t[0] = f'pushf 0 \n {t[2]} \n fsub'
def p_termo4 (t)      : 
    """termo      : '+' termo"""                   
    t[0] = f'pushf 0 \n {t[2]} \n fadd'
def p_termo5 (t)      : 
    """termo      : ID"""                           
    t[0] = f'pushg {getoffSet(t[1])}'
def p_termo6 (t)      : 
    """termo      : FUNC '(' expression ')'"""
    t[0] = t[1](t[3])
def p_termo7 (t)      : 
    """termo      : LER '(' STRING ')'"""           
    t[0] = f'pushs "{t[3]}" \n writes \n read \n atoi'


def p_error(t)        : print(f"Erro de sintaxe: {t.value}, {t}")

def despejaVars (vars):
    return 'pushf 0\n' * len (vars)

def getoffSet (id):
    if (id in vars):
        return vars[id]
    else:
        vars[id] = len(vars)
        return vars[id]

parser = yacc()

program = open(sys.argv[1]).read()

print(parser.parse(program))