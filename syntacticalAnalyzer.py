import sys
import argparse
import threading
from src.parser import build_tree, build_atom, build_definitionHuge, build_type, \
    build_definitionType, build_list, build_module, ParseError


def add_arguments(args_str) -> argparse.Namespace:
    """Return the list of function arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', default=[sys.stdin],
                        type=argparse.FileType('r'),
                        help='files to parse (on default stdin)')
    parser.add_argument('-s', dest='silence', action='store_true',
                        help='don\'t create output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--atom', dest='atom', action='store_true',
                       help='parse only atom')
    group.add_argument('-t', '--type', dest='typedef', action='store_true',
                       help='parse only definition of type')
    group.add_argument('--typeexpr', dest='typeexpr', action='store_true',
                       help='parse only type')
    group.add_argument('-m', '--module', dest='module', action='store_true',
                       help='parse only module')
    group.add_argument('-r', '--relation', dest='relation', action='store_true',
                       help='parse only relation')
    group.add_argument('-l', '--list', dest='list', action='store_true',
                       help='parse only list')
    group.add_argument('-p', '--prog', dest='prog', action='store_true',
                       help='standard parser')

    return parser.parse_args(args_str)


def get_parser(args):
    if args.atom:
        return build_atom
    if args.typedef:
        return build_definitionType
    if args.typeexpr:
        return build_type
    if args.module:
        return build_module
    if args.relation:
        return build_definitionHuge
    if args.list:
        return build_list
    if args.prog:
        return build_tree
    return build_tree


def main(args_str):
    args = add_arguments(args_str)

    build = get_parser(args)

    for file in args.files:
        if len(args.files) > 1:
            print(file.name + ':', end=' ')
        try:
            result = build(file.read())
            print('Correct')
            if not args.silence:
                out = open(file.name + '.out', 'w')
                out.write(result)
                out.close()
        except ParseError as e:
            print(e)

    for file in args.files:
        file.close()


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    threading.stack_size(0x2000000)
    t = threading.Thread(target=main(sys.argv[1:]))
    t.start()
    t.join()
