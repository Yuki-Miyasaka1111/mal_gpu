import os

def rename_exe_to_json(folder_path):
    """
    フォルダ内のすべての.exeファイルを.jsonにリネームする関数。
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.exe'):
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, file[:-4] + '.json')
                
                # exe ファイルを json にリネーム
                os.rename(old_file_path, new_file_path)
                print(f".exeファイルを.jsonにリネームしました: {old_file_path} -> {new_file_path}")

    print("ファイルのリネームが完了しました。")

if __name__ == "__main__":
    # 入力フォルダのパスを設定（マルウェアファミリーのフォルダを指定）
    input_folder = '/workspaces/mal_gpu/data/interim/extract_all_data'

    # exe -> json にリネーム処理
    rename_exe_to_json(input_folder)
