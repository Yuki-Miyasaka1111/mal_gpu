import os
import json
import re

def normalize_memory_addresses_and_immediates(text):
    """
    メモリアドレスや動的即値を正規化する関数。
    - メモリアドレス (0x で始まる16進数の値) を "memoryaddress" に置換。
    - 動的に変化する即値を "immediatevalue" に置換。
    """
    # メモリアドレスの置換 (例: 0x775ade2d -> memoryaddress)
    text = re.sub(r'0x[0-9a-fA-F]{6,8}', 'memoryaddress', text)

    # immediatevalueには置換する必要がなかったのでコメントアウト
    # 動的に変化する即値を "immediatevalue" に置換（長さに応じて判断）
    # text = re.sub(r'\b\d+\b', 'immediatevalue', text)

    return text

def escape_control_characters(text):
    """
    Descriptionフィールド内の制御文字をエスケープする関数。
    """
    return re.sub(r'[\x00-\x1F]', lambda match: '\\u{:04x}'.format(ord(match.group())), text)

def process_json_files_for_normalization(folder_path):
    """
    フォルダ内のすべてのJSONファイルを処理し、'Description' フィールド内の
    メモリアドレスや即値の正規化、および制御文字のエスケープを行う。
    """
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                
                # ファイルを開いてJSON内容を読み込み、エラーが発生した場合はスキップ
                content = None
                try:
                    # UTF-8 で読み込みを試みる
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"UTF-8での読み込みエラー: {file_path}")
                    print(f"エラー内容: {str(e)}")
                    # Latin-1 で再試行
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content = json.load(f)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        print(f"Latin-1での読み込みエラー: {file_path}")
                        print(f"エラー内容: {str(e)}")
                        continue  # エラーが発生したファイルはスキップ

                # JSONのDescriptionフィールドに対して正規化と制御文字エスケープを適用
                def normalize_description_field(obj):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            if key == 'Description' and isinstance(value, str):
                                # メモリアドレスと即値の正規化
                                value = normalize_memory_addresses_and_immediates(value)
                                # 制御文字のエスケープ
                                obj[key] = escape_control_characters(value)
                            elif isinstance(value, (dict, list)):
                                normalize_description_field(value)
                    elif isinstance(obj, list):
                        for item in obj:
                            normalize_description_field(item)

                try:
                    # 正規化処理を実行
                    normalize_description_field(content)

                    # 正規化された内容をUTF-8でJSONファイルに書き戻す
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(content, f, ensure_ascii=False, separators=(',', ':'))
                        print(f"ファイルを処理しました: {file_path}")
                    
                    except UnicodeEncodeError as e:
                        print(f"UTF-8での書き込みエラー: {file_path}")
                        print(f"エラー内容: {str(e)}")
                        # UTF-8での書き込みに失敗した場合、Latin-1で再度書き込み
                        with open(file_path, 'w', encoding='latin-1') as f:
                            json.dump(content, f, ensure_ascii=False, separators=(',', ':'))
                        print(f"Latin-1でファイルを書き込みました: {file_path}")
                
                except Exception as e:
                    print(f"処理中にエラーが発生しました: {file_path}")
                    print(f"エラー内容: {str(e)}")
                    # 例外が発生した場合は変更を破棄して次に進む
                    continue

# 入力フォルダのパスを設定
input_folder = '/workspaces/mal_gpu/data/interim/extract_all_data'

# メモリアドレス、即値の正規化、制御文字のエスケープを実行
process_json_files_for_normalization(input_folder)
