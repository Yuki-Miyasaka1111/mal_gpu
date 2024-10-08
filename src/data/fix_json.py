import os
import re

def fix_json_format(file_path):
    """
    JSONファイルの形式を修正する関数
    - 各JSONオブジェクトの末尾の不要なカンマを削除
    - 全体を [ ] で囲み、JSON配列形式にする
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        print(f"ファイルの読み込みエラー: {file_path}, エラー内容: {e}")
        return

    # 正規表現で各JSONオブジェクトを抽出
    # Assumption: Each JSON object starts with { and ends with }, non-greedy
    pattern = re.compile(r'\{.*?\}', re.DOTALL)
    json_objects = pattern.findall(content)

    if not json_objects:
        print(f"有効なJSONオブジェクトが見つかりませんでした: {file_path}")
        return

    # 各オブジェクトの末尾の不要なカンマを削除
    fixed_objects = []
    for obj in json_objects:
        # Remove trailing comma before }
        fixed_obj = re.sub(r',\s*}', '}', obj)
        fixed_objects.append(fixed_obj)

    # JSON配列として結合
    json_content = "[\n" + ",\n".join(fixed_objects) + "\n]"

    # 修正後の内容が空の配列でないことを確認
    if json_content.strip() == "[]":
        print(f"修正後の内容が空の配列です。書き込みをスキップします: {file_path}")
        return

    # 修正されたJSONを書き戻す
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json_content)
        print(f"JSON形式修正完了: {file_path}")
    except Exception as e:
        print(f"ファイルの書き込みエラー: {file_path}, エラー内容: {e}")

def fix_json_files_in_folder(base_folder):
    """
    指定されたフォルダ内のJSONファイルを修正し、すでに修正されているファイルはスキップする
    """
    for root, _, files in os.walk(base_folder):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read().strip()
                    # すでにJSON配列形式か確認
                    if content.startswith("[") and content.endswith("]"):
                        print(f"スキップ済み: {file_path}（すでに修正済み）")
                        continue
                except Exception as e:
                    print(f"ファイルの読み込みエラー（スキップ）: {file_path}, エラー内容: {e}")
                    continue
                # JSON形式を修正
                fix_json_format(file_path)

# 入力フォルダのパスを設定
input_folder = '/workspaces/mal_gpu/data/interim/extract_all_data_v2'

# 指定されたフォルダ内のすべてのJSONファイルを修正
fix_json_files_in_folder(input_folder)

print("すべてのJSONファイルの形式修正が完了しました。")
