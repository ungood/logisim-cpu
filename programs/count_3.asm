# Counts by 3, forever.
LDI 3
STA 15
LDI 0
loop: ADD 15
OUT
JMP loop