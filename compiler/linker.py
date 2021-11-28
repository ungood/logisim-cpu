# The linker takes object code files (*.o) and produces machine code (*.raw)
# Our object code is a simple language consisting of two types of statements:
#   1. Instructions = Operation + Optional Operand
#   2. Number

import io

from architecture import ARCHITECTURES, Architecture
from parsing import *
from raw import RawWriter

from logzero import logger


class ObjectCodeParser(ParserBase):
    def __init__(self, arch: Architecture):
        number = Word(nums)
        number.set_parse_action(lambda token: int(token[0]))

        operation = make_operations(arch)
        statement = Opt(operation)('operation') + Opt(number('operand'), default=0) + Suppress(LineEnd())

        parser = OneOrMore(Group(statement))
        super().__init__(parser)


class Linker(object):
    def __init__(self, arch: Architecture):
        self.arch = arch
        self.parser = ObjectCodeParser(self.arch)

    def link(self, input: io.TextIOBase, output: io.TextIOBase):
        statements = self.parser.parse(input)
        if len(statements) > self.arch.max_addresses:
            raise RuntimeError('Linked program exceeds the memory capacity of the target architecture.')

        writer = RawWriter(output, width=2)
        for statement in statements:
            if 'operation' not in statement and 'operand' not in statement:
                continue # Skip blank lines
            opcode = 0 if 'operation' not in statement else statement.operation.opcode
            machine_code = (opcode << 4) | statement.operand
            logger.debug(f'Parsed opcode: {opcode} and operand: {statement.operand} for {statement}.')
            writer.write(machine_code)


def main(arch: Architecture, input: io.TextIOBase, output: io.TextIOBase, **kwargs):
    #logger.info(f"Assembling '{input.name}' to '{output.name}' for {arch.name}.")
    Linker(arch).link(input, output)

def write_diagram(arch: Architecture, output: io.TextIOBase, **kwargs):
    #logger.info(f"Writing object diagram for {arch.name} to '{output.name}'.")
    ObjectCodeParser(arch).write_diagram(output)

if __name__ == '__main__':
    Linker(ARCHITECTURES[-1]).parser.run_tests("""
        # These should be valid
        LDA 14
        NOP
        25

        # These are not:
        FOO 14
        BAR
        $5
        0x5e
    """)
