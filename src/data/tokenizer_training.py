from tokenizers import Tokenizer, models, trainers, pre_tokenizers
import os
import logging
from tqdm import tqdm
import json

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/mal_gpu/logs/tokenizer_training02.log'),  # ログをファイルに出力
        logging.StreamHandler()  # 標準出力にも出力
    ]
)

# 入力ファイルのパス
concatenated_file = '/workspaces/mal_gpu/data/interim/tokenizer_training/tokenizer_training_data_concatenated01.txt'
non_concatenated_file = '/workspaces/mal_gpu/data/interim/tokenizer_training/tokenizer_training_data_non_concatenated01.txt'

# ファイルの存在チェック
if not os.path.exists(concatenated_file):
    logging.error(f"ファイルが見つかりません: {concatenated_file}")
    exit(1)

if not os.path.exists(non_concatenated_file):
    logging.error(f"ファイルが見つかりません: {non_concatenated_file}")
    exit(1)

# トークナイザーの訓練関数
def train_tokenizer(input_file, output_tokenizer_dir, model_type="BPE", is_concatenated=True):
    """全データを使用してトークナイザーを訓練"""
    logging.info(f"{model_type} トークナイザーの訓練を開始します。入力ファイル: {input_file}")

    # モデルの選択
    if model_type == "BPE":
        tokenizer = Tokenizer(models.BPE())
        trainer = trainers.BpeTrainer(
            vocab_size=50000,  # 語彙サイズは必要に応じて調整
            min_frequency=2,
            special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>", "memoryaddress", "immediatevalue"]
        )
    elif model_type == "WordPiece":
        tokenizer = Tokenizer(models.WordPiece())
        trainer = trainers.WordPieceTrainer(
            vocab_size=50000,
            min_frequency=2,
            special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>", "memoryaddress", "immediatevalue"]
        )
    elif model_type == "Unigram":
        tokenizer = Tokenizer(models.Unigram())
        trainer = trainers.UnigramTrainer(
            vocab_size=50000,
            special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>", "memoryaddress", "immediatevalue"]
        )
    else:
        raise ValueError(f"サポートされていないモデルタイプ: {model_type}")

    # 前処理の設定
    if is_concatenated:
        tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    else:
        tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

    # ファイル内の総行数をカウント（進捗バーのため）
    total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))

    # 大容量ファイルをストリーム処理するためのジェネレーター関数
    def batch_iterator(batch_size=1000):
        with open(input_file, 'r', encoding='utf-8') as f:
            batch = []
            for line in tqdm(f, total=total_lines, desc=f"{model_type} トークナイザーの訓練中", ncols=100):
                line = line.strip()
                if line == '':
                    continue
                batch.append(line)
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    # トークナイザーの訓練
    tokenizer.train_from_iterator(batch_iterator(), trainer=trainer)

    # 出力ディレクトリが存在しない場合、作成する
    if not os.path.exists(output_tokenizer_dir):
        os.makedirs(output_tokenizer_dir)

    # トークナイザーの保存 (vocab.json と merges.txt または modelファイル)
    tokenizer.model.save(output_tokenizer_dir)

    # Tokenizer config を保存
    tokenizer_config = {
        "model_type": model_type,
        "vocab_size": 50000,
        "special_tokens": ["<s>", "<pad>", "</s>", "<unk>", "<mask>", "memoryaddress", "immediatevalue"]
    }
    with open(os.path.join(output_tokenizer_dir, "tokenizer_config.json"), "w") as f:
        json.dump(tokenizer_config, f)

    logging.info(f"{model_type} トークナイザーの訓練が完了しました。保存先: {output_tokenizer_dir}")

# トークナイザーの訓練実行

# BPE トークナイザー訓練（全データ使用）
# train_tokenizer(
#     input_file=concatenated_file,
#     output_tokenizer_dir='/workspaces/mal_gpu/data/interim/tokenizer_training/bpe/concatenated_tokenizer',
#     model_type="BPE",
#     is_concatenated=True  # 連結パターン
# )

# train_tokenizer(
#     input_file=non_concatenated_file,
#     output_tokenizer_dir='/workspaces/mal_gpu/data/interim/tokenizer_training/bpe/non_concatenated_tokenizer',
#     model_type="BPE",
#     is_concatenated=False  # 非連結パターン
# )

# WordPiece トークナイザー訓練（全データ使用）
train_tokenizer(
    input_file=concatenated_file,
    output_tokenizer_dir='/workspaces/mal_gpu/data/interim/tokenizer_training/wordpiece/concatenated_tokenizer',
    model_type="WordPiece",
    is_concatenated=True
)

train_tokenizer(
    input_file=non_concatenated_file,
    output_tokenizer_dir='/workspaces/mal_gpu/data/interim/tokenizer_training/wordpiece/non_concatenated_tokenizer',
    model_type="WordPiece",
    is_concatenated=False
)

# Unigram トークナイザー訓練（全データ使用）
train_tokenizer(
    input_file=concatenated_file,
    output_tokenizer_dir='/workspaces/mal_gpu/data/interim/tokenizer_training/unigram/concatenated_tokenizer',
    model_type="Unigram",
    is_concatenated=True
)

train_tokenizer(
    input_file=non_concatenated_file,
    output_tokenizer_dir='/workspaces/mal_gpu/data/interim/tokenizer_training/unigram/non_concatenated_tokenizer',
    model_type="Unigram",
    is_concatenated=False
)
