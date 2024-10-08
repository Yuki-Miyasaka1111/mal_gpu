import os
import re
import traceback

def unescape_and_re_escape(description_content):
    """
    エスケープの重複を削減し、適切なエスケープを再適用する関数。
    """
    # 重複バックスラッシュのパターンを検出し、適切にアンエスケープ
    while '\\\\' in description_content:
        # 4重以上のバックスラッシュを1段階ずつ減らす（例: \\\\\\\\ -> \\\\ -> \\ -> \）
        description_content = re.sub(r'(\\\\)+', lambda m: '\\' * (len(m.group(0)) // 2), description_content)

    # 制御文字をエスケープ
    description_content = re.sub(r'[\x00-\x1F]', lambda x: '\\u{:04x}'.format(ord(x.group())), description_content)

    # 再度、バックスラッシュを適切にエスケープ
    description_content = description_content.replace('\\', '\\\\')

    return description_content

def escape_control_characters_and_backslashes_in_description(file_path):
    """
    JSONファイルのDescriptionフィールドに含まれる制御文字とバックスラッシュをエスケープする関数。
    """
    content = None
    try:
        # utf-8 で読み込みを試みる
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            # utf-8 で失敗した場合、latin-1 で再試行
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"エラーが発生: {file_path}, エラー内容: {e}")
            # 詳細なエラー情報を出力
            traceback.print_exc()
            return

    if content:
        try:
            # Description フィールドの内容をアンエスケープし、その後に再エスケープ
            def escape_description(match):
                description_content = match.group(1)
                # 重複エスケープのアンエスケープと再エスケープ
                re_escaped_description = unescape_and_re_escape(description_content)
                return f'"Description": "{re_escaped_description}"'

            # 正規表現で "Description": "..." を探して、その中の制御文字とバックスラッシュをエスケープする
            escaped_content = re.sub(r'"Description":\s*"(.*?)"', escape_description, content)

            # エスケープされた内容をファイルに書き戻す
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(escaped_content)

            print(f"エスケープ完了: {file_path}")

        except Exception as e:
            print(f"エラーが発生: {file_path}, エラー内容: {e}")
            # 詳細なエラー情報を出力
            traceback.print_exc()

def process_files_in_folder(folder_path):
    """
    フォルダ内のすべてのファイルに対してDescriptionの制御文字とバックスラッシュエスケープ処理を行う。
    """
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                escape_control_characters_and_backslashes_in_description(file_path)

# 入力フォルダのパスを設定
input_folder = '/workspaces/mal_gpu/data/interim/extract_all_data'

# フォルダ内の全てのファイルを処理
process_files_in_folder(input_folder)