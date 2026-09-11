# Harvard-8Bit-CPU
An 8 bit CPU designed in Logisim with a custom assembler. A modification of Ben Eater’s 8-bit CPU design that uses a Harvard Architecture.

## Instruction Set
### Register Operations
- **LIA [imm8]** - Load immediate into register A
- **LIB [imm8]** - Load immediate into register B
- **LDA [addr8]** - Load RAM into register A
- **LDB [addr8]** - Load RAM into register B
- **STA [addr8]** - Store register A's contents in RAM
- **STB [addr8]** - Store register B's contents in RAM
- **AOUT** - Display the contents of register A
- **BOUT** - Display the contents of register B

### ALU Operations
- **ADD [addr8]** - Add registers A and B and store in RAM
- **SAB [addr8]** - Subtract register B from A and store in RAM
- **SBA [addr8]** - Subtract register A from B and store in RAM
- **AND [addr8]** - AND registers A and B and store in RAM
- **XOR [addr8]** - XOR registers A and B and store in RAM
- **OR [addr8]** - OR registers A and B and store in RAM

### Jump / Conditional Operations
- **JMP [addr8]** - Jump in program
- **JMZ [addr8]** - Jump in program if ALU last gave zero
- **JMV [addr8]** - Jump in program if ALU last gave overflow
- **JMN [addr8]** - Jump in program if ALU last gave negative
- **JMC [addr8]** - Jump in program if ALU last gave carry

### Miscellaneous
- **OUT [addr8]** - Display a value in RAM
- **NOP** - Do nothing
- **HLT** - Halt the program

## Assembling / Running A Program
Run `program_rom_programmer.py` and put in the name of the desired assembly program. This will generate a `[program_name]_rom.txt` in the `rom_content` folder. In Logisim, load that ROM text file into the PROGRAM ROM, and finally enable ticks to run the program.
