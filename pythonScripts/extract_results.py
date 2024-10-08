#!/usr/bin/python

import zipfile
import os

def extract_zips(input_folder, output_folder):
	try: 
		if not os.path.exists(output_folder):
			os.makedirs(output_folder)

		zip_files = [f for f in os.listdir(input_folder) if f.endswith('.zip')]

		for zip_file in zip_files:
			zip_file_path = os.path.join(input_folder, zip_file)
			with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
				zip_ref.extractall(output_folder)

			print(f"Extracted: {zip_file}")

		print("Extraction complete")

	except FileNotFoundError:
		print(f"Folder not found: {input_folder}")

	except Exception as e:
		print(f"Exception: {e}")

input_folder = './Mar-21-2024/data/IcedID'
output_folder = './Mar-21-2024/data/IcedIDExtracted'

extract_zips(input_folder, output_folder)

