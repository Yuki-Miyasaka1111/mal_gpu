import os
import pandas as pd

# フォルダパス
csv_folder = '/workspaces/mal_gpu/data/interim/family_csv/processed'
output_file = '/workspaces/mal_gpu/data/processed/temp/combined_malware_data.csv'

# 全てのCSVファイルを読み込む
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

combined_data = []

for csv_file in csv_files:
    file_path = os.path.join(csv_folder, csv_file)
    family_name = os.path.splitext(csv_file)[0]  # ファイル名からマルウェアファミリー名を取得
    
    # CSVを読み込む
    df = pd.read_csv(file_path)
    
    # ファミリー名の列を追加
    df['Family'] = family_name
    
    # データをリストに追加
    combined_data.append(df)

# 全てのデータを結合
combined_df = pd.concat(combined_data, ignore_index=True)

# 結合されたデータを保存
combined_df.to_csv(output_file, index=False)

print(f"全てのマルウェアファミリーのCSVを結合しました: {output_file}")
