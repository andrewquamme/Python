# FILE:       mips.py
# AUTHOR:     Andrew Quamme
# PURPOSE:    Decode hex instructions into MIPs instructions
# USAGE:      python3 mips.py {hex}
#
# EXAMPLE:    python3 mips.py 0x02328020 0x02328020 0xac100070
# 
#             add     $s0, $s1, $s2
#             add     $s0, $s1, $s2
#             sw      $s0, 112($zero)

from sys import argv

def extract_fields(instruction):
    print("Instruction:",instruction)
    instruction = int(instruction, 16)
    fields = {
        "opcode": (instruction >> 26) & 0x3f, # bit [31-26]
        "rs": (instruction >> 21) & 0x1f,     # bit [25-21]
        "rt": (instruction >> 16) & 0x1f,     # bit [20-16]
        "rd": (instruction >> 11) & 0x1f,     # bit [15-11]
        "shamt": (instruction >> 6) & 0x1f,   # bit [10- 6]
        "funct": instruction & 0x3f,          # bit [ 0- 5]
        "imm16": instruction & 0xffff,        # bit [15- 0]
        "address": instruction & 0x03ffffff,  # bit [25- 0]
        # "imm32": signExtend16to32(instruction & 0xffff)
    }
    print(fields)
    return fields


def get_reg(reg):

    regs =[ 
    "$zero", "$at", "$v0", "$v1", "$a0",
    "$a1",   "$a2", "$a3", "$t0", "$t1",
    "$t2",   "$t3", "$t4", "$t5", "$t6",
    "$t7",   "$s0", "$s1", "$s2", "$s3",
    "$s4",   "$s5", "$s6", "$s7", "$t8",
    "$t9",   "$k0", "$k1", "$gp", "$sp",
    "$fp",   "$ra" ]

    return regs[reg]


def print_mips(fields):
    instruction = "Not a valid (yet?) instruction"

    opcode = fields['opcode']
    rs     = get_reg(fields['rs'])
    rt     = get_reg(fields['rt'])
    imm16  = hex(fields['imm16'])

    if   opcode == 0: # R-Type
        funct = fields['funct']
        rd    = get_reg(fields['rd'])

        if   funct == 0: # sll
            instruction = f"sll\t{rd}, {rt}, {fields['shamt']}"

        if   funct == 32: # add
            instruction = f"add\t{rd}, {rs}, {rt}"

        elif funct == 33: # addu
            instruction = f"addu\t{rd}, {rs}, {rt}"

        elif funct == 34: # sub
            instruction = f"sub\t{rd}, {rs}, {rt}"
        
        elif funct == 35: # subu
            instruction = f"subu\t{rd}, {rs}, {rt}"
        
        elif funct == 38: # xor
            instruction = f"xor\t{rd}, {rs}, {rt}"
        
        elif funct == 43: # sub
            instruction = f"sltu\t{rd}, {rs}, {rt}"

    elif opcode == 4: # beq
        instruction = f"beq\t{rs}, {rt}, {imm16}"

    elif opcode == 8: # addi
        instruction = f"addi\t{rt}, {rs}, {imm16}"
    
    elif opcode == 10: # slti
        instruction = f"slti\t{rt}, {rs}, {imm16}"

    elif opcode == 13: # ori
        instruction = f"ori\t{rt}, {rs}, {imm16}"
    
    elif opcode == 32: # lb
        instruction = f"lb\t{rt}, {imm16}({rs})"
    
    elif opcode == 35: # lw
        instruction = f"lw\t{rt}, {imm16}({rs})"
    
    elif opcode == 41: # sh
        instruction = f"sh\t{rt}, {imm16}({rs})"

    elif opcode == 43: # sw
        instruction = f"sw\t{rt}, {imm16}({rs})"

    print(instruction)


def main():
    if (len(argv) == 1):
        print("Enter hex: ")
        instruction = input()
        extract_fields(instruction)
    else:
        instructions = []

        for instruction in argv[1:]:
            instructions.append(extract_fields(instruction))
        
        for fields in instructions:
            print_mips(fields)

if __name__ == "__main__":
    main()
