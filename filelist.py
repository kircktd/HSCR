# -*- coding: utf-8 -*-
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

#Defined Variables
unique_lines = []

#Defined Program Workfile Location
user_list = r"C:\Reporting\tmp\user_list.txt"
hs_config = r"C:\Reporting\Scripts\hs_config.txt"
ps_script = r"C:\Reporting\Scripts\user_files.ps1"
user_files = r"C:\Reporting\Scripts\user_files.txt"

#Print Script Startup Message To Screen
print("Hammerspace Custom Reporting User File Listing Script")

def run_subprocess(command):
    output = ''
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
    return output

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
    if now.minute == 50:
        file_names = {user_list, file_list}
        for empty_file in file_names:
            with open(empty_file, "w") as f:
                f.write("")

        with open(hs_config,'r') as hs:
            for dir in hs:
                hscmd = "hs usage user"
                share = dir.strip().replace(":", "").replace('\n', '')
                cmd = (hscmd + " " + dir)
                output = run_subprocess(cmd)
                filter_output(output.decode())

        with open(user_list, 'r') as file:
            lines = file.readlines()

        unique_lines = []

        for line in lines:
            if line not in unique_lines:
                unique_lines.append(line)

        with open(user_list, 'w') as file:
            file.writelines(unique_lines)

        with open(user_list, 'r') as file:
            lines = file.readlines()  # Read all the lines from the file

        with open(user_list, 'w', encoding="utf-8") as file:
            for line in lines:
                index = line.find('@')
                if index != -1:
                    line = line[:index] +'\n'
                    line = line.replace("'", "")
                file.write(line)

        subprocess.run(["powershell.exe", "-File", ps_script], shell=True)

        with open(user_files, "r") as userfiles:
            for line in userfiles:
                line = line.rstrip()
                data = line.split(',')
                if len(data) >= 3:
                    file_path = data[0].strip().replace('\\','\\\\').lstrip()
                    file_size = data[1].strip()
                    file_size = file_size.replace(" ", "")
                    user_name = data[2].strip()
                    user_name = user_name.replace(" ", "")
                    with open(file_list, "a") as fileout:
                        print("fileshare_file_list{File=","\"",file_path,"\"",",","User=","\"",user_name,"\"","}",file_size, file=fileout)

    time.sleep(60)
