import ply.yacc as yacc
import sys
from lexer import tokens

import graphviz


class Node:
    def parts_str(self):
        st = []
        for part in self.adj:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_adj(self, s):
        self.adj += s
        return self

    def __init__(self, type, s):
        self.type = type
        self.adj = s


def p_start(p):
    ''' program :
                | program rule '''
    if len(p) > 1:
        if p[1] is None:
            p[1] = Node('body', [])
        p[0] = p[1].add_adj([p[2]])
    else:
        p[0] = Node('body', [])


def p_rule(p):
    ''' rule : LEFT EQ LP right_part RP
             | COMMENT_E
             | LEFT EQ right_part'''
    if len(p) == 2:
        p[0] = Node('comment', [])
    if len(p) == 6:
        p[0] = Node('=', [p[1], p[4]])
    if len(p) == 4:
        p[0] = Node('=', [p[1], p[3]])


def p_right_part(p):
    ''' right_part :
                    | parenthesis
                    | concat_type
                    '''
    p[0] = p[1]


def p_concat_type(p):
    '''concat_type :
                   | alt_type
                   | concat_type CONCAT alt_type'''
    if len(p) == 4:
        p[0] = Node('+', [p[1], p[3]])
    else:
        p[0] = p[1]


def p_alt_type(p):
    '''alt_type :  unoper_type
                | alt_type ALT unoper_type'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('|', [p[1], p[3]])


def p_TERMINAL(p):
    '''TERMINAL : RIGHT
                | NAME'''
    p[0] = Node(p[1], [])


def p_parenthesis(p):
    '''parenthesis : LP right_part RP'''
    p[0] = p[2]


def p_unoper_type(p):
    '''unoper_type : parenthesis
                   | TERMINAL
                   | parenthesis unoper
                   | TERMINAL unoper '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('UO', [p[1], p[2]])


def p_unoper(p):
    '''unoper : OPT
             | LB DIGIT COMMA DIGIT RB
             | LB COMMA DIGIT RB
             | LB DIGIT COMMA RB
             | LB COMMA RB'''
    if (len(p) == 2):
        p[0] = p[1]
    if (len(p) == 4):
        p[0] = Node('{}', [p[2]])
    if (len(p) == 5):
        p[0] = Node('{}', [p[2], p[3]])
    if (len(p) == 6):
        p[0] = Node('{}', [p[2], p[3], p[4]])


parser = yacc.yacc()

# building a tree
number = 1


def add(lastname, lastnode, dadid="0"):
    global number
    for part in lastnode:
        if (not isinstance(part, str)):
            graph.node(str(number), part.type)
            number += 1
            graph.edge(dadid, str(number - 1))
            add(part.type, part.adj, str(number - 1))
        else:
            graph.node(str(number), part)
            number += 1
            graph.edge(dadid, str(number - 1))


def build_tree(code):
    return parser.parse(code)


graph = graphviz.Graph(format='png')
try:
    with open(sys.argv[1], 'r') as f:
        data = f.read()
    sys.stdout = open(sys.argv[1] + '.out', 'w')
except Exception as e:
    print(e)
    raise Exception("Can not open file")

try:
    tree = build_tree(data)
except Exception as e:
    print(e)
    raise Exception("Can not build tree")

try:
    graph.node("0", "program")
    lastname = "program"
    lastnode = tree.adj
    add(lastname, lastnode)

    graph.render("tree", view=True)
except Exception as e:
    print(e)
    raise Exception("Can not render graph")