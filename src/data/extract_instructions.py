import csv
import sys
import os
import re
import codecs  # アンエスケープ用
from tqdm import tqdm
import logging

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/extract_instructions.log'),
        logging.StreamHandler()
    ]
)

# フィールドサイズの上限を設定
csv.field_size_limit(sys.maxsize)

# 入力となるCSVファイル
input_csv = '/workspaces/mal_gpu/data/interim/tokenizer_training_data01.csv'

# 出力となるテキストファイル
output_txt_concatenated = '/workspaces/mal_gpu/data/interim/tokenizer_training_data_concatenated01.txt'
output_txt_non_concatenated = '/workspaces/mal_gpu/data/interim/tokenizer_training_data_non_concatenated01.txt'

# ファイルの存在チェック
if not os.path.exists(input_csv):
    logging.error(f"ファイルが見つかりません: {input_csv}")
    sys.exit(1)
else:
    logging.info('入力ファイルの存在を確認しました')

# 総行数の設定（14,866行）
total_lines = 14866  # 必要に応じて変更

# オペコードのリストを用意
opcodes = [
    'aaa', 'aad', 'aam', 'aas', 'adc', 'add', 'and', 'arpl', 'bound', 'bsf', 'bsr', 'bswap', 'bt', 'btc', 'btr', 'bts', 
    'call', 'cbw', 'cdq', 'cdqe', 'clc', 'cld', 'clflush', 'cli', 'clts', 'cmc', 'cmp', 'cmpsb', 'cmpsd', 'cmpsq', 'cmpsw', 
    'cmpxchg', 'cmpxchg16b', 'cmpxchg8b', 'cpuid', 'cwd', 'cwde', 'daa', 'das', 'dec', 'div', 'enter', 'hlt', 'idiv', 
    'imul', 'in', 'inc', 'insb', 'insd', 'insw', 'int', 'int3', 'into', 'invd', 'invlpg', 'iret', 'iretd', 'iretw', 
    'ja', 'jae', 'jb', 'jbe', 'jc', 'jcxz', 'je', 'jecxz', 'jg', 'jge', 'jl', 'jle', 'jmp', 'jna', 'jnae', 'jnb', 
    'jnbe', 'jnc', 'jne', 'jng', 'jnge', 'jnl', 'jnle', 'jno', 'jnp', 'jns', 'jnz', 'jo', 'jp', 'jpe', 'jpo', 'js', 
    'jz', 'lahf', 'lar', 'lds', 'lea', 'leave', 'les', 'lfs', 'lgdt', 'lgs', 'lidt', 'lldt', 'lmsw', 'loadall', 'lodsb', 
    'lodsd', 'lodsq', 'lodsw', 'loop', 'loope', 'loopne', 'loopnz', 'loopz', 'lsl', 'lss', 'ltr', 'mfence', 'mov', 
    'movaps', 'movd', 'movdqa', 'movdqu', 'movdq2q', 'movq', 'movsb', 'movsd', 'movsq', 'movsw', 'movsx', 'movsxd', 
    'movzx', 'mul', 'neg', 'nop', 'not', 'or', 'out', 'outsb', 'outsd', 'outsw', 'pop', 'popa', 'popad', 'popcnt', 
    'popf', 'popfd', 'popfq', 'push', 'pusha', 'pushad', 'pushf', 'pushfd', 'pushfq', 'rcl', 'rcr', 'rdmsr', 'rdpmc', 
    'rdtsc', 'rdx', 'rep', 'repe', 'repne', 'repnz', 'repz', 'ret', 'rol', 'ror', 'rsm', 'sahf', 'sal', 'sar', 'sbb', 
    'scasb', 'scasd', 'scasq', 'scasw', 'seta', 'setae', 'setb', 'setbe', 'setc', 'sete', 'setg', 'setge', 'setl', 
    'setle', 'setna', 'setnae', 'setnb', 'setnbe', 'setnc', 'setne', 'setng', 'setnge', 'setnl', 'setnle', 'setno', 
    'setnp', 'setns', 'setnz', 'seto', 'setp', 'setpe', 'setpo', 'sets', 'setz', 'sgdt', 'shl', 'shld', 'shr', 'shrd', 
    'sidt', 'sldt', 'smsw', 'stc', 'std', 'sti', 'stosb', 'stosd', 'stosq', 'stosw', 'str', 'sub', 'test', 'verr', 
    'verw', 'wait', 'wbinvd', 'wrmsr', 'xadd', 'xchg', 'xlat', 'xor', 'xgetbv', 'xsetbv', 'vmcall', 'vmlaunch', 'vmresume', 
    'vmxoff', 'vmxon', 'vmptrld', 'vmptrst', 'vmclear', 'vmread', 'vmwrite', 'vmlaunch', 'vmresume', 'movq2dq', 'paddb', 
    'paddd', 'paddq', 'paddsb', 'paddsw', 'paddusb', 'paddusw', 'paddw', 'pand', 'pandn', 'pavgb', 'pavgw', 'pcmpeqb', 
    'pcmpeqd', 'pcmpeqw', 'pcmpgtb', 'pcmpgtd', 'pcmpgtw', 'pextrw', 'pinsrw', 'pmaddwd', 'pmaxsw', 'pmaxub', 'pminsw', 
    'pminub', 'pmovmskb', 'pmulhw', 'pmullw', 'por', 'psadbw', 'pshufw', 'pslld', 'psllq', 'psllw', 'psrad', 'psraw', 
    'psrld', 'psrlq', 'psrlw', 'psubb', 'psubd', 'psubq', 'psubsb', 'psubsw', 'psubusb', 'psubusw', 'psubw', 'punpckhbw', 
    'punpckhdq', 'punpckhwd', 'punpcklbw', 'punpckldq', 'punpcklwd', 'pxor', 'cvtps2pd', 'cvtpd2ps', 'cvtdq2ps', 
    'cvtps2dq', 'cvttpd2dq', 'cvttps2dq', 'addpd', 'addps', 'addsd', 'addss', 'andnpd', 'andnps', 'andpd', 'andps', 
    'cmppd', 'cmpps', 'cmpsd', 'cmpss', 'comisd', 'comiss', 'cvtdq2pd', 'cvtpd2dq', 'cvtpi2ps', 'cvtps2pi', 'cvtsd2si', 
    'cvtsi2sd', 'cvtsi2ss', 'cvtss2si', 'cvttpd2pi', 'cvttsd2si', 'cvttss2si', 'divpd', 'divps', 'divsd', 'divss', 
    'lddqu', 'maxpd', 'maxps', 'maxsd', 'maxss', 'minpd', 'minps', 'minsd', 'minss', 'movapd', 'movaps', 'movhpd', 
    'movhps', 'movlpd', 'movlps', 'movmskpd', 'movmskps', 'movntdq', 'movntpd', 'movntps', 'movnti', 'mulps', 'mulpd', 
    'mulsd', 'mulss', 'orpd', 'orps', 'shufpd', 'shufps', 'sqrtpd', 'sqrtps', 'sqrtsd', 'sqrtss', 'subpd', 'subps', 
    'subsd', 'subss', 'unpckhpd', 'unpckhps', 'unpcklpd', 'unpcklps', 'xorpd', 'xorps'
    # 他の拡張命令セット（SSE, SSE2, AVXなど）や最新のアーキテクチャに対応した命令も追加できます
]

# オペコードを非キャプチャグループで定義
opcode_pattern = r'\b(?:' + '|'.join(opcodes) + r')\b'

# 命令を分割するための正規表現パターン
instruction_regex = re.compile(r'(' + opcode_pattern + r'.*?)(?=' + opcode_pattern + r'|\Z)', re.IGNORECASE)

# 命令全体を連結するための関数
def concatenate_instruction_operands(instruction_line):
    # 命令を分割（最初の部分がオペコード、それ以降がオペランド）
    parts = instruction_line.strip().split(None, 1)
    if len(parts) == 2:
        opcode, operands = parts
        # オペランド内の空白とカンマを削除して連結
        operands = operands.replace(' ', '').replace(',', '')
        return opcode + operands
    else:
        # オペランドがない場合
        return parts[0]

# すべてのエスケープシーケンスをアンエスケープする関数
def unescape_control_characters(instruction):
    try:
        # unicode_escapeで通常の制御文字をアンエスケープ
        unescaped_instruction = codecs.decode(instruction, 'unicode_escape')
        # さらにlatin1を使用して16進数やUnicodeエスケープに対応
        return unescaped_instruction.encode('latin1').decode('unicode_escape')
    except Exception as e:
        logging.warning(f"アンエスケープ処理でエラーが発生しました: {e}")
        return instruction

with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile, \
     open(output_txt_concatenated, 'w', encoding='utf-8') as txtfile_concat, \
     open(output_txt_non_concatenated, 'w', encoding='utf-8') as txtfile_non_concat:

    reader = csv.reader(csvfile)
    header = next(reader)
    instructions_index = header.index('instructions')  # 'instructions'カラムのインデックスを取得

    logging.info('CSVファイルの処理を開始します')

    for row in tqdm(reader, total=total_lines, dynamic_ncols=True):
        try:
            instructions = row[instructions_index]

            # アンエスケープ処理を適用
            instructions = unescape_control_characters(instructions)

            # 正規表現を使用して命令を抽出
            instruction_list = instruction_regex.findall(instructions)

            # 各命令について処理
            concatenated_instructions = []
            non_concatenated_instructions = []

            for instruction in instruction_list:
                instruction = instruction.strip()
                if not instruction:
                    continue  # 空の命令をスキップ

                # 非連結パターン（そのまま）
                non_concatenated_instructions.append(instruction)

                # 連結パターン
                concatenated_instruction = concatenate_instruction_operands(instruction)
                concatenated_instructions.append(concatenated_instruction)

            # テキストファイルに書き込み
            # 連結パターン
            for instruction in concatenated_instructions:
                txtfile_concat.write(instruction + '\n')
            # 関数間の区切りとして空行を追加（オプション）
            txtfile_concat.write('\n')

            # 非連結パターン
            for instruction in non_concatenated_instructions:
                txtfile_non_concat.write(instruction + '\n')
            # 関数間の区切りとして空行を追加（オプション）
            txtfile_non_concat.write('\n')

        except Exception as e:
            logging.warning(f"エラーが発生しました: {e}")
            continue

    logging.info('処理が完了しました')
