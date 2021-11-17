from dataclasses import dataclass

MI = 0b0000_0000_0000_0001
RI = 0b0000_0000_0000_0010
RO = 0b0000_0000_0000_0100
II = 0b0000_0000_0000_1000

IO = 0b0000_0000_0001_0000
CO = 0b0000_0000_0010_0000
J  = 0b0000_0000_0100_0000
CE = 0b0000_0000_1000_0000

AI = 0b0000_0001_0000_0000
AO = 0b0000_0010_0000_0000
EO = 0b0000_0100_0000_0000
SU = 0b0000_1000_0000_0000

FI = 0b0001_0000_0000_0000
BI = 0b0010_0000_0000_0000
BO = 0b0100_0000_0000_0000
OI = 0b1000_0000_0000_0000

FETCH = [ CO|MI, RO|II|CE ]

def shex(value, width=2):
    return "{value:0{width}x}".format(value=value, width=width)

@dataclass
class Instruction:
    opcode: int
    name: str
    steps: list
    
    def __post_init__(self):
        self.steps = FETCH + self.steps

instructions = [
    Instruction(0x0, 'NOP', [                        ]),
    Instruction(0x1, 'LDA', [ IO|MI, RO|AI           ]),
    Instruction(0x2, 'ADD', [ IO|MI, RO|BI, EO|AI    ]),
    Instruction(0x3, 'SUB', [ IO|MI, RO|BI, EO|AI|SU ]),

    Instruction(0x4, 'STA', [ IO|MI, AO|RI           ]),
    Instruction(0x5, 'LDI', [ IO|AI                  ]),
    Instruction(0x6, 'JMP', [ IO|J                   ]),

    Instruction(0xE, 'OUT', [ AO|OI                  ]),
    Instruction(0xF, 'HLT', [                        ]),
]

def find(predicate):
    return next(filter(predicate, instructions))

def find_opcode(opcode):
    return find(lambda instruction: instruction.opcode == opcode)
    
def find_name(name):
    return find(lambda instruction: instruction.name == name)