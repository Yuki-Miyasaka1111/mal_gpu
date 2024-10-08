unzip_family:
	# nohup python3 /workspaces/mal_gpu/src/data/unzip_family.py > logs/unzip_family.log 2>&1 &
	python3 /workspaces/mal_gpu/src/data/unzip_family.py

unzip_all_data:
	# nohup python3 /workspaces/mal_gpu/src/data/unzip_all_data.py > logs/unzip_all_data.log 2>&1 &
	python3 /workspaces/mal_gpu/src/data/unzip_all_data.py

analytics:
	nohup python3 /workspaces/mal_gpu/src/data/analytics.py > logs/analytics.log 2>&1 &

analytics_fix_columns:
	nohup python3 /workspaces/mal_gpu/src/data/analytics_fix_columns.py > logs/analytics_fix_columns.log 2>&1 &

analytics_append_data:
	nohup python3 /workspaces/mal_gpu/src/data/analytics_append_data.py > logs/analytics_append_data.log 2>&1 &

extract_opcodes:
	nohup python3 /workspaces/mal_gpu/src/data/extract_opcodes.py > logs/extract_opcodes.log 2>&1 &
	# python3 /workspaces/mal_gpu/src/data/extract_opcodes.py

extract_opcodes_for_json_file:
	python3 /workspaces/mal_gpu/src/data/extract_opcodes_for_json_file.py

extract_instructions:
	nohup python3 /workspaces/mal_gpu/src/data/extract_instructions.py > logs/extract_instructions01.log 2>&1 &
	# python3 /workspaces/mal_gpu/src/data/extract_instructions.py

fix_json:
	# nohup python3 /workspaces/mal_gpu/src/data/fix_json.py > logs/fix_json.log 2>&1 &
	python3 /workspaces/mal_gpu/src/data/fix_json.py

fix_json_for_json_file:
	python3 /workspaces/mal_gpu/src/data/fix_json_for_json_file.py

fix_extention:
	nohup python3 /workspaces/mal_gpu/src/data/fix_extension.py > logs/fix_extension.log 2>&1 &

concat_all_csv:
	nohup python3 /workspaces/mal_gpu/src/data/concat_all_csv.py > logs/concat_all_csv.log 2>&1 &

concat_all_asm_count_csv:
	nohup python3 /workspaces/mal_gpu/src/data/concat_all_asm_count_csv.py > logs/concat_all_asm_count_csv.log 2>&1 &

count_asm:
	nohup python3 /workspaces/mal_gpu/src/data/count_asm.py > logs/count_asm.log 2>&1 &

replacement_control_characters:
	# nohup python3 /workspaces/mal_gpu/src/data/replacement_control_characters.py > logs/replacement_control_characters.log 2>&1 &
	python3 /workspaces/mal_gpu/src/data/replacement_control_characters.py

replacement_control_characters_for_json_file:
	python3 /workspaces/mal_gpu/src/data/replacement_control_characters_for_json_file.py

replacement_memory_address:
	nohup python3 /workspaces/mal_gpu/src/data/replacement_memory_address.py > logs/replacement_memory_address.log 2>&1 &

replacement_memory_address_for_json_file:
	python3 /workspaces/mal_gpu/src/data/replacement_memory_address_for_json_file.py

check_json_file:
	nohup python3 /workspaces/mal_gpu/src/data/check_json_file.py > logs/check_json_file.log 2>&1 &

# トークナイザーの訓練
tokenizer_training:
	nohup python3 /workspaces/mal_gpu/src/data/tokenizer_training.py > logs/tokenizer_training.log 2>&1 &

tokenizer_training_sentencepiece:
	nohup python3 /workspaces/mal_gpu/src/data/tokenizer_training_sentencepiece.py > logs/tokenizer_training_sentencepiece.log 2>&1 &


# モデルの訓練
model_bpe:
	nohup python3 /workspaces/mal_gpu/src/models/bpe/bpe.py > /workspaces/mal_gpu/src/models/bpe/results/bpe.log 2>&1 &