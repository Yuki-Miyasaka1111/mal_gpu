import zipfile
import os

"""
AveMariaRAT, Socks5Systemz, Stealc, Stopのzipファイルは、ローカルで解凍してコンテナに手動でコピーする。
これら以外のファイルを解凍する。同名のファイルが既に解凍先にある場合はスキップする。
"""
def extract_family_zips(input_folder, output_folder):
    try: 
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # スキップするファイル名のリスト
        skip_files = ["AveMariaRAT", "Socks5Systemz", "Stealc", "Stop"]

        zip_files = [f for f in os.listdir(input_folder) if f.endswith('.zip')]

        for zip_file in zip_files:
            # スキップ対象ファイルかチェック
            if any(skip in zip_file for skip in skip_files):
                print(f"スキップしたファイル: {zip_file}")
                continue

            # 解凍先に同名のディレクトリが存在するかチェック
            extracted_dir = os.path.join(output_folder, os.path.splitext(zip_file)[0])
            if os.path.exists(extracted_dir):
                print(f"既に解凍済みのファイル: {zip_file} -> {extracted_dir}")
                continue

            zip_file_path = os.path.join(input_folder, zip_file)
            try:
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extracted_dir)  # ファイル名と同じディレクトリに解凍
                print(f"解凍: {zip_file}")

            except zipfile.BadZipFile:
                print(f"エラー: {zip_file} は正しいzipファイルではありません。スキップします。")
                continue

            except Exception as e:
                print(f"このファイルでエラーが起きました。: {zip_file}: {e}")
                continue

        print("完了")

    except FileNotFoundError:
        print(f"フォルダが見つかりません: {input_folder}")

    except Exception as e:
        print(f"例外が発生しました: {e}")

# 入力フォルダと出力フォルダのパスを設定
input_folder = '/workspaces/mal_gpu/data/raw'
output_folder = '/workspaces/mal_gpu/data/interim/extract_family'

# ZIPファイルを解凍する（既に解凍済みのものはスキップ）
extract_family_zips(input_folder, output_folder)
