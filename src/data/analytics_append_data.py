import os
import csv
import re

# デバッグ用
def debug_print(message):
    print(f"[DEBUG] {message}")

# 検索対象の文字列
target_search_strings = [
    "WMIPatch n1.n2.n3",
    "WMIQuery exit"
]

# フォルダパス
extract_all_data_folder = '/workspaces/mal_gpu/data/interim/extract_all_data/Vidar'
processed_folder = '/workspaces/mal_gpu/data/interim/family_csv/processed'

def update_csv_with_counts(family_folder, family_name):
    """
    マルウェアファミリーのフォルダ内のJSONファイルを処理して、出現回数をカウントしてCSVファイルに書き込む関数。
    スキップはしない。
    """
    # マルウェアファミリーのCSVファイルパス
    csv_file_path = os.path.join(processed_folder, f"{family_name}.csv")
    
    if not os.path.exists(csv_file_path):
        debug_print(f"CSV file not found: {csv_file_path}")
        return

    # マルウェアファミリーのフォルダ内のJSONファイルを取得
    json_folder_path = os.path.join(family_folder)
    if not os.path.exists(json_folder_path):
        debug_print(f"JSON folder not found: {json_folder_path}")
        return

    temp_file = csv_file_path + ".tmp"

    try:
        with open(csv_file_path, 'r', newline='') as infile, open(temp_file, 'w', newline='') as outfile:
            debug_print(f"Editing CSV File: {csv_file_path}")
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            # カラムが存在するかを確認
            if not all(target in fieldnames for target in target_search_strings):
                debug_print(f"Required columns not found in CSV: {csv_file_path}")
                return

            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # 各行を処理
            for row in reader:
                filename = row['Filename']
                json_file_path = os.path.join(json_folder_path, filename)

                # JSONファイルが存在する場合、出現回数をカウント
                if os.path.exists(json_file_path) and (filename.endswith('.json') or filename.endswith('.exe')):
                    try:
                        with open(json_file_path, encoding='latin1') as json_file:
                            file_contents = json_file.read()

                            # 各ターゲット文字列の回数をカウントしてCSVに書き込み
                            for search_string in target_search_strings:
                                count = file_contents.count(search_string)
                                row[search_string] = count
                                debug_print(f"Found {count} occurrences of '{search_string}' in {filename}")

                    except Exception as e:
                        debug_print(f"Error processing file {filename}: {e}")
                else:
                    debug_print(f"JSON file not found for {filename}")

                # 行を更新して書き込み
                writer.writerow(row)

        # 処理後、一時ファイルを元のCSVファイルに置き換え
        os.replace(temp_file, csv_file_path)

    except Exception as e:
        debug_print(f"Error processing CSV file: {e}")

    finally:
        # 一時ファイルを削除
        if os.path.exists(temp_file):
            os.remove(temp_file)
            debug_print(f"Temporary file {temp_file} deleted.")

# # 再帰的に各マルウェアファミリーのフォルダを処理
# for family_folder in os.listdir(extract_all_data_folder):
#     family_folder_path = os.path.join(extract_all_data_folder, family_folder)
#     if os.path.isdir(family_folder_path):
#         update_csv_with_counts(family_folder_path, family_folder)

# 1つの特定のマルウェアファミリーのフォルダを処理
family_name = os.path.basename(extract_all_data_folder)  # フォルダ名をマルウェアファミリー名として使用
update_csv_with_counts(extract_all_data_folder, family_name)