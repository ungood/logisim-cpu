# Multiplies the values in x and y and displays the result
init:
LDA x
STA product  # Initialize product with value of x

loop:
LDA y
SUB one      # Subtract 1 from y
STA y
JZ  halt     # Halt if y is now zero
LDA product 
ADD x
STA product  # Add x to product
JMP loop

halt:
OUT
HLT

one: 1       # Constant 1
x: 4
y: 5
product: 0