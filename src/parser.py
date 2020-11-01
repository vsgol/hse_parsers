from parsec import *

spaces = regex(r'\s*', re.MULTILINE)
space = regex(r'\s', re.MULTILINE)
ident = regex(r'(?!type\b|module\b)[_a-z]\w*')
variable_s = regex(r'(?!type\b|module\b)[A-Z]\w*')


@generate
def list_s():
    yield spaces + string('[') + spaces
    value = yield (atom ^ variable ^ list_my) | string('')
    if not value:
        yield spaces + string(']')
        return '[list] ()'

    yield spaces
    rasd = yield string('|') | string('')
    if rasd:
        tail = yield spaces >> variable
        yield spaces + string(']')
        return '[list] ({} | [Var] {})'.format(value, tail)

    yield spaces
    rasd = yield string(',') | string('')
    if not rasd:
        yield spaces + string(']')
        return '[list] ({})'.format(value)

    yield spaces
    tail = yield sepBy(atom ^ variable ^ list_my,
                       spaces + string(',') + spaces <
                       (atom ^ variable ^ list_my))
    yield spaces + string(']')
    value += ', '.join(tail)
    return '[list] ({})'.format(value)


@generate
def list_p():
    yield spaces + string('(')
    name = yield spaces >> (list_s ^ list_p) << spaces
    yield spaces + string(')')
    return name


list_my = list_p | list_s


@generate
def module():
    yield spaces + string('module') + space
    ex = yield spaces >> ident << spaces
    yield string('.')
    return 'module: {}'.format(ex)


@generate
def variable_p():
    yield spaces + string('(')
    name = yield spaces >> (variable_s | variable_p) << spaces
    yield spaces + string(')')
    return name


@generate
def variable():
    name = yield spaces >> (variable_s | variable_p)
    return '[Var] {}'.format(name)


@generate
def atom_s():
    name = yield spaces >> ident
    names = yield spaces >> sepBy(atom ^ variable ^ list_my, spaces)
    names.insert(0, name)
    res = ', '.join(names)
    if len(names) > 1:
        return '[Atom] ({})'.format(res)
    return '[Atom] {}'.format(res)


@generate
def atom_p():
    yield spaces + string('(')
    name = yield spaces >> (atom_s | atom_p)
    yield spaces + string(')')
    return name


atom = atom_s | atom_p


@generate
def term():
    ter = yield spaces >> sepBy1(expr_p,
                                 spaces + string(',') + spaces < expr_p)
    if len(ter) == 1:
        return ter[0]

    res = '[,] ({}) ({})'.format(ter[0], ter[1])
    for i in ter[2:]:
        res = '[,] (' + res + ') (' + i + ')'
    return res


@generate
def expr():
    ex = yield spaces >> sepBy1(term,
                                spaces + string(';') + spaces < term)
    if len(ex) == 1:
        return ex[0]

    res = '[;] ({}) ({})'.format(ex[0], ex[1])
    for i in ex[2:]:
        res = '[;] (' + res + ') (' + i + ')'
    return res


@generate
def expr_del():
    ex = yield spaces >> string('(') >> expr << spaces << string(')')
    return '{}'.format(ex)


expr_p = expr_del ^ atom


@generate
def definitionHuge():
    name = yield spaces >> atom
    ex = yield (spaces >> string(':-') >> spaces >> expr << spaces) | spaces + string('')
    yield string('.')
    if ex:
        return '[:-] ({}) ({})'.format(name, ex)
    return '[:-] ({})'.format(name)


@generate
def typeP_s():
    names = yield spaces >> sepBy1(atom ^ typeP_p ^ variable,
                                   spaces + string('->') + spaces < (atom ^ typeP_p ^ variable))
    res = ' '.join(names)
    if len(names) > 1:
        return '[Type] ({})'.format(res)
    return res


@generate
def typeP_p():
    yield spaces + string('(')
    name = yield spaces >> (typeP_s | typeP_p)
    yield spaces + string(')')
    return name


typeP = typeP_s ^ typeP_p ^ string('')


@generate
def definitionType():
    yield spaces + string('type') + space
    name = yield spaces >> ident
    type_ = yield spaces >> typeP << spaces
    yield string('.')
    return '[Typedef] {} ({})'.format(name, type_)


header = many(module)
definitionType_m = many(definitionType)
definitionHuge_m = many(definitionHuge)


@generate
def parser():
    head = yield header
    listT = yield definitionType_m
    listH = yield definitionHuge_m << spaces << eof()
    return '\n'.join(head) + ('\n\n' if head else '') \
           + '\n'.join(listT) + ('\n\n' if listT else '') \
           + '\n'.join(listH) + ('\n\n' if listT else '')


def build_atom(text):
    return atom_s.parse(text)


def build_definitionType(text):
    return definitionType.parse(text)


def build_type(text):
    return typeP_s.parse(text)


def build_module(text):
    return module.parse(text)


def build_definitionHuge(text):
    return definitionHuge.parse(text)


def build_list(text):
    return list_s.parse(text)


def build_tree(text):
    return parser.parse(text)
