#!/usr/bin/env python3

import instructions

def pad(array, desired_length, default_value):
    """Pads the input array to a given length with the supplied value."""
    return array + [default_value] * (desired_length - len(array))

def print_instruction(instruction):
    steps = pad(instruction.steps, 2**4, 0)
    hexed = [instructions.shex(step, 4) for step in steps]
    print(' '.join(hexed))

NOP = instructions.find_name('NOP')

print("v2.0 raw")
for opcode in range(16):
    try:
        instruction = instructions.find_opcode(opcode)
        print_instruction(instruction)
    except StopIteration:
        print_instruction(NOP)
    