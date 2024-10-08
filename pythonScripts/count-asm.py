import csv
import os

# Initialize a dictionary to store instruction counts
instruction_counts = {}

directory = './TrojanJSON'

for root, dirs, files in os.walk(directory):
    # Iterate over files in the current folder
    for file in files:
        # Check if the file has a .json extension
        if file.endswith(".json"):
            # Construct the full file path
            file_path = os.path.join(root, file)
            with open(file_path, encoding='latin1') as file:
                for line in file:
                    if '"Title": "Opcode"' in line:
                        # Extract the "Description" field (assuming it's always in the same position)
                        description_start_index = line.find("Description") + len("Description") + 4
                        description_end_index = line.find(",", description_start_index)
                        description = line[description_start_index:description_end_index]

                        # Strip trailing quote if it exists
                        description = description.rstrip('"')

                        # Extract the instruction from the "Description" field
                        instruction = description.split()[0]

                        # Count the instruction
                        instruction_counts[instruction] = instruction_counts.get(instruction, 0) + 1

# Print the instruction counts
for instruction, count in instruction_counts.items():
    print(f"{instruction} {count}")


instruction_categories = {
    "Data Movement": ["movntdq","vmovsd", "pmovsxbd", "vmovq","cvtss2si","pmovzxbw", "vmovdqu", "setp","fldl2e", "pinsrw", "unpckhpd", "andnpd", "vcvtqq2pd", "pextrw", "movupd", "movhlps", "vmovd", "unpcklpd", "cmpsb", "cmpsd", "outsb", "vcvttps2qq", "insb","paddq", "pshuflw", "punpcklqdq", "punpckhqdq", "movlhps", "movlpd", "movaps","movq", "movss", "movsd", "movaps", "movups",  "data16", "pushfd", "popfd", "lodsb", "stosd", "stosb", "mov", "push", "pop", "movzx", "movsd", "movsx", "movdqa", "movdqu", "movapd", "movups", "movsw", "movsb", "movd", "fld", "fst", "fstp", "fxch", "fxch4", "fxch7", ],
    "Arithmetic and Logic": ["psubb","fcmovnb", "paddsw", "paddsb", "psubb", "pmuldq", "pmaddubsw", "pmulhw", "pmulld","sbb","rol","xorpd", "vpxor", "pxor",  "shl", "xorps","vxorps","xor","imul", "subpd","psubq", "mulpd", "addpd","pmaxub","tzcnt", "pclmulqdq", "pinsrd","cvtsd2ss", "subsd", "orpd", "orps","psllw","mulss","addss","divss","fsin","psrlw","pmullw","cmovnb", "rcl","f2xm1","cvttsd2si","pslld","psrlq","fsubr","divsd","addsd","fisttp","fmulp","psllq", "mulsd", "rcr", "psrldq", "psrld", "psllq", "por", "pand", "pmaddwd",  "xadd", "psubd", "pslldq", "paddb", "paddq", "paddw", "bswap", "shrd", "add", "sub", "inc", "dec", "adc",  "and", "or", "not", "neg",  "shr", "sar", "ror", "idiv", "div", "mul", "cdq"],
    "Control Transfer": ["int1","iretd","salc", "ud2","jecxz", "int3", "loopne",  "shld", "loop", "in", "leave", "setl", "setns", "setnbe", "cmovb", "rep", "repne", "setz", "setnz", "setnle", "setb", "setnb", "sets", "call", "ret", "jmp", "jz", "jnz", "jb", "jbe", "jnb", "jnbe", "js", "jns", "jl", "jle", "jnl", "jnle", "jo", "jno", "jc", "jnc", "jpe", "jpo", "jp", "jnp", "jcxe"],
    "Comparison": ["cmpss","scasd","comisd", "pcmpgtd","fucomip", "ucomisd", "pcmpeqd", "pcmpgtb","comiss","ucomiss","fcomi","scasb", "pcmpistri", "pcmpeqb", "pcmpeqw", "psadbw", "cmppd", "fcomip", "cmovz", "cmovnz", "cmovp", "cmovnp", "cmovbe", "cmovnbe", "cmovl", "cmovnl", "cmovle", "cmovnle", "cmovs", "cmovns", "cmovo", "cmovno", "cmp", "test", "bt", "bts", "btr", "bsr", "bsf", "btc"],
    "Miscellaneous": ["monitorx", "psrad", "psraw","vcvttss2usi", "vcvttpd2uqq","xacquire","xrelease","cvtdq2ps", "cvttps2dq", "vcvtuqq2pd", "aam", "pshufw", "enter", "xlat", "andps", "sldt", "vpextrd", "les", "addr16", "lds", "sgdt", "out", "aad","fxtract", "setbe", "setnp","aas", "daa", "aaa", "das","movlps", "movhps", "lddqu", "fidivr","prefetcht0","prefetchnta","cvttss2si","cvtss2sd","fincstp","popad","pushad","fyl2x","lodsw","seto","setnl","setle","setno","pandn","cmovnb""popad", "cwde", "emms", "fldenv", "ldmxcsr", "loop", "movss", "movsd", "punpckhbw", "andpd", "nop", "fwait", "pause", "lea", "lock", "nop", "pause", "int", "wait", "clc", "stc", "cmc", "cli", "cld", "std", "sahf", "lahf", "xgetbv", "rdmsr", "sysenter", "sysexit"],
    "Floating-Point": ["fdecstp","minsd","psubsb","fyl2xp1","psubusb","phaddw","fldl2t","maxsd","vcvttpd2qq", "fldln2", "fldlg2", "fstpnce", "addps", "mulps", "ftst", "fcmovne", "fbstp", "sqrtsd","cvtsi2sd", "cvtps2pd", "cvtdq2pd", "cvtpd2ps", "faddp", "fsubp", "fsubrp", "fdivp", "fdivr", "fdivrp", "fnclex", "fninit", "fldcw", "fld1", "fldz", "fldpi", "fnstcw", "fnstsw", "fnstenv", "fnstsw", "fstcw", "fstsw", "fstenv", "fstsw", "fild", "fist", "fistp", "fild", "fadd", "fsub", "fmul", "fdiv", "fcom", "fcomp", "fcompp", "fptan",  "fprem", "fsincos", "frndint", "fscale", "fsqrt", "fabs", "fchs", "fxch", "fprem1", "fucom", "fucomp", "fucompp", "fxam", "fiadd",  "fidiv", "ficom", "ficom", "fldt", "fstpt", "frstors", "fnsave", "fnstsw", "fsave",  "fstenv", "fstdw", "ffree", "ffreep", "fstp", "fstsw", "fstsw", "fs", "fsavew", "fnsavew", "fwait", "fnop"],
    "Vector Operations": ["psubsw", "paddusw", "pmaxsw", "punpckhwd","pminsw", "psubq", "vpinsrd", "bound", "vpinsrd", "psrldq", "pshufw", "vcvtqq2pd", "vbroadcastss", "pmuludq","movmskpd", "pshufhw", "punpcklwd","punpckldq","paddusb","pmovmskb", "vzeroupper","vpmovmskb","vpcmpeqb","vpcmpeqw","vpmovmskb", "pshufb", "punpcklbw", "bnd", "pshufd", ],
    "System and Control": ["clts", "smsw", "lfence", "rdrand", "cpuid", "rdtsc","rdtscp","lfence", "sfence", "mfence", "clflush", "rdpmc", "rsm", "invlpg", "invlpga", "wrmsr", "wbnoiner"],
    "Encryption": ["vmovups","pblendw","palignr", "vmovaps","xchg","vinsertf128","stmxcsr","fxsave", "fxrstor","stosw","fisub","wbinvd","ficomp", "lar", "ud0", "sysret", "syscall", "hint-not-taken","hint-taken","hlt", "frstor","shufps", "punpckhdq","psubw","packuswb","psubusw","arpl", "sti", "femms","invd","into", "aesimc", "aeskeygenassist", "aesenc", "fimul", "cvtsd2si", "cvtsi2ss", "subss","lodsd","fcos","fpatan","pextrd","packssdw", "packsswb","paddd","pcmpgtw","insd", "outsd","unpckhps", "fbld", "loope",]
}

unknown_instructions = set()

# Initialize a dictionary to store counts for each category
category_counts = {category: 0 for category in instruction_categories}

# Loop through the counts and categorize them
for instruction, count in instruction_counts.items():
    found_category = False
    for category, category_instructions in instruction_categories.items():
        if instruction in category_instructions:
            category_counts[category] += count
            found_category = True
            break
    if not found_category:
        unknown_instructions.add(instruction)


# Print the counts for each category
for category, count in category_counts.items():
    print(f"{category}: {count}")

# Print unknown instructions
if unknown_instructions:
    print("\nUnknown Instructions:")
    for instruction in unknown_instructions:
        print(instruction)

# Save the instruction counts to a CSV file
with open('trojan_instruction_counts.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write the header
    csv_writer.writerow(['Instruction', 'Count'])

    # Write the instruction counts
    for instruction, count in instruction_counts.items():
        csv_writer.writerow([instruction, count])

    # Write a blank row between instruction and category counts
    csv_writer.writerow([])

    # Write the header for category counts
    csv_writer.writerow(['Category', 'Count'])

    # Write the category counts
    for category, count in category_counts.items():
        csv_writer.writerow([category, count])

print("Instruction counts saved to 'instruction_counts.csv'")