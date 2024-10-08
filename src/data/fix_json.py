import os
import json

def is_json_already_fixed(file_path):
    """
    ファイルが既に修正されているか確認する関数
    JSONファイルが正しい配列形式（[ ] で始まり、終わっている）かを確認。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read().strip()
        except UnicodeDecodeError:
            print(f"バイナリファイルをスキップ: {file_path}")
            return True  # バイナリファイルは修正不要とみなす
    # 最初と最後が適切なJSON形式か確認
    return content.startswith("[") and content.endswith("]")

def fix_json_format(file_path):
    """
    JSONファイルを配列形式に修正する関数
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            lines = file.readlines()

    # ファイル内容が空でないかを確認
    if not lines:
        print(f"ファイルが空です: {file_path}")
        return

    # JSONファイルの形式を修正
    json_content = "[\n"
    for i, line in enumerate(lines):
        # 不要なカンマを削除
        clean_line = line.rstrip().rstrip(',').replace(', }', ' }')  # "Description"の後のカンマを削除
        if i < len(lines) - 1:
            json_content += clean_line + ",\n"
        else:
            json_content += clean_line + "\n"
    json_content += "]"

    # 書き込み前に内容が空でないかをチェック
    if json_content.strip() == "[]":
        print(f"修正後の内容が空の配列です。書き込みをスキップします: {file_path}")
        return

    # 修正されたJSONを書き戻す
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_content)

def fix_json_files_in_folder(base_folder):
    """
    指定されたフォルダ内のJSONファイルを修正し、すでに修正されているファイルはスキップする
    """
    error_dict = {}

    # 再帰的にフォルダを探索してJSONファイルを修正
    for root, _, files in os.walk(base_folder):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                try:
                    if is_json_already_fixed(file_path):
                        print(f"スキップ済み: {file_path}（すでに修正済み）")
                    else:
                        fix_json_format(file_path)
                        print(f"修正完了: {file_path}")
                except Exception as e:
                    error_dict[file_path] = str(e)

    # エラーがあった場合、errors.jsonファイルに保存
    if error_dict:
        error_file_path = os.path.join(base_folder, "fix_json_errors.json")
        with open(error_file_path, 'w', encoding='utf-8') as error_file:
            json.dump(error_dict, error_file, indent=4, ensure_ascii=False)
        print(f"エラー情報を {error_file_path} に保存しました。")


# APT28フォルダに対してJSONファイルを修正
base_folder = "/workspaces/mal_gpu/data/interim/extract_all_data/Loki"

# 指定されたフォルダ内のすべてのJSONファイルを修正
fix_json_files_in_folder(base_folder)

print("すべてのJSONファイルの修正が完了しました。")
