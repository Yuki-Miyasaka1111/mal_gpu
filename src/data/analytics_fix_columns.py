import os
import csv
import shutil

# デバッグ用
def debug_print(message):
    print(f"[DEBUG] {message}")

# 変更するカラム名
old_column = "WMIPatch n1.n2.n3WMIQuery exit"
new_columns = ["WMIPatch n1.n2.n3", "WMIQuery exit"]

# フォルダパス
temp_folder = '/workspaces/mal_gpu/data/interim/family_csv/temp'
processed_folder = '/workspaces/mal_gpu/data/interim/family_csv/processed'

# 出力フォルダが存在しない場合は作成
if not os.path.exists(processed_folder):
    os.makedirs(processed_folder)

def process_csv(file_path, output_path):
    """
    WMIPatch n1.n2.n3WMIQuery exitカラムをWMIPatch n1.n2.n3とWMIQuery exitに分割し、
    それより右の列が上書きされないように処理する。
    """
    temp_file = output_path + ".tmp"

    try:
        with open(file_path, 'r', newline='') as infile, open(temp_file, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames.copy()  # オリジナルのfieldnamesをコピー

            # 「WMIPatch n1.n2.n3WMIQuery exit」が存在する場合
            if old_column in fieldnames:
                # カラムを削除して新しいカラムを挿入する
                column_index = fieldnames.index(old_column)
                fieldnames.remove(old_column)

                # 古いカラムの位置に新しいカラムを追加
                fieldnames.insert(column_index, new_columns[0])
                fieldnames.insert(column_index + 1, new_columns[1])

                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                # 各行を処理して、新しいカラムに0を埋め込む
                for row in reader:
                    # rowにfieldnamesにないキーがあるとエラーが出るので、事前に一致させる
                    row = {key: row[key] for key in fieldnames if key in row}
                    
                    # 新しいカラムを0で埋める
                    row[new_columns[0]] = 0  # "WMIPatch n1.n2.n3"を0で埋める
                    row[new_columns[1]] = 0  # "WMIQuery exit"を0で埋める
                    writer.writerow(row)

                debug_print(f"Processed and updated CSV file: {output_path}")
            else:
                # 該当するカラムがない場合はそのままコピー
                shutil.copy(file_path, output_path)
                debug_print(f"No changes made to CSV file: {output_path}")
        
        # 処理後、一時ファイルを元のCSVファイルに置き換え
        os.replace(temp_file, output_path)

    except Exception as e:
        debug_print(f"Error processing CSV file: {e}")

    finally:
        # 一時ファイルを削除
        if os.path.exists(temp_file):
            os.remove(temp_file)
            debug_print(f"Temporary file {temp_file} deleted.")

# tempフォルダ内のすべてのCSVファイルを処理
for csv_file in os.listdir(temp_folder):
    if csv_file.endswith('.csv'):
        file_path = os.path.join(temp_folder, csv_file)
        output_path = os.path.join(processed_folder, csv_file)
        process_csv(file_path, output_path)
