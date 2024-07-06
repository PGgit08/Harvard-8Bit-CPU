# ASSEMBLER
from instructions import *

# open assembly file
file_name = input("Name of assembly file: ")
program_rom = "rom_content/" + file_name.replace(".asm", '') + "_rom.txt"

# create rom file
try:
    open(program_rom, 'x').close()

except Exception:
    pass

instruction_table = {}

# create instruction table
for instruction in INSTRUCTIONS:
    instruction_table[instruction.name] = hex(int(instruction.bin, 2)).replace("0x", '')


addr = 0

clearRom(program_rom)

for i in range(len(readContents("assembly/" + file_name))):
    line = readContents("assembly/" + file_name)[i].replace("\n", "")

    # Comment/Blank Checks
    if line == '' or '#' in line:
        continue

    if ' ' not in line:
        code = line
        val = '00'

    else:
        code, val = line.split(' ')

    hexCode = instruction_table[code]

    writeRom(program_rom, bin(addr), hexCode+val)

    addr += 1
