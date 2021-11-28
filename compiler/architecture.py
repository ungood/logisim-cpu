from dataclasses import dataclass, field
from io import TextIOBase

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

@dataclass
class Operation(object):
    opcode: int
    name: str
    steps: list
    
    def __post_init__(self):
        self.steps = FETCH + self.steps

@dataclass
class Architecture(object):
    name: str
    address_width: int = 8   # The width of the memory address register
    memory_width:  int = 4   # The width of each word in memory.
    opcode_width:  int = 4   # The width of each operation.
    pc_width:      int = 4   # The number of bits in the program counter.
    step_width:    int = 3   # The number of bits in the step counter.
    operations:    list = field(default_factory=list)
    flags:         list = field(default_factory=list)

    def __post_init__(self):
        self.max_addresses = 2**self.address_width
        self.max_operations = 2**self.opcode_width
        self.max_steps = 2**self.step_width

        self.opcodes = {op.opcode: op for op in self.operations}
        self.nop = self.opcodes[0]


SAP_1 = Architecture('SAP-1', step_width=4, operations=[
    Operation(0x0, 'NOP', [                           ]),
    Operation(0x1, 'LDA', [ IO|MI, RO|AI              ]),
    Operation(0x2, 'ADD', [ IO|MI, RO|BI, EO|AI|FI    ]),

    Operation(0xE, 'OUT', [ AO|OI                     ]),
    Operation(0xF, 'HLT', [                           ]),
])

SAP_1B = Architecture('SAP-1b', operations=SAP_1.operations + [
    Operation(0x3, 'SUB', [ IO|MI, RO|BI, EO|AI|SU|FI ]),
    Operation(0x4, 'STA', [ IO|MI, AO|RI              ]),
    Operation(0x5, 'LDI', [ IO|AI                     ]),
    Operation(0x6, 'JMP', [ IO|J                      ]),
    Operation(0x7, 'JZ',  [                           ]),
])

ARCHITECTURES = [SAP_1, SAP_1B]

if __name__ == "__main__":
    print(ARCHITECTURES)