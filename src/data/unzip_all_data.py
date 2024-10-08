import os
import zipfile

def extract_zip(zip_file_path, extract_to_folder):
    """ZIPファイルを解凍し、再帰的にネストされたZIPファイルも解凍する"""
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_folder)
        print(f"解凍: {zip_file_path} to {extract_to_folder}")
        
        # 解凍後に、解凍先フォルダ内のZIPファイルを再帰的に解凍する
        for root, dirs, files in os.walk(extract_to_folder):
            for file in files:
                if file.endswith('.zip'):
                    nested_zip_path = os.path.join(root, file)
                    nested_extract_to_folder = os.path.join(root, os.path.splitext(file)[0])
                    
                    if not os.path.exists(nested_extract_to_folder):
                        os.makedirs(nested_extract_to_folder)

                    # ネストされたZIPファイルを解凍
                    extract_zip(nested_zip_path, nested_extract_to_folder)
                    os.remove(nested_zip_path)  # 解凍後はネストされたZIPファイルを削除
                    print(f"ネストされたZIPファイルを削除: {nested_zip_path}")
    except zipfile.BadZipFile:
        print(f"エラー: {zip_file_path} は正しいzipファイルではありません。スキップします。")
    except Exception as e:
        print(f"このファイルでエラーが起きました。: {zip_file_path}: {e}")

def extract_all_zips(input_folder, output_folder):
    """ZIPファイルを再帰的に解凍し、同名のファイルがあっても再解凍する"""
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(root, file)
                
                # ルートフォルダの直下のフォルダ名を取得し、それを使用して解凍先を決定
                relative_path = os.path.relpath(root, input_folder)
                parts = relative_path.split(os.sep)
                
                # ネストされた階層を整理して解凍先を決定
                if len(parts) > 1:
                    new_relative_path = os.path.join(parts[0], *parts[2:])
                else:
                    new_relative_path = relative_path
                
                extract_to_folder = os.path.join(output_folder, new_relative_path)
                
                # 解凍先ディレクトリに同名のファイルが存在しても再解凍する
                if not os.path.exists(extract_to_folder):
                    os.makedirs(extract_to_folder)

                # ZIPファイルを解凍し、再帰的にネストされたZIPファイルも解凍する
                extract_zip(zip_file_path, extract_to_folder)

    print("すべての解凍が完了しました。")

# 入力フォルダと出力フォルダのパスを設定
input_folder = '/workspaces/mal_gpu/data/interim/extract_family/Stop'
output_folder = '/workspaces/mal_gpu/data/interim/extract_all_data_v2'

# ZIPファイルを再帰的に解凍
extract_all_zips(input_folder, output_folder)
