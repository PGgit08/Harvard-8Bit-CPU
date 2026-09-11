# PROGRAMS THE CONTROL ROM
from instructions import *

clearRom("rom_content/control_rom.txt")

for i in range(0, 16):
    flag = bin(i).replace('0b', '').zfill(4)

    for instruction in INSTRUCTIONS:
        if instruction.requiredFlag != -1 and flag[3 - instruction.requiredFlag] == '0':
            # NOP if the flag does not match the required flag for this instruction 
            Instruction("", instruction.bin, [SEQ_CLR]).programSteps(flag)

        else:
            # otherwise, program the instruction's steps for this flag
            instruction.programSteps(flag)

print("CONTROL ROM PROGRAMMED SUCCESSFULLY")
