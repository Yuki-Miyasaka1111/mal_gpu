import csv
import os

# ディレクトリ設定
base_directory = '/workspaces/mal_gpu/data/interim/extract_all_data'
output_directory01 = '/workspaces/mal_gpu/data/interim/family_asm_count_csv/instruction_counts'
output_directory02 = '/workspaces/mal_gpu/data/interim/family_asm_count_csv/category_counts'

if not os.path.exists(output_directory01):
    os.makedirs(output_directory01)

if not os.path.exists(output_directory02):
    os.makedirs(output_directory02)

# 命令カテゴリ定義
instruction_categories = {
    "Data Movement": ["movntdq", "vmovsd", "pmovsxbd", "vmovq", "cvtss2si", "pmovzxbw", "vmovdqu", "setp", "fldl2e", "pinsrw", "unpckhpd", "andnpd", "vcvtqq2pd", "pextrw", "movupd", "movhlps", "vmovd", "unpcklpd", "cmpsb", "cmpsd", "outsb", "vcvttps2qq", "insb", "paddq", "pshuflw", "punpcklqdq", "punpckhqdq", "movlhps", "movlpd", "movaps", "movq", "movss", "movsd", "movaps", "movups", "data16", "pushfd", "popfd", "lodsb", "stosd", "stosb", "mov", "push", "pop", "movzx", "movsd", "movsx", "movdqa", "movdqu", "movapd", "movups", "movsw", "movsb", "movd", "fld", "fst", "fstp", "fxch", "fxch4", "fxch7", "cvtps2dq", "str"],
    "Arithmetic and Logic": ["psubb", "fcmovnb", "paddsw", "paddsb", "psubb", "pmuldq", "pmaddubsw", "pmulhw", "pmulld", "sbb", "rol", "xorpd", "vpxor", "pxor", "shl", "xorps", "vxorps", "xor", "imul", "subpd", "psubq", "mulpd", "addpd", "pmaxub", "tzcnt", "pclmulqdq", "pinsrd", "cvtsd2ss", "subsd", "orpd", "orps", "psllw", "mulss", "addss", "divss", "fsin", "psrlw", "pmullw", "cmovnb", "rcl", "f2xm1", "cvttsd2si", "pslld", "psrlq", "fsubr", "divsd", "addsd", "fisttp", "fmulp", "psllq", "mulsd", "rcr", "psrldq", "psrld", "psllq", "por", "pand", "pmaddwd", "xadd", "psubd", "pslldq", "paddb", "paddq", "paddw", "bswap", "shrd", "add", "sub", "inc", "dec", "adc", "and", "or", "not", "neg", "shr", "sar", "ror", "idiv", "div", "mul", "cdq", "subps", "fisubr", "rcpps"],
    "Control Transfer": ["int1", "fcmovnu", "fcmovnbe", "xabort", "iretd", "salc", "ud2", "jecxz", "int3", "loopne", "shld", "loop", "in", "leave", "setl", "setns", "setnbe", "cmovb", "rep", "repne", "setz", "setnz", "setnle", "setb", "setnb", "sets", "call", "ret", "jmp", "jz", "jnz", "jb", "jbe", "jnb", "jnbe", "js", "jns", "jl", "jle", "jnl", "jnle", "jo", "jno", "jc", "jnc", "jpe", "jpo", "jp", "jnp", "jcxe"],
    "Comparison": ["cmpss", "scasd", "comisd", "pcmpgtd", "fucomip", "ucomisd", "pcmpeqd", "pcmpgtb", "comiss", "ucomiss", "fcomi", "scasb", "pcmpistri", "pcmpeqb", "pcmpeqw", "psadbw", "cmppd", "fcomip", "cmovz", "cmovnz", "cmovp", "cmovnp", "cmovbe", "cmovnbe", "cmovl", "cmovnl", "cmovle", "cmovnle", "cmovs", "cmovns", "cmovo", "cmovno", "cmp", "test", "bt", "bts", "btr", "bsr", "bsf", "btc"],
    "Miscellaneous": ["monitorx", "psrad", "psraw", "vcvttss2usi", "vcvttpd2uqq", "xacquire", "xrelease", "cvtdq2ps", "cvttps2dq", "vcvtuqq2pd", "aam", "pshufw", "enter", "xlat", "andps", "sldt", "vpextrd", "les", "addr16", "lds", "sgdt", "out", "aad", "fxtract", "setbe", "setnp", "aas", "daa", "aaa", "das", "movlps", "movhps", "lddqu", "fidivr", "prefetcht0", "prefetchnta", "cvttss2si", "cvtss2sd", "fincstp", "popad", "pushad", "fyl2x", "lodsw", "seto", "setnl", "setle", "setno", "pandn", "cmovnb", "popad", "cwde", "emms", "fldenv", "ldmxcsr", "loop", "movss", "movsd", "punpckhbw", "andpd", "nop", "fwait", "pause", "lea", "lock", "nop", "pause", "int", "wait", "clc", "stc", "cmc", "cli", "cld", "std", "sahf", "lahf", "xgetbv", "rdmsr", "sysenter", "sysexit"],
    "Floating-Point": ["fdecstp", "fdisi8087_nop", "fsetpm287_nop", "fucomi", "minsd", "psubsb", "fyl2xp1", "psubusb", "phaddw", "fldl2t", "maxsd", "vcvttpd2qq", "fldln2", "fldlg2", "fstpnce", "addps", "mulps", "ftst", "fcmovne", "fbstp", "sqrtsd", "cvtsi2sd", "cvtps2pd", "cvtdq2pd", "cvtpd2ps", "faddp", "fsubp", "fsubrp", "fdivp", "fdivr", "fdivrp", "fnclex", "fninit", "fldcw", "fld1", "fldz", "fldpi", "fnstcw", "fnstsw", "fnstenv", "fnstsw", "fstcw", "fstsw", "fstenv", "fstsw", "fild", "fist", "fistp", "fild", "fadd", "fsub", "fmul", "fdiv", "fcom", "fcomp", "fcompp", "fptan", "fprem", "fsincos", "frndint", "fscale", "fsqrt", "fabs", "fchs", "fxch", "fprem1", "fucom", "fucomp", "fucompp", "fxam", "fiadd", "fidiv", "ficom", "ficom", "fldt", "fstpt", "frstors", "fnsave", "fnstsw", "fsave", "fstenv", "fstdw", "ffree", "ffreep", "fstp", "fstsw", "fstsw", "fs", "fsavew", "fnsavew", "fwait", "fnop"],
    "Vector Operations": ["psubsw", "paddusw", "pmaxsw", "punpckhwd", "pminsw", "psubq", "vpinsrd", "bound", "vpinsrd", "psrldq", "pshufw", "vcvtqq2pd", "vbroadcastss", "pmuludq", "movmskpd", "pshufhw", "punpcklwd", "punpckldq", "paddusb", "pmovmskb", "vzeroupper", "vpmovmskb", "vpcmpeqb", "vpcmpeqw", "vpmovmskb", "pshufb", "punpcklbw", "bnd", "pshufd"],
    "System and Control": ["sidt", "lmsw", "vhaddpd", "vpsraw", "unpcklps", "clts", "smsw", "lfence", "rdrand", "cpuid", "rdtsc", "rdtscp", "lfence", "sfence", "mfence", "clflush", "rdpmc", "rsm", "invlpg", "invlpga", "wrmsr", "wbnoiner"],
    "Encryption": ["vmovups", "pblendw", "palignr", "vmovaps", "xchg", "vinsertf128", "stmxcsr", "fxsave", "fxrstor", "stosw", "fisub", "wbinvd", "ficomp", "lar", "ud0", "sysret", "syscall", "hint-not-taken", "hint-taken", "hlt", "frstor", "shufps", "punpckhdq", "psubw", "packuswb", "psubusw", "arpl", "sti", "femms", "invd", "into", "aesimc", "aeskeygenassist", "aesenc", "fimul", "cvtsd2si", "cvtsi2ss", "subss", "lodsd", "fcos", "fpatan", "pextrd", "packssdw", "packsswb", "paddd", "pcmpgtw", "insd", "outsd", "unpckhps", "fbld", "loope"]
}

# 未知の命令に対して空のセットを初期化
unknown_instructions = set()

# 各ファミリーディレクトリ内のJSONファイルを処理する関数
def process_family(family_name, family_folder):
    instruction_counts = {}
    category_counts = {category: 0 for category in instruction_categories}
    
    # ファミリフォルダー内のすべてのファイルを反復処理
    for root, dirs, files in os.walk(family_folder):
        for file_name in files:
            if file_name.endswith(".json") or file_name.endswith(".exe"):
                file_path = os.path.join(root, file_name)

                try:
                    with open(file_path, encoding='latin1') as json_file:
                        for line in json_file:
                            if '"Title": "Opcode"' in line:
                                description_start_index = line.find("Description") + len("Description") + 4
                                description_end_index = line.find(",", description_start_index)
                                description = line[description_start_index:description_end_index].rstrip('"')

                                # 命令を抽出
                                instruction = description.split()[0]

                                # 命令をカウント
                                instruction_counts[instruction] = instruction_counts.get(instruction, 0) + 1
                except Exception as e:
                    print(f"Error processing file {file_name}: {e}")
                    continue

    # 命令のカテゴライズ
    for instruction, count in instruction_counts.items():
        found_category = False
        for category, category_instructions in instruction_categories.items():
            if instruction in category_instructions:
                category_counts[category] += count
                found_category = True
                break
        if not found_category:
            unknown_instructions.add(instruction)

    # Instructionカウントを保存するファイル
    instruction_output_file = os.path.join(output_directory01, f'{family_name}.csv')
    with open(instruction_output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # ヘッダーを書き込む
        csv_writer.writerow(['Instruction', 'Count'])

        # 命令数を書き込む
        for instruction, count in instruction_counts.items():
            csv_writer.writerow([instruction, count])

    print(f"Instruction counts saved to '{instruction_output_file}'")

    # Categoryカウントを保存するファイル
    category_output_file = os.path.join(output_directory02, f'{family_name}.csv')
    with open(category_output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # カテゴリとカウントのヘッダーを書き込む
        csv_writer.writerow(['Category', 'Count'])

        # カテゴリーごとのカウントを書き込む
        for category, count in category_counts.items():
            csv_writer.writerow([category, count])

    print(f"Category counts saved to '{category_output_file}'")

# 各ファミリーのディレクトリを処理
for family_folder in os.listdir(base_directory):
    family_path = os.path.join(base_directory, family_folder)
    if os.path.isdir(family_path):
        print(f"Processing family: {family_folder}")
        process_family(family_folder, family_path)

# 不明な命令を出力
if unknown_instructions:
    print("\nUnknown Instructions:")
    for instruction in unknown_instructions:
        print(instruction)