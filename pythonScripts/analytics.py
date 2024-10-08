#!/usr/bin/python

import os
import json
import csv
import re
import pandas as pd

search_strings = [
    #PeekabooPin.cpp
    "ExceptionHandler",
    "Single step exception",
    "Unaligned memory access",
    "OnContextChanged",
    "Child Process",
    "Cannot get tls key",
    #FunctionHandler.cpp
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
    "WMIPatch n1.n2.n3"
    "WMIQuery exit",
    "ChangeServiceConfigW",
    "GetEnv",
    "InitiateSystemShutdownExW",
    "GetProcAddr",
    "GetProcAddr value is",
    "GetModuleHandleA value is",
    "GetModuleHandleW value is",
    "WMIExecQuery",
    #InsHandler.cpp
    "Floating point save operation one",
    "Floating point save operation two",
    "POPFD",
    "RTDCS",
    "CPUID",
    "CPUID 0x4",
    "INT 2D",
    "IN eax, dx",
    "hlt",
    #SystemCallHooks.cpp
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
    #PeekabooPin.cpp
    "ExceptionHandler",
    "Single step exception",
    "Unaligned memory access",
    "OnContextChanged",
    "Child Process",
    "TLS key",
    #FunctionHandler.cpp
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
    "WMIPatch n1.n2.n3"
    "WMIQuery exit",
    "ChangeServiceConfigW",
    "GetEnv",
    "InitiateSystemShutdownExW",
    "GetProcAddr",
    "GetProcAddr Hit",
    "GetModuleHandleA Hit",
    "GetModuleHandleW Hit",
    "WMIExecQuery",
    #InsHandler.cpp
    "Floating point save operation one",
    "Floating point save operation two",
    "POPFD",
    "RTDCS",
    "CPUID",
    "CPUID 0x4",
    "INT 2D",
    "IN eax, dx",
    "HLT",
    #SystemCallHooks.cpp
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

folder_path = '/Mar-21-2024/data/IcedIDExtracted'
folder_path2 = "./samples/IcedID"


file_counts = {}
filesizelist =[]
#syswowlist =[]
#totalcallslist = []
#instrcutionslist = []
opcodeslist =[]
#bbllist = []
threadslist = []
nt1list =[]
nt2list =[]
nt3list =[]
nt4list =[]
nt5list =[]
nt6list =[]
nt7list =[]
nt8list =[]
nt9list =[]
nt10list =[]
nt11list =[]
nt12list =[]
nt13list =[]
nt14list =[]
nt15list =[]
nt16list =[]
nt17list =[]

nv1list =[]
nv2list =[]
nv3list =[]
nv4list =[]
nv5list =[]
nv6list =[]

#baseaddresslist = []
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    
    filepath2 = os.path.join(folder_path2, os.path.splitext(filename)[0] + '.exe')
    filesize = int (round(os.path.getsize(filepath2) / 1024))
    filesizelist.append(filesize)
    print(filename)

    if filename.endswith(".json"):
        
        with open(filepath, encoding='latin1') as f:

            total_opcodes =0
            #total_calls = 0
            #total_ins = 0
            #total_bbl = 0
            total_thrds = 0
            #baseaddr = 0x00000000
            total_nt1 = 0
            total_nt2 = 0
            total_nt3 = 0
            total_nt4 = 0
            total_nt5 = 0
            total_nt6 = 0
            total_nt7 = 0
            total_nt8 = 0
            total_nt9 = 0
            total_nt10 = 0
            total_nt11 = 0
            total_nt12 = 0
            total_nt13 = 0
            total_nt14 = 0
            total_nt15 = 0
            total_nt16 = 0
            total_nt17 = 0

            total_nv1 = 0
            total_nv2 = 0
            total_nv3 = 0
            total_nv4 = 0
            total_nv5 = 0
            total_nv6 = 0

            
            
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

            

            #matches_baseaddress = re.findall(r'"Base Address", "Description": "\b(0[xX][0-9a-fA-F]+\b)"', ''.join(lines))
            
            print("matchesthreads", matches_thrds)

            for match3 in matches_thrds:
                print("totalthreads", int(match3))
                total_thrds = int(match3)
            print("totalthreads2", total_thrds)
            for nt in nt1:
                total_nt1 = int(nt)

            for na in nt2:
                total_nt2 = int(na)

            for nb in nt3:
                total_nt3 = int(nb)

            for nc in nt4:
                total_nt4 = int(nc)               

            for nd in nt5:
                total_nt5 = int(nd)

            for ne in nt6:
                total_nt6 = int(ne)

            for nf in nt7:
                total_nt7 = int(nf)

            for ng in nt8:
                total_nt8 = int(ng)

            for nh in nt9:
                total_nt9 = int(nh)

            for ni in nt10:
                total_nt10 = int(ni)

            for nj in nt11:
                total_nt11 = int(nj)

            for nk in nt12:
                total_nt12 = int(nk)

            for nl in nt13:
                total_nt13 = int(nl)

            for nm in nt14:
                total_nt14 = int(nm)

            for nn in nt15:
                total_nt15 = int(nn)

            for np in nt16:
                total_nt16 = int(np)

            for nq in nt17:
                total_nt17 = int(nq)

            for v1 in nv1:
                total_nv1 = int(v1)
                
            for v2 in nv2:
                total_nv2 = int(v2)

            for v3 in nv3:
                total_nv3 = int(v3)

            for v4 in nv4:
                total_nv4 = int(v4)
            
            for v5 in nv5:
                total_nv5 = int(v5)

            for v6 in nv6:
                total_nv6 = int(v6)


            #for match4 in matches_baseaddress:
                #baseaddr = match4


            f.seek(0)
            file_contents = f.read()
            total_opcodes = file_contents.count("Opcode")

               
        try:
            json_contents = json.loads(file_contents)
        except json.JSONDecodeError:
            print("exiting")
            json_contents=None

        
        counts = {search_string: 0 for search_string in search_strings}
        if json_contents is None:
            for search_string in search_strings:
                counts[search_string] += file_contents.count(search_string)

            
            
        else: 
            for key, value in json_contents.items():
                for search_string in search_strings:
                    if isinstance(key, str) and search_string in key:
                        counts[search_string] += key.count(search_string)
                    elif isinstance(value, str) and search_string in value:
                     counts[search_string] += value.count(search_string)

        file_counts[filename] = counts

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

        #baseaddresslist.append(baseaddr)


with open("/Mar-21-2024/data/IcedID.csv", "w", newline ="") as f:
    print("writing")
    writer = csv.writer(f)
    writer.writerow(["Filename"] + ["File Size (kB)"] +  ["Opcodes"] + ["Threads"]  
             + ["NtProtectVirtualMemory"]       
             + ["NtAllocateVirtualMemory"] 
             + ["NtDeleteFile"] 
             + ["NtFreeVirtualMemoryCount"] 
             + ["NtFreeUserPhysicalPagesCount"] 
             + ["NtQueryVirtualMemoryCount"] 
             + ["NtCeateKeyCount"] 
             + ["NtDeleteKeyCount"] 
             + ["NtRenameKeyCount"] 
             + ["NtSetValueKeyCount"] 
             + ["NtSaveKeyCount"] 
             + ["NtOpenFileCount"] 
             + ["NtReadFileCount"] 
             + ["NtWriteFileCount"] 
             + ["NtDeviceIoControlFileCount"] 
             + ["NtQueryInformationFileCount"] 
             + ["NtSetInformationFileCount"] 

             + ["VirtualAllocCount"] 
             + ["VirtualAllocCount"] 
             + ["VirtulProtectCount"] 
             + ["Process32NextCount"] 
             + ["Process32FirstCount"] 
             + ["Process32FirstWCount"]                   
                    
            + column_strings)
    
    i=0
    for filename, counts in file_counts.items():
        row = [filename] + [filesizelist[i]] + [opcodeslist[i]] +  [threadslist[i]] + [nt1list[i]] + [nt2list[i]] + [nt3list[i]] + [nt4list[i]] + [nt5list[i]] + [nt6list[i]] + [nt7list[i]] + [nt8list[i]] + [nt9list[i]] + [nt10list[i]] + [nt11list[i]] + [nt12list[i]] + [nt13list[i]] + [nt14list[i]] + [nt15list[i]] + [nt16list[i]] + [nt17list[i]] + [nv1list[i]] + [nv2list[i]] + [nv3list[i]] + [nv4list[i]] + [nv5list[i]] + [nv6list[i]] + [counts[search_string] for search_string in search_strings]
        writer.writerow(row)
        i+=1



