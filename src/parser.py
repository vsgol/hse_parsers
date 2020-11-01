from src.lexer import tokens
import ply.yacc as yacc


class IncompleteToken(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(''.format(self.value))


def p_program(p):
    """
    program    : attitude program
               |
    """

    if len(p) > 1:
        p[0] = p[1] + '\n' + p[2]
    else:
        p[0] = ''


def p_listatom_ID(p):
    """
    listatom   : ID listatom
               | ID
    """

    if len(p) > 2:
        p[0] = ', Atom ' + p[1] + p[2]
    else:
        p[0] = ', Atom ' + p[1]


def p_listatom(p):
    """
    listatom   : atombr listatom
               | atombr
    """

    if len(p) > 2:
        p[0] = ', (' + p[1] + ')' + p[2]
    else:
        p[0] = ', (' + p[1] + ')'


def p_atombr(p):
    """
    atombr     : DELIMITERL atom DELIMITERR
               | DELIMITERL atombr DELIMITERR
    """

    if len(p) > 2:
        p[0] = p[2]


def p_atom(p):
    """
    atom       : ID listatom
               | ID
    """

    if len(p) > 2:
        p[0] = '[Atom] (ID ' + p[1] + p[2] + ')'
    else:
        p[0] = '[Atom] (ID ' + p[1] + ')'


def p_attitude(p):
    """
    attitude   : atom CORKSCREW expression DOT
               | atom DOT
    """

    if len(p) > 3:
        p[0] = '[' + p[2] + '] (' + p[1] + ') (' + p[3] + ') [.]'
    else:
        p[0] = p[1] + ' [.]'


def p_binary_operators(p):
    """
    term       : brace CONJUNCTION term
               | brace
    expression : term DISJUNCTION expression
               | term
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = '[' + p[2] + '] (' + p[1] + ') (' + p[3] + ')'


def p_brace(p):
    """
    brace      : atom
               | DELIMITERL expression DELIMITERR
    """

    if len(p) > 2:
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1]


def p_error(p):
    raise IncompleteToken(p)


parser = yacc.yacc()


def build_tree(code):
    return parser.parse(code)
