import sentencepiece as spm
import os
import logging

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/mal_gpu/logs/tokenizer_training_sentencepiece.log'),  # ログをファイルに出力
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
def train_sentencepiece_tokenizer(input_file, output_prefix, vocab_size=50000, input_sentence_size=1000000, shuffle_input_sentence=True, max_sentence_length=0):
    """SentencePieceトークナイザーを訓練"""
    logging.info(f"SentencePieceトークナイザーの訓練を開始します。入力ファイル: {input_file}")
    
    # SentencePieceのトレーニングを実行
    spm.SentencePieceTrainer.train(
        input=input_file,
        model_prefix=output_prefix,
        vocab_size=vocab_size,
        pad_id=0,
        unk_id=1,
        bos_id=-1,
        eos_id=-1,
        pad_piece="[PAD]",
        unk_piece="[UNK]",
        user_defined_symbols=["[CLS]", "[SEP]", "[MASK]", "memoryaddress", "immediatevalue"],
        input_sentence_size=input_sentence_size,
        shuffle_input_sentence=shuffle_input_sentence,
        max_sentence_length=max_sentence_length
    )

    logging.info(f"SentencePieceトークナイザーの訓練が完了しました。出力プレフィックス: {output_prefix}")

# SentencePieceトークナイザーの訓練実行（連結パターン）
train_sentencepiece_tokenizer(
    input_file=concatenated_file,
    output_prefix='/workspaces/mal_gpu/data/interim/tokenizer_training/sentencepiece/concatenated_tokenizer',
    vocab_size=2256,
    input_sentence_size=1000000,
    shuffle_input_sentence=True,
    max_sentence_length=1073741824
)

# 必要に応じて、非連結データでも訓練を行う場合は以下を実行
train_sentencepiece_tokenizer(
    input_file=non_concatenated_file,
    output_prefix='/workspaces/mal_gpu/data/interim/tokenizer_training/sentencepiece/non_concatenated_tokenizer',
    vocab_size=2256,
    input_sentence_size=1000000,
    shuffle_input_sentence=True,
    max_sentence_length=1073741824  # 無制限に設定
)
