#!/usr/bin/python

from pathlib import Path
import os

def check_and_delete_pcap_without_json(pcap_folder, json_folder):
	try:
		pcap_files = [f for f in os.listdir(pcap_folder) if f.endswith('.pcap')]
		print(pcap_files)
		for pcap_file in pcap_files:
			pcap_path = Path(pcap_folder) / pcap_file
			json_path = Path(json_folder) / (str(pcap_file[:-5]) + '.json')
			print(f"Checking: {pcap_path}  -- > {json_path}")
			#if not pcap_path.is_file():
			if not os.path.exists(json_path):
				print(f"Deleting: {pcap_path}")
				os.remove(pcap_path)

		print("Deletions complete")

	except FileNotFoundError:
		print("Folder not found")

	except Exception as e:
		print(f"Exception: {e}")

pcap_folder = './Mar-21-2024/networktraffic/IcedID'
json_folder = './Mar-21-2024/data/IcedIDExtracted'

check_and_delete_pcap_without_json(pcap_folder, json_folder)

