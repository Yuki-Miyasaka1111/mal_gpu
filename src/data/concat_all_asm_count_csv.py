import os
import pandas as pd

# ディレクトリのパスを設定
instruction_directory = '/workspaces/mal_gpu/data/interim/family_asm_count_csv/instruction_counts'
category_directory = '/workspaces/mal_gpu/data/interim/family_asm_count_csv/category_counts'
instruction_output_file = '/workspaces/mal_gpu/data/processed/temp/combined_instructions.csv'
category_output_file = '/workspaces/mal_gpu/data/processed/temp/combined_categories.csv'

# 各ファミリーのデータを保持するリスト
instruction_dfs = []
category_dfs = []

# Instructionデータを結合
for file_name in os.listdir(instruction_directory):
    if file_name.endswith('.csv'):
        file_path = os.path.join(instruction_directory, file_name)
        family_name = file_name.split('.csv')[0]  # ファイル名からファミリー名を取得

        try:
            df = pd.read_csv(file_path)
            instruction_df = df[['Instruction', 'Count']].copy()
            instruction_df['Family'] = family_name  # ファミリー名を新しい列として追加
            instruction_dfs.append(instruction_df)
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

# Categoryデータを結合
for file_name in os.listdir(category_directory):
    if file_name.endswith('.csv'):
        file_path = os.path.join(category_directory, file_name)
        family_name = file_name.split('.csv')[0]  # ファイル名からファミリー名を取得

        try:
            df = pd.read_csv(file_path)
            category_df = df[['Category', 'Count']].copy()
            category_df['Family'] = family_name  # ファミリー名を新しい列として追加
            category_dfs.append(category_df)
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

# すべてのInstructionデータを結合
if instruction_dfs:
    combined_instruction_df = pd.concat(instruction_dfs, ignore_index=True)
    combined_instruction_df.to_csv(instruction_output_file, index=False)
    print(f"Combined instruction data saved as {instruction_output_file}")
else:
    print("No instruction data found.")

# すべてのCategoryデータを結合
if category_dfs:
    combined_category_df = pd.concat(category_dfs, ignore_index=True)
    combined_category_df.to_csv(category_output_file, index=False)
    print(f"Combined category data saved as {category_output_file}")
else:
    print("No category data found.")
