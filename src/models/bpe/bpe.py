import os
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# 使用するGPUを設定
os.environ["CUDA_VISIBLE_DEVICES"] = "2,3"

# トークナイザのファイルパス
tokenizer_path = '/workspaces/mal_gpu/data/interim/tokenizer_training/bpe/concatenated_tokenizer'
training_data_path = '/workspaces/mal_gpu/data/interim/tokenizer_training/tokenizer_training_data.csv'

# 1. RobertaTokenizerを使用してトークナイザをロード
tokenizer = RobertaTokenizer.from_pretrained(tokenizer_path)

# 2. Hugging Face datasets でデータを読み込む（ストリームではなくフルデータ）
dataset = load_dataset('csv', data_files=training_data_path, split='train')

# 3. データをトークナイズする関数を作成
def preprocess_function(examples):
    return tokenizer(examples['instructions'], truncation=True, padding='max_length', max_length=512)

# 4. データセットをトークナイズ
tokenized_dataset = dataset.map(preprocess_function, batched=True, batch_size=64)

# 5. ラベルの整数マッピングを追加
label_mapping = {'benign': 0, 'malicious': 1}
tokenized_dataset = tokenized_dataset.map(lambda x: {'label': label_mapping[x['label']]})

# 6. モデルの準備（RobertaForSequenceClassificationを使用）
model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=2)

# 7. トレーニング設定
training_args = TrainingArguments(
    output_dir='/workspaces/mal_gpu/src/models/bpe/results',   # モデルの保存ディレクトリ
    evaluation_strategy="epoch",              # 各エポックの終わりに評価
    save_strategy="epoch",                    # 各エポックの終わりにモデルを保存
    learning_rate=2e-5,                       # 学習率
    per_device_train_batch_size=16,           # 各GPUあたりのバッチサイズ
    per_device_eval_batch_size=16,            # 評価時のバッチサイズ
    num_train_epochs=3,                       # エポック数
    weight_decay=0.01,                        # 重みの減衰
    logging_dir='/workspaces/mal_gpu/logs',   # ログの保存ディレクトリ
    logging_steps=10,                         # 何ステップごとにログを取るか
    save_steps=1000,                          # モデルを保存するステップ
    load_best_model_at_end=True,              # 最も性能の良いモデルを最後にロード
    report_to="none",                         # レポートの出力を抑制
    max_steps=5000                            # 総ステップ数を指定
)

# 8. トレーナーの作成
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,  # トレーニングデータセット
    tokenizer=tokenizer
)

# 9. モデルのトレーニング
trainer.train()

# トレーニング終了後にモデルを保存
model.save_pretrained('/workspaces/mal_gpu/src/models/bpe')
tokenizer.save_pretrained('/workspaces/mal_gpu/src/models/bpe')

print("モデルのトレーニングが完了しました。")
