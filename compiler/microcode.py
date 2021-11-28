#!/usr/bin/env python3

from io import TextIOBase
from logzero import logger

from architecture import Architecture, ARCHITECTURES
from raw import RawWriter

def pad(array, desired_length, default_value):
    """Pads the input array to a given length with the supplied value."""
    return array + [default_value] * (desired_length - len(array))

class MicrocodeWriter(object):
    def __init__(self, arch: Architecture, output: TextIOBase):
        self.arch = arch
        self.writer = RawWriter(output, width=4)
    
    def write(self):
        for opcode in range(self.arch.max_operations):
            self.write_opcode(opcode)

    def write_opcode(self, opcode):
        try:
            operation = self.arch.opcodes[opcode]
            logger.debug(f'{opcode:0x} -> {operation}')
            self.write_operation(operation)
        except KeyError:
            logger.debug(f'{opcode:0x} -> No Operation')
            self.write_operation(self.arch.nop)

    def write_operation(self, operation):
        steps = pad(operation.steps, 2**4, 0)
        self.writer.write(*steps)
        

def main(arch: Architecture, output: TextIOBase, **kwargs):
    MicrocodeWriter(arch, output).write()

if __name__ == '__main__':
    import sys
    main(ARCHITECTURES[-1], sys.stdout)
