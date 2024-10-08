#!/usr/bin/python

import os
import json
import csv
import re

# デバッグ用
def debug_print(message):
    print(f"[DEBUG] {message}")

search_strings = [
    # PeekabooPin.cpp
    "ExceptionHandler",
    "Single step exception",
    "Unaligned memory access",
    "OnContextChanged",
    "Child Process",
    "Cannot get tls key",
    # FunctionHandler.cpp
    "fastprox",
    "GlobalMemoryStatus",
    "EnumProcesses or K32EnumProcesses",
    "NtQuerySystemInformation ImageName",
    "NtQuerySystemInformation ImageName exit",
    "IsDebuggerPresent",
    "IsRemoteDebuggerPresent",
    "NtQueryInformationProcess_Class",
    "NtQueryInformationProcess",
    "NtQueryInformationProcess exit",
    "NtQueryPerformanceCounter tracks execution times and can reveal Pin",
    "GetAdaptersAddresses",
    "NtUserFindWindowEx",
    "VirtualAlloc_WriteWatch",
    "VirtualAlloc",
    "VirtualProtect",
    "VirtualProtect Page Guard value is",
    "VirtualQuery",
    "Process32Next",
    "Process32First value is",
    "Process32FirstW value is",
    "GetAdaptersInfo",
    "FindWindowHook",
    "FindWindow",
    "FindWindow path2 value is",
    "WNetGetProviderName",
    "WNetGetProviderName value is",
    "GetTickCount",
    "SetTimer",
    "WaitForSingleObject",
    "GetUsernameEntry",
    "GetUsernameExit",
    "EnumServicesStatusEx",
    "Strategy for EnumServicesStatusEx",
    "EnumServicesStatusEx entry",
    "IcmpCreateFile",
    "IcmpSendEchoHook",
    "GetDiskFreeSpace",
    "FindFirstFile",
    "FindFirstFile value is",
    "_popenHook",
    "Popen value is",
    "LoadLibraryA",
    "LoadLibraryA value is",
    "LoadLibraryW",
    "LoadLibraryW value is",
    "GetDeviceDriverBaseName",
    "GetWindowText",
    "GetModuleFileName",
    "GetModuleFileName exit", 
    "GetModuleFileName exit1",
    "GetModuleFileName exit2",
    "SetupDiGetDeviceRegistryProperty",
    "NtCloseHandle exit",
    "GetCursorHook",
    "GetCursorPos exit",
    "GetKeyboardLayout",
    "GetSystemInfo",
    "GetPwrCapabilities",
    "WMIQuery",
    "WMIPatch",
    "WMIPatch n1.n2.n3",
    "WMIQuery exit",
    "ChangeServiceConfigW",
    "GetEnv",
    "InitiateSystemShutdownExW",
    "GetProcAddr",
    "GetProcAddr value is",
    "GetModuleHandleA value is",
    "GetModuleHandleW value is",
    "WMIExecQuery",
    # InsHandler.cpp
    "Floating point save operation one",
    "Floating point save operation two",
    "POPFD",
    "RTDCS",
    "CPUID",
    "CPUID 0x4",
    "INT 2D",
    "IN eax, dx",
    "hlt",
    # SystemCallHooks.cpp
    "NtDelayExecution",
    "NtQueryDirectoryObject",
    "NtQueryDirectoryObject value is",
    "NtOpenKey",
    "NtOpenKey value is",
    "NtCreateFile",
    "NtCreateFile value is",
    "NtEnumerateKey",
    "NtEnumerateKey value is",
    "NtQueryValueKey",
    "NtQueryValueKey value is",
    "NtQueryAttributesFile",
    "NtQueryAttributesFile value is",
    "NtQueryObject",
    "NtUserEnumDisplayDevices",
    "NtUserEnumDisplayDevices value is",
    "NtUserFindWindowEx",
    "NtUserFindWindowEx path1 value is",
    "NtUserFindWindowEx path2 value is",
    "MUTEX",
]

column_strings = [
    # PeekabooPin.cpp
    "ExceptionHandler",
    "Single step exception",
    "Unaligned memory access",
    "OnContextChanged",
    "Child Process",
    "TLS key",
    # FunctionHandler.cpp
    "fastprox",
    "GlobalMemoryStatus",
    "EnumProcesses or K32EnumProcesses",
    "NtQuerySystemInformation ImageName",
    "NtQuerySystemInformation ImageName exit",
    "IsDebuggerPresent",
    "IsRemoteDebuggerPresent",
    "NtQueryInformationProcess_Class",
    "NtQueryInformationProcess",
    "NtQueryInformationProcess exit",
    "NtQueryPerformanceCounter",
    "GetAdaptersAddresses",
    "NtUserFindWindowEx",
    "VirtualAlloc_WriteWatch",
    "VirtualAlloc",
    "VirtualProtect",
    "VirtualProtect Page Guard",
    "VirtualQuery",
    "Process32Next",
    "Process32First",
    "Process32FirstW",
    "GetAdaptersInfo",
    "FindWindowHook",
    "FindWindow",
    "FindWindow path2",
    "WNetGetProviderName",
    "WNetGetProviderName Hit",
    "GetTickCount",
    "SetTimer",
    "WaitForSingleObject",
    "GetUsernameEntry",
    "GetUsernameExit",
    "EnumServicesStatusEx",
    "Strategy for EnumServicesStatusEx",
    "EnumServicesStatusEx entry",
    "IcmpCreateFile",
    "IcmpSendEchoHook",
    "GetDiskFreeSpace",
    "FindFirstFile",
    "FindFirstFile Hit",
    "_popenHook",
    "Popen value is",
    "LoadLibraryA",
    "LoadLibraryA Hit",
    "LoadLibraryW",
    "LoadLibraryW Hit",
    "GetDeviceDriverBaseName",
    "GetWindowText",
    "GetModuleFileName",
    "GetModuleFileName exit", 
    "GetModuleFileName exit1",
    "GetModuleFileName exit2",
    "SetupDiGetDeviceRegistryProperty",
    "NtCloseHandle exit",
    "GetCursorHook",
    "GetCursorPos exit",
    "GetKeyboardLayout",
    "GetSystemInfo",
    "GetPwrCapabilities",
    "WMIQuery",
    "WMIPatch",
    "WMIPatch n1.n2.n3",
    "WMIQuery exit",
    "ChangeServiceConfigW",
    "GetEnv",
    "InitiateSystemShutdownExW",
    "GetProcAddr",
    "GetProcAddr Hit",
    "GetModuleHandleA Hit",
    "GetModuleHandleW Hit",
    "WMIExecQuery",
    # InsHandler.cpp
    "Floating point save operation one",
    "Floating point save operation two",
    "POPFD",
    "RTDCS",
    "CPUID",
    "CPUID 0x4",
    "INT 2D",
    "IN eax, dx",
    "HLT",
    # SystemCallHooks.cpp
    "NtDelayExecution",
    "NtQueryDirectoryObject",
    "NtQueryDirectoryObject Hit",
    "NtOpenKey",
    "NtOpenKey Hit",
    "NtCreateFile",
    "NtCreateFile Exit",
    "NtEnumerateKey",
    "NtEnumerateKey Hit",
    "NtQueryValueKey",
    "NtQueryValueKey Hit",
    "NtQueryAttributesFile",
    "NtQueryAttributesFile Hit",
    "NtQueryObject",
    "NtUserEnumDisplayDevices",
    "NtUserEnumDisplayDevices Hit",
    "NtUserFindWindowEx",
    "NtUserFindWindowEx path1",
    "NtUserFindWindowEx path2",
    "MUTEX",
]

base_folder = '/workspaces/mal_gpu/data/interim/extract_all_data'
output_folder = '/workspaces/mal_gpu/data/interim/family_csv'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def check_processed_files(csv_file):
    """既存のCSVファイルを確認して、すでに処理済みのファイルをセットとして返す"""
    if os.path.exists(csv_file):
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダーをスキップ
            processed_files = {row[0] for row in reader}
        return processed_files
    return set()

def process_family_folder(family_folder, family_name):
    debug_print(f"Processing family folder: {family_folder}")
    file_counts = {}
    filesizelist = []
    opcodeslist = []
    threadslist = []
    
    nt1list = []
    nt2list = []
    nt3list = []
    nt4list = []
    nt5list = []
    nt6list = []
    nt7list = []
    nt8list = []
    nt9list = []
    nt10list = []
    nt11list = []
    nt12list = []
    nt13list = []
    nt14list = []
    nt15list = []
    nt16list = []
    nt17list = []

    nv1list = []
    nv2list = []
    nv3list = []
    nv4list = []
    nv5list = []
    nv6list = []

    # CSVファイルが存在するかチェック
    output_file = os.path.join(output_folder, f"{family_name}.csv")
    processed_files = check_processed_files(output_file)

    # CSVファイルがない場合はヘッダーを書き込む
    if not processed_files:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Filename", "File Size (kB)", "Opcodes", "Threads", 
                "NtProtectVirtualMemory", "NtAllocateVirtualMemory", "NtDeleteFile", 
                "NtFreeVirtualMemoryCount", "NtFreeUserPhysicalPagesCount", 
                "NtQueryVirtualMemoryCount", "NtCeateKeyCount", "NtDeleteKeyCount", 
                "NtRenameKeyCount", "NtSetValueKeyCount", "NtSaveKeyCount", 
                "NtOpenFileCount", "NtReadFileCount", "NtWriteFileCount", 
                "NtDeviceIoControlFileCount", "NtQueryInformationFileCount", 
                "NtSetInformationFileCount", "VirtualAllocCount", 
                "VirtualAllocCount", "VirtulProtectCount", "Process32NextCount", 
                "Process32FirstCount", "Process32FirstWCount"
            ] + column_strings)

    for filename in os.listdir(family_folder):
        if filename in processed_files:
            debug_print(f"Skipping already processed file: {filename}")
            continue  # すでに処理されたファイルをスキップ
        
        filepath = os.path.join(family_folder, filename)
        debug_print(f"Processing file: {filename}")
        if filename.endswith(".json") or filename.endswith(".exe"):
            try:
                if os.path.exists(filepath):
                    filesize = int(round(os.path.getsize(filepath) / 1024))
                else:
                    filesize = 0
                filesizelist.append(filesize)
                debug_print(f"File size for {filename}: {filesize} kB")

                with open(filepath, encoding='latin1') as f:
                    total_opcodes = 0
                    total_thrds = 0
                    total_nt1 = total_nt2 = total_nt3 = total_nt4 = total_nt5 = total_nt6 = 0
                    total_nt7 = total_nt8 = total_nt9 = total_nt10 = total_nt11 = 0
                    total_nt12 = total_nt13 = total_nt14 = total_nt15 = total_nt16 = total_nt17 = 0
                    total_nv1 = total_nv2 = total_nv3 = total_nv4 = total_nv5 = total_nv6 = 0

                    lines = f.readlines()
                    matches_thrds = re.findall(r'"Number of threads ", "Description": "(\d+)"', ''.join(lines))
                    nt1 = re.findall(r'"NtProtectVirtualMemory was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt2 = re.findall(r'"NtAllocateVirtualMemory was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt3 = re.findall(r'"NtDeleteFile was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt4 = re.findall(r'"NtFreeVirtualMemoryCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt5 = re.findall(r'"NtFreeUserPhysicalPagesCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt6 = re.findall(r'"NtQueryVirtualMemoryCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt7 = re.findall(r'"NtCeateKeyCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt8 = re.findall(r'"NtDeleteKeyCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt9 = re.findall(r'"NtRenameKeyCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt10 = re.findall(r'"NtSetValueKeyCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt11 = re.findall(r'"NtSaveKeyCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt12 = re.findall(r'"NtOpenFileCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt13 = re.findall(r'"NtReadFileCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt14 = re.findall(r'"NtWriteFileCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt15 = re.findall(r'"NtDeviceIoControlFileCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt16 = re.findall(r'"NtQueryInformationFileCount was called ", "Description": "(\d+) times"', ''.join(lines))
                    nt17 = re.findall(r'"NtSetInformationFileCount was called ", "Description": "(\d+) times"', ''.join(lines))

                    nv1 = re.findall(r'"VirtualAlloc before was called ", "Description": "(\d+) times"', ''.join(lines))
                    nv2 = re.findall(r'"VirtualAlloc after was called ", "Description": "(\d+) times"', ''.join(lines))
                    nv3 = re.findall(r'"VirtulProtect after was called ", "Description": "(\d+) times"', ''.join(lines))
                    nv4 = re.findall(r'"Process32Next after was called ", "Description": "(\d+) times"', ''.join(lines))
                    nv5 = re.findall(r'"Process32First after was called ", "Description": "(\d+) times"', ''.join(lines))
                    nv6 = re.findall(r'"Process32FirstW after was called ", "Description": "(\d+) times"', ''.join(lines))
                    debug_print(f"Threads for {filename}: {matches_thrds}")

                    for match in matches_thrds:
                        total_thrds = int(match)
                    for nt in nt1: total_nt1 = int(nt)
                    for nt in nt2: total_nt2 = int(nt)
                    for nt in nt3: total_nt3 = int(nt)
                    for nt in nt4: total_nt4 = int(nt)
                    for nt in nt5: total_nt5 = int(nt)
                    for nt in nt6: total_nt6 = int(nt)
                    for nt in nt7: total_nt7 = int(nt)
                    for nt in nt8: total_nt8 = int(nt)
                    for nt in nt9: total_nt9 = int(nt)
                    for nt in nt10: total_nt10 = int(nt)
                    for nt in nt11: total_nt11 = int(nt)
                    for nt in nt12: total_nt12 = int(nt)
                    for nt in nt13: total_nt13 = int(nt)
                    for nt in nt14: total_nt14 = int(nt)
                    for nt in nt15: total_nt15 = int(nt)
                    for nt in nt16: total_nt16 = int(nt)
                    for nt in nt17: total_nt17 = int(nt)

                    for nv in nv1: total_nv1 = int(nv)
                    for nv in nv2: total_nv2 = int(nv)
                    for nv in nv3: total_nv3 = int(nv)
                    for nv in nv4: total_nv4 = int(nv)
                    for nv in nv5: total_nv5 = int(nv)
                    for nv in nv6: total_nv6 = int(nv)

                    file_contents = ''.join(lines)
                    total_opcodes = file_contents.count("Opcode")
                    debug_print(f"Total opcodes for {filename}: {total_opcodes}")

                opcodeslist.append(total_opcodes)
                threadslist.append(total_thrds)
                nt1list.append(total_nt1)
                nt2list.append(total_nt2)
                nt3list.append(total_nt3)
                nt4list.append(total_nt4)
                nt5list.append(total_nt5)
                nt6list.append(total_nt6)
                nt7list.append(total_nt7)
                nt8list.append(total_nt8)
                nt9list.append(total_nt9)
                nt10list.append(total_nt10)
                nt11list.append(total_nt11)
                nt12list.append(total_nt12)
                nt13list.append(total_nt13)
                nt14list.append(total_nt14)
                nt15list.append(total_nt15)
                nt16list.append(total_nt16)
                nt17list.append(total_nt17)

                nv1list.append(total_nv1)
                nv2list.append(total_nv2)
                nv3list.append(total_nv3)
                nv4list.append(total_nv4)
                nv5list.append(total_nv5)
                nv6list.append(total_nv6)

                file_counts[filename] = {search_string: file_contents.count(search_string) for search_string in search_strings}

                # CSVに1行ずつ書き込む
                with open(output_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    row = [
                        filename, filesize, total_opcodes, total_thrds, 
                        total_nt1, total_nt2, total_nt3, total_nt4, total_nt5, 
                        total_nt6, total_nt7, total_nt8, total_nt9, total_nt10, 
                        total_nt11, total_nt12, total_nt13, total_nt14, total_nt15, 
                        total_nt16, total_nt17, total_nv1, total_nv2, total_nv3, 
                        total_nv4, total_nv5, total_nv6
                    ] + [file_counts[filename][search_string] for search_string in search_strings]
                    writer.writerow(row)
            
            except Exception as e:
                debug_print(f"Error processing file {filename}: {e}")

# 再帰的に各マルウェアファミリーのフォルダを処理
for family_folder in os.listdir(base_folder):
    family_folder_path = os.path.join(base_folder, family_folder)
    if os.path.isdir(family_folder_path):
        process_family_folder(family_folder_path, family_folder)
