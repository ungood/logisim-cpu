#!/usr/bin/env python3

import io
import pprint
from string import hexdigits
from typing import List

from architecture import ARCHITECTURES, Architecture
from raw import RawWriter
from parsing import *

pretty_printer = pprint.PrettyPrinter(indent=4, width=1)

class AssemblyParser(ParserBase):
    def __init__(self, arch: Architecture):

        dec = Word(nums).set_parse_action(lambda t: int(t[0]))
        hex = Suppress('$') + Word(hexdigits).set_parse_action(lambda t: int(t[0], base=16))
        bin = Suppress('%') + Word("01").set_parse_action(lambda t: int(t[0], base=2))
        number = dec ^ hex ^ bin

        identifier = Word(alphas + "_")
        label = identifier('label') + Suppress(':')

        operation = make_operations(arch)('operation')
        operand = Group(number ^ identifier)('operand')
        instruction = (operation + Opt(operand))

        data = number('data')

        newline = Suppress(LineEnd())
        # Lines consist of an optional label, optionally followed by an instruction or some data.
        line = Opt(label) + Opt(instruction ^ data) + newline
        line.ignore(Word('#;', exact=1) + SkipTo(newline))

        parser = OneOrMore(Group(line))
        super().__init__(parser)


class Assembler(object):
    def __init__(self, arch: Architecture):
        self.arch = arch
        self.parser = AssemblyParser(self.arch)

    def assemble(self, input: io.TextIOBase, output: io.TextIOBase):
        results = self.parser.parse(input)
        name_table = {}
        statements = []

        # First pass, to build the name table.
        for line in results:
            if 'label' in line:
                label = line['label']
                address = len(statements)
                name_table[label] = address

            if 'operation' in line or 'data' in line:
                statements.append(line)
                logger.debug(f"Assinging to address {len(statements)}: {line.dump()}")

        logger.debug(f'Name table:\n{pretty_printer.pformat(name_table)}')
        logger.debug(f'Statements:\n{pretty_printer.pformat(statements)}')

        # Second pass, write statements, replacing references to labels.
        for address, statement in enumerate(statements):
            if 'data' in statement:
                output.write(f'{statement.data[0]}\n')
            else:
                output.write(f'{statement.operation.name}')
                if 'operand' in statement:
                    operand = statement.operand[0]
                    if isinstance(operand, str):
                        operand = name_table[operand]
                    output.write(f' {operand}')
                output.write('\n')


def main(arch: Architecture, input: io.TextIOBase, output: io.TextIOBase, **kwargs):
    Assembler(arch).assemble(input, output)

def write_diagram(arch: Architecture, output: io.TextIOBase, **kwargs):
    AssemblyParser(arch).write_diagram(output)

if __name__ == '__main__':
    Assembler(ARCHITECTURES[-1]).parser.run_tests("""
        # These should be valid
        empty_label:
        ; Just a comment
        NOP # Another kind of comment
        LDA 14
        25
        x: $0e
        y: %0110
    """)