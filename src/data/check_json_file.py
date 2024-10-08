import os
import json

def read_file_with_encoding(file_path, encoding='utf-8'):
    """
    指定したエンコーディングでファイルを読み込む関数。エンコーディングエラーが発生した場合は None を返す。
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        return None

def check_json_files_in_folders(base_folder):
    """
    指定されたフォルダ内のすべてのJSONファイルを確認し、内容が空であるか、正しい形式であるかを確認する。
    """
    empty_files = []  # 空ファイルを記録
    invalid_files = []  # 無効な形式のファイルを記録

    for root, _, files in os.walk(base_folder):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                content = read_file_with_encoding(file_path, 'utf-8')

                # utf-8で読み込めない場合、latin-1を試す
                if content is None:
                    content = read_file_with_encoding(file_path, 'latin-1')

                if content is None:
                    print(f"ファイル {file_path} の読み込みエラー: utf-8 および latin-1 でのデコードに失敗しました。")
                    invalid_files.append(file_path)
                    continue

                # JSONファイルの内容をチェック
                content = content.strip()
                
                # ファイルが空（"[]"のみ）の場合
                if content == "[]":
                    empty_files.append(file_path)
                else:
                    # 正しいJSON形式かどうかを確認
                    try:
                        json_data = json.loads(content)
                        # データが無効（リストではない、または空のリスト）の場合
                        if not isinstance(json_data, list) or len(json_data) == 0:
                            empty_files.append(file_path)
                    except json.JSONDecodeError:
                        invalid_files.append(file_path)

    # 結果を表示
    print("=== 結果 ===")
    print(f"空のJSONファイル: {len(empty_files)} ファイル")
    for file in empty_files:
        print(f"  - {file}")

    print(f"\n無効なJSONファイル: {len(invalid_files)} ファイル")
    for file in invalid_files:
        print(f"  - {file}")

    # 結果をファイルに保存
    with open(os.path.join(base_folder, "json_check_results.json"), 'w', encoding='utf-8') as result_file:
        json.dump({
            "empty_files": empty_files,
            "invalid_files": invalid_files
        }, result_file, indent=4, ensure_ascii=False)

    print(f"\n結果は {os.path.join(base_folder, 'json_check_results.json')} に保存されました。")

# マルウェアファミリーが格納されているベースフォルダのパスを指定
base_folder = "/workspaces/mal_gpu/data/interim/extract_all_data"

# フォルダ内のすべてのJSONファイルをチェック
check_json_files_in_folders(base_folder)
