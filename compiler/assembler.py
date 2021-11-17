#!/usr/bin/env python3

import argparse
import fileinput
from instructions import instructions, shex

arg_parser = argparse.ArgumentParser(
    description='Parses assembly program and emits machine code.')
    
arg_parser.add_argument('file', metavar='FILE', help='files to read, if empty, stdin is used')
args = arg_parser.parse_args()

instruction_map = {i.name: i for i in instructions}
    

print("v2.0 raw")
for line in fileinput.input(files=args.file):
    line = line.strip()
    try:
        value = int(line)
        print(shex(value))
    except (SyntaxError, ValueError):
        split = line.split(' ')
        name = split[0]
        instruction = instruction_map[name]
        operand = int(split[1]) if len(split) > 1 else 0
        print(shex(instruction.opcode << 4 | operand))