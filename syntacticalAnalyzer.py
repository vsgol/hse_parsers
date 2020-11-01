import sys
import argparse
from src.parser import build_tree, IncompleteToken
from src.lexer import IllegalCharacter


def add_arguments(args_str) -> argparse.Namespace:
    """Return the list of function arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', default=[sys.stdin],
                        type=argparse.FileType('r'),
                        help='files to parse (on default stdin)')
    parser.add_argument('-s', dest='silence', action='store_true',
                        help='don\'t create output file')

    return parser.parse_args(args_str)


def main(args_str):
    args = add_arguments(args_str)

    for file in args.files:
        if len(args.files) > 1:
            print(file.name + ':', end=' ')
        try:
            result = build_tree(file.read())
            print('Correct')
            if not args.silence:
                out = open(file.name + '.out', 'w')
                out.write(result)
                out.close()
        except IllegalCharacter as e:
            print('IllegalCharacter: \'{}\', line {}'.format(e.value, e.line))
        except IncompleteToken as e:
            print('IncompleteToken:', e.value)

    for file in args.files:
        file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
