import ply.lex as lex
import sys

tokens = [
    'LEFT',
    'RIGHT',
    'NAME',
    'EQ',
    'ALT',
    'CONCAT',
    'OPT',
    'LP',
    'RP',
    'LB',
    'RB',
    'COMMENT_B',
    'COMMENT_E',
    'COMMA',
    'DIGIT',
    'TAB'
]

comment_balance = 0
p_balance = 0
b_balance = 0


def t_LEFT(t):
    r'(?m)^[A-Za-z_][A-Za-z_0-9]*'
    global comment_balance
    if comment_balance == 0:
        return t


def t_RIGHT(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    global comment_balance
    if comment_balance == 0:
        return t


def t_COMMENT_B(t):
    r'\['
    global comment_balance
    comment_balance += 1


def t_COMMENT_E(t):
    r'\]'
    global comment_balance
    comment_balance -= 1
    if comment_balance < 0:
        raise Exception("Unexpected symbol ']' in line %d", t.lexer.lineno)
    if comment_balance == 0:
        return t


def t_NAME(t):
    r'(\".*\")'
    global comment_balance
    if comment_balance == 0:
        return t


def t_EQ(t):
    r'='
    global comment_balance
    if comment_balance == 0:
        return t


def t_ALT(t):
    r'\|'
    global comment_balance
    if comment_balance == 0:
        return t


def t_CONCAT(t):
    r'\+'
    global comment_balance
    if comment_balance == 0:
        return t


def t_OPT(t):
    r'\?'
    global comment_balance
    if comment_balance == 0:
        return t


def t_LP(t):
    r'\('
    global comment_balance
    global p_balance
    p_balance += 1
    if comment_balance == 0:
        return t


def t_RP(t):
    r'\)'
    global comment_balance
    global p_balance
    p_balance -= 1
    if p_balance < 0:
        raise Exception("Unexpected ')' in line %d \n", t.lexer.lineno)
    if comment_balance == 0:
        return t


def t_LB(t):
    r'\{'
    global comment_balance
    global b_balance
    b_balance += 1
    if comment_balance == 0:
        return t


def t_RB(t):
    r'\}'
    global comment_balance
    global b_balance
    b_balance -= 1
    if b_balance < 0:
        raise Exception("Unexpected '}' in line %d", t.lexer.lineno)
    if comment_balance == 0:
        return t


def t_COMMA(t):
    r'\,'
    global comment_balance
    if comment_balance == 0:
        return t


def t_DIGIT(t):
    r'[0-9]+'
    global comment_balance
    if comment_balance == 0:
        return t


def t_TAB(t):
    r'\n(\s\s\s\s)+'
    global comment_balance
    if comment_balance == 0:
        t.type = tokens[4]
        t.value = "|"
        return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    if t.value[0] != ' ':
        raise Exception("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
