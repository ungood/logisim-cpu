import argparse
import sys

from architecture import ARCHITECTURES
import assembler
import linker
import microcode

import logzero

class DictAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.choices.get(values, self.default))

parser = argparse.ArgumentParser('sappy', description='Compiler for the SAP series of CPUs.')
parser.add_argument('--debug', '-d', action='store_true')

subparsers = parser.add_subparsers()
parent_parser = argparse.ArgumentParser(add_help=False)

arch_map = {a.name: a for a in ARCHITECTURES}

parent_parser.add_argument('--arch',
    action=DictAction,
    choices=arch_map,
    default=ARCHITECTURES[-1],
    help='Which architecture to run the command against.')

def create_command(name, func, input_option=True, output_option=True):
    command = subparsers.add_parser(name, parents=[parent_parser])
    command.set_defaults(func=func)

    if input_option:
        command.add_argument('input',
            nargs='?',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help='The file to read. If empty, stdin is used.')

    if output_option:
        command.add_argument('output',
            nargs='?',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help='The file to write. If empty, stdout is used.')

create_command('write-microcode', microcode.main, input_option=False)

create_command('write-object-code-diagram', linker.write_diagram, input_option=False)
create_command('link', linker.main)

create_command('write-assembly-diagram', assembler.write_diagram, input_option=False)
create_command('assemble', assembler.main)

def main():    
    args = parser.parse_args()

    loglevel = logzero.DEBUG if args.debug else logzero.INFO
    logzero.loglevel(loglevel)

    try:
        args.func(**vars(args))
    finally:
        if 'input' in args and args.input != sys.stdin:
            args.input.close()
        if 'output' in args and args.output != sys.stdout:
            args.output.close()

if __name__ == '__main__':
    main()