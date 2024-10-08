import os
import json
import csv

# トークナイザー訓練用のデータを保存するファイル
tokenizer_training_file = '/workspaces/mal_gpu/data/interim/tokenizer_training_data02.csv'

# 処理対象の1つのJSONファイルのパス
json_file_path = '/workspaces/mal_gpu/data/interim/extract_all_data/njrat/3a4864163edd1ccae20fdfbcfbabbdd49c70f923f29c0f4a8c1687fa5c734eee.json'

def extract_opcodes_from_json(json_file_path):
    """
    JSONファイルからOpcodeを抽出する関数
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            opcodes = []
            for entry in data:
                title = entry.get("Title")
                description = entry.get("Description")

                if title == "Opcode":
                    opcodes.append(description)
            if not opcodes:
                print(f"Opcodeが見つかりませんでした: {json_file_path}")
            return opcodes
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError in file: {json_file_path}")
        print(f"Error details: {e}")
        return []
    except Exception as e:
        print(f"予期しないエラーが発生しました: {json_file_path}, エラー: {e}")
        return []

def get_label_from_path(json_file_path):
    """
    ファイルパスからラベル（benign または malicious）を判別する関数
    """
    if '/Benign' in json_file_path or '/Benign-DIKE' in json_file_path:
        return 'benign'
    else:
        return 'malicious'

print("Opcodeデータの抽出が開始されました。") 

# CSVファイルを作成し、ヘッダーを設定
with open(tokenizer_training_file, 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['path', 'instructions', 'label']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # jsonファイルであるか確認する
    if os.path.isfile(json_file_path) and json_file_path.endswith('.json'):
        print(f"現在処理中のファイル: {json_file_path}")
        opcodes = extract_opcodes_from_json(json_file_path)
        if opcodes:
            # ファイルパスからラベルを取得
            label = get_label_from_path(json_file_path)
            # JSONファイルのパス、Opcodeのシーケンス、ラベルをCSVファイルに書き込む
            writer.writerow({
                'path': json_file_path,
                'instructions': ' '.join(opcodes),
                'label': label
            })
        else:
            print(f"ファイルにOpcodeが含まれていません: {json_file_path}")

print("Opcodeデータの抽出が完了しました。")
