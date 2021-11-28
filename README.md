# logisim-cpu

This repository contains a "Simple as Possible" ([SAP](https://en.wikipedia.org/wiki/Simple-As-Possible_computer)) CPU
implemented with [Logisim](http://www.cburch.com/logisim/) following Ben Eater's [excellent tutorial](https://eater.net/8bit)
on building an 8-bit computer from scratch on a breadboard.

This project was created alongside my son as a way to teach him computing fundamentals.

We try to keep the design as similar as possible to Ben Eater's breadboard version, including breaking out signals
into individual wires to keep the same look.  Eventually, we may try to build the breadboard version.

## Milestones

### [SAP-1](https://github.com/ungood/logisim-cpu/releases/tag/SAP-1)

This is almost identical to the version of SAP-1 described in *Digital Computer Electronics* which has only 5 instructions:
LDA, ADD, SUB, OUT, and HLT.

It is described well, [here](https://deeprajbhujel.blogspot.com/2015/12/sap-1-instructions-and-instruction-cycle.html).

### SAP-1b

In Progress. This will be Ben Eater's version of the SAP-1 computer with added jump and conditionals.

### SAP-1.5

Planned. An upgraded version of SAP-1b with more instructions and larger memory, while still being able to be physically
realized on a breadboard with minimal new parts from the Ben Eater kit.

### Future

If we take this project further, I am undecided if we will build towards SAP-2 and SAP-3, or if, instead, we'll build
towards a 6502 design, so we can follow up with Ben Eater's 6502 series.

In either case, I do not plan on implementing future versions on bread boards. Instead, we may start to utilize FPGAs
or PCBs.