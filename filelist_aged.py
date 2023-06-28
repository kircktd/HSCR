#Imported Modules
import subprocess
import logging
import sys
import shlex
import json
import time
import datetime
import re
import time
import io
import math
import reprlib
import os

#Defined Windows_Exporter Output Files
file_list = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_file_list.prom"
file_list_aged = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_file_list_aged.prom"

#Defined Variables
unique_lines = []

#Defined Program Workfile Location
user_list = r"C:\Reporting\tmp\user_list.txt"
hs_config = r"C:\Reporting\Scripts\hs_config.txt"
ps_script = r"C:\Reporting\Scripts\user_files.ps1"
ps_script_aged = r"C:\Reporting\Scripts\user_files_aged.ps1"
user_files = r"C:\Reporting\tmp\user_files.txt"
user_files_aged = r"C:\Reporting\tmp\user_files_aged.txt"
files_out = r"C:\Reporting\tmp\files_out.txt"
large_files_out = r"C:\Reporting\tmp\files_out.txt"

#Print Script Startup Message To Screen
print("Hammerspace Custom Reporting User File Listing Script")

#Define Subprocess function
def run_subprocess(command):
    output = ''
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
    return output

#Create List Of Users From Hammerspace Shares
def filter_output(output):
    lines = output.splitlines()
    for line in lines:
        if "{USER(" in line:
            start_index = line.index("{USER(") + len("{USER(")
            end_index = line.index(")", start_index)
            user = line[start_index:end_index].split()[0]
            with open(user_list, 'a') as list_out:
                 print(user, file=list_out)

while True:
    now = datetime.datetime.now()
    if now.minute == 53:
        file_names = {user_list, file_list, file_list_aged, files_out}
        for empty_file in file_names:
            with open(empty_file, "w") as f:
                f.write("")

    with open(hs_config, 'r') as hs:
        values = hs.readlines()
        for value in values:
            dir = value.strip()
            cmd = ['hs', 'sum', '-e', "IS_FILE?SUMS_TABLE{|KEY={OWNER,OWNER_GROUP,ACCESS_AGE>6months},|VALUE={1FILE,SPACE_USED,TOP10_TABLE{{space_used,dpath}}}}", dir]
            result1 = subprocess.run(cmd, capture_output=True, text=True)
            result = result1.stdout
            with open(files_out, "a") as fileout:
                lines = result.split('\n')  # Split the result into lines
                for line in lines:
                    if "KEY" in line and "VALUE" not in line:  # Check if "KEY" is present and "VALUE" is not present in the line
                        cleaned_line = line.lstrip()  # Remove leading whitespace and tabs from the line
                        if "KBYTES" not in cleaned_line and "BYTES" != cleaned_line:  # Skip lines containing "KBYTES" or exactly "BYTES"
                            print(cleaned_line, dir, file=fileout)

    with open(files_out, 'r') as file:
        lines = file.readlines()

    modified_lines = []

    user_name = ""
    file_size = ""
    file_path = ""

    with open(files_out, 'r+') as file:
        for line in file:
            line = line.strip()
        
            if "USER" in line:
                user_name = line.split("'")[1]
                user_name = user_name.split("@")[0]
        
            if "USER" not in line and user_name is not None:
                file_path_start = line.find('"') + 1
                file_path_end = line.find('"', file_path_start)
                file_path = line[file_path_start:file_path_end]
                last_two_chars = line[-2:].upper()
                modified_path = file_path.replace('.', last_two_chars, 1)
                modified_line = line[:file_path_start] + modified_path + line[file_path_end:]

                start_index = line.find("{") + 1
                end_index = line.find(" ", start_index)
                file_size_str = line[start_index:end_index]
                file_size = float(file_size_str)
                if 'GBYTES' in line:
                    file_size = file_size * 1000
            
            # Extract the uppercase letter and colon from the line
                upper_letter_colon = line.split()[-1]
            
            # Put the uppercase letter and colon in front of the string
                modified_path = upper_letter_colon + modified_path[2:]

                with open(file_list_aged, 'a') as aged_files_out:
                    print("fileshare_file_list_aged{File=","\"",modified_path,"\"",",","User=","\"",user_name,"\"","}",file_size, file=aged_files_out)
    time.sleep(60)
