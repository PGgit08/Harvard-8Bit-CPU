# start with 1 in both registers
LIA 01
LIB 01

# display registers
AOUT
BOUT

# add registers
ADD 00

# output sum
OUT 00

# load register A with sum
LDA 00

# add again
ADD 00

# output sum
OUT 00

# load register B with sum
LDB 00

# jump to very start if overflow
JMV 00

# jump to first addition
JMP 04
