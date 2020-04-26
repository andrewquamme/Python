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
    # print("Instruction:",instruction)
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

    return fields


def get_reg(reg):
    regs = {
        0:  "$zero",
        1:  "$at",
        2:  "$v0",
        3:  "$v1",
        4:  "$a0",
        8:  "$t0",
        16: "$s0",
        17: "$s1",
        18: "$s2",
        19: "$s3",
        20: "$s4",
        21: "$s5",
        24: "$t8",
        26: "$k0",
        27: "$k1",
        28: "$gp",
        29: "$sp",
        30: "$fp",
        31: "$ra"
    }
    return regs.get(reg, "$--")


def print_mips(fields):
    instruction = ""

    if   fields['opcode'] == 0:

        if   fields['funct'] == 32:
            instruction = "add\t"

        elif fields['funct'] == 33:
            instruction = "addu\t"

        elif fields['funct'] == 34:
            instruction = "sub\t"

        instruction += f"{get_reg(fields['rd'])}, {get_reg(fields['rs'])}, {get_reg(fields['rt'])}"

    elif fields['opcode'] == 13:
        instruction = f"ori\t{get_reg(fields['rt'])}, {fields['rs']}, {fields['imm']}"

    elif fields['opcode'] == 43:
        instruction = f"sw\t{get_reg(fields['rt'])}, {fields['imm16']}({get_reg(fields['rs'])})"

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
