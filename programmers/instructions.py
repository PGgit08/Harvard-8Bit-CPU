from functools import reduce

### ROM/FILE EDITING FUNCTIONS ###
def readContents(file): 
    with open(file, "r") as contents:
        lines = contents.readlines()
        contents.close()

        return lines

def writeContents(file, lines): 
    with open(file, "w") as contents:
        contents.truncate(0)
        contents.writelines(lines)
        contents.close()


def clearRom(file):
    writeContents(file, ["v2.0 raw\n"] + (["0000\n"] * (2**16)))
    print("ROM CLEARED!!!")

def writeRom(file, binAddr, hexData):
    contents = readContents(file)
    contents[int(binAddr, 2) + 1] = hexData.replace('0x', '') + '\n'
    writeContents(file, contents)
    

# hexOR function
def hexOR(*hexNums):
    decimal = list(map(lambda hex: int(hex, 16), hexNums))
    or_result = reduce(lambda a, b: a | b, decimal)
    return hex(or_result)


# CONTROL LINES
A_IN = '0x0020'
B_IN = '0x0040'
A_OUT = '0xA000'
B_OUT = '0x6000'
IMM = '0x0400'
PC_OUT = '0x0002'
PC_INC = '0x4000'
PC_IN = '0xC000'
MAR_IN = '0x0008'
ROM_OUT = '0x0010'
RAM_OUT = '0x2000'
IR_IN = '0x0004'
SEQ_CLR = '0x0800'
OUT_IN = '0x1000'
HALT = '0x8000'
RAM_IN = '0x0001'
ALU_0 = '0x0080'
ALU_1 = '0x0100'
ALU_2 = '0x0200'
FLAGS_IN = '0xe000'


# represents a custom instruction
class Instruction:
    name = ""
    bin = "" # instructions's binary value
    steps = [] # instructions's control steps
    used_steps = 0
    fetch = True # preform a fetch cycle for this instruction?
    requiredFlag = -1 # the required flag for this instruction (if none then default is -1)

    def __init__(self, name, bin, steps, fetch=True, requiredFlag=-1):
        self.name = name
        self.bin = bin
        self.steps = steps
        self.fetch = fetch
        self.requiredFlag = requiredFlag

    def stepAddress(self, flag):
        stepAddress = bin(self.used_steps).replace('0b', '').zfill(3) + self.bin.replace('0b', '') + flag + '0'
        self.used_steps += 1

        return stepAddress

    def programFetchSteps(self, flag):
        if not self.fetch: return

        writeRom("rom_content/control_rom.txt", self.stepAddress(flag), hexOR(PC_OUT, MAR_IN))
        writeRom("rom_content/control_rom.txt", self.stepAddress(flag), hexOR(ROM_OUT, IR_IN, PC_INC))

    def programSteps(self, flag):
        self.used_steps = 0

        self.programFetchSteps(flag)

        for data in self.steps:
            writeRom("rom_content/control_rom.txt", self.stepAddress(flag), data)


# INSTRUCTION SET
INSTRUCTIONS = [
    Instruction("NOP", '0b00000000', [SEQ_CLR]),
    
    Instruction("LIA", '0b00000001', [
        hexOR(ROM_OUT, IMM, A_IN),
        SEQ_CLR
    ]),
    
    Instruction("LIB", '0b00000101', [
        hexOR(ROM_OUT, IMM, B_IN),
        SEQ_CLR
    ]),

    Instruction("AOUT", '0b00000010', [
        hexOR(A_OUT, OUT_IN),
        SEQ_CLR
    ]),

    Instruction("BOUT", '0b00000110', [
        hexOR(B_OUT, OUT_IN),
        SEQ_CLR
    ]),

    Instruction("HLT", '0b00000011', [
        HALT
    ], False),
    
    Instruction("STA", '0b00000100', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(A_OUT, RAM_IN),
        SEQ_CLR
    ]),

    Instruction("STB", '0b00000111', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(B_OUT, RAM_IN),
        SEQ_CLR
    ]),

    Instruction("LDA", '0b00001000', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(A_IN, RAM_OUT),
        SEQ_CLR
    ]),

    Instruction("LDB", '0b00001001', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(B_IN, RAM_OUT),
        SEQ_CLR
    ]),

    Instruction("JMP", '0b00001010', [
        hexOR(ROM_OUT, PC_IN, MAR_IN),
        hexOR(ROM_OUT, IR_IN, PC_INC),
        SEQ_CLR
    ], False),

    Instruction("ADD", '0b00001011', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(ALU_0, ALU_1, RAM_IN, FLAGS_IN),
        SEQ_CLR
    ]),

    Instruction("SAB", '0b00001111', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(ALU_1, RAM_IN, FLAGS_IN),
        SEQ_CLR
    ]),

    Instruction("SBA", '0b00010000', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(ALU_0, RAM_IN, FLAGS_IN)
    ]),

    Instruction("JMZ", '0b00010001', [
        hexOR(ROM_OUT, PC_IN, MAR_IN),
        hexOR(ROM_OUT, IR_IN, PC_INC),
        SEQ_CLR
    ], False, requiredFlag=0),

    Instruction("JMV", '0b00010010', [
        hexOR(ROM_OUT, PC_IN, MAR_IN),
        hexOR(ROM_OUT, IR_IN, PC_INC),
        SEQ_CLR
    ], False, requiredFlag=1),

    Instruction("JMN", '0b00010011', [
        hexOR(ROM_OUT, PC_IN, MAR_IN),
        hexOR(ROM_OUT, IR_IN, PC_INC),
        SEQ_CLR
    ], False, requiredFlag=2),

    Instruction("JMC", '0b00010100', [
        hexOR(ROM_OUT, PC_IN, MAR_IN),
        hexOR(ROM_OUT, IR_IN, PC_INC),
        SEQ_CLR
    ], False, requiredFlag=3),

    Instruction("OUT", '0b00010101', [
        hexOR(ROM_OUT, MAR_IN),
        hexOR(RAM_OUT, OUT_IN),
        SEQ_CLR
    ]),

    Instruction("AND", '0b00010110', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(RAM_IN, FLAGS_IN, ALU_0, ALU_2)
    ]),

    Instruction("XOR", '0b00010111', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(RAM_IN, FLAGS_IN, ALU_2)
    ]),

    Instruction("OR", '0b00011000', [
        hexOR(MAR_IN, ROM_OUT),
        hexOR(RAM_IN, FLAGS_IN, ALU_2, ALU_1)
    ])
]
