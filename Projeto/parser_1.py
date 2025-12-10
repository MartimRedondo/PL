import ply.yacc as yacc
import ply.lex as lex
import sys
import re
from helper import *

# Definições do parser

prox_simb = ('Erro', '', 0, 0) # token, valor,localização

def p_Prog(p):
    """
    Prog : Frase
    """
    p[0] = 'pushn ' + str(parser.next_addr) + '\n'
    p[0] += 'start\n'
    p[0] += p[1]
    p[0] += 'stop\n'
    return p

class Frase():

    def p_Frase1(p):
        """
        Frase : Frase Exp 
        """
        if p[1] is not None and p[2] is not None:
            p[0] = p[1] + p[2]
        else:
            p[0] = ''
        return p

    def p_Frase2(p):
        """
        Frase :
        """
        p[0] = ''
        return p

class Exp():

    def p_Exp1(p):
        """
        Exp : Termo
        """
        p[0] = p[1]
        return p

    def p_Exp2(p):
        """
        Exp : Exp Termo SINAL 
        """
        if p[1] is not None and p[2] is not None and p[3] is not None:
            if p[3] == '+':
                p[0] = p[1] + p[2] + 'FADD\n'
            elif p[3] == '-':
                p[0] = p[1] + p[2] + 'FSUB\n'
            elif p[3] == '*':
                p[0] = p[1] + p[2] + 'FMUL\n'
            elif p[3] == '/':
                p[0] = p[1] + p[2] + 'FDIV\n'
            elif p[3] == '%':
                p[0] = p[1] + p[2] + 'MOD\n'
            elif p[3] == '^':  
                p[0] = ''
                pattern = r'[-+]?\d*\.\d+|\d+'
                matches = re.findall(pattern, p[2])
                if matches:
                    numero = float(matches[0])
                p[0] += p[1] + p[1] + 'FMUL\n'
                numero -= 2
                while numero > 0:
                    p[0] += p[1] + 'FMUL\n'
                    numero -= 1
        else:
            p[0] = ''
        return p

class Termo ():
    def __init__(self, type, exp):
        self.type = type
        self.exp = exp

    def p_Termo1(p):
        """
        Termo : NUM
        """
        p[0] = 'pushf ' + str(p[1]) + '\n'
        return p
        
    def p_Termo2(p):
        """
        Termo : '(' Exp ')'
        """  
        p[0] = p[2]
        return p  

    
def rec_term():
    global prox_simb
    if prox_simb.type == '(':
        rec_termo2('(')   
        rec_exp()
        print ("reconheci p8: term -> '('")
    if prox_simb == 'NUM':
        print("reconheci p7: term -> NUM")


def rec_termo2(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        #chamar erro
        p_error(simb)

def rec_sinal():
    global prox_simb
    if prox_simb.type == '+':
        

def rec_exp():
    global prox_simb
    if (prox_simb == 'NUM' | prox_simb == '('):
        rec_term()
    else:
        rec_exp()
        rec_term()
        rec_sinal()

def p_error(p):
    print("Erro Sintático: " + p)

def p_eof(p):
    if hasattr(p.lexer, 'eof_returned'):
        res = None
    else:
        p.lexer.lineno +=len(p.value)
        p.value = '$'
        p.type = '$'
        p.lexer.eof_returned = True
        res = p
    return p

parser = yacc.yacc()
parser.exito = True
parser.tab_id = {}
parser.next_addr = 0

fonte = ""
for linha in sys.stdin:
    fonte += linha

codigo = parser.parse(fonte)

if parser.exito:
    print("Parsing terminou com sucesso")
    print(codigo)
