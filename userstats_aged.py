#Imported Modules
import subprocess
import logging
import sys
import shlex
import json
import time
import re
import time
import datetime
import io
import math
import reprlib
import os

#Defined Variablespip
secstring = "SECONDS"
minstring = "MINUTES"
kilostring = "KBYTES"
megstring = "MBYTES"
gigstring = "GBYTES"
terastring = "TBYTES"
kilofiles = "KFILES"
megafiles = "MFILES"
hunfiles = "FILES"

#Defined Windows_Exporter Output Files
user_files_aged = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_user_count_aged.prom"
user_capacity_aged = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_user_capacity_aged.prom"
user_files_all_aged  = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_user_count_all_aged.prom"
user_capacity_all_aged = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_user_capacity_all_aged.prom"
cap_aged_total = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_capacity_aged_total.prom"
count_aged_total = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_count_aged_total.prom"

#Defined Program Workfile Location
hs_config = r"C:\Reporting\Scripts\hs_config.txt"
user_stats_aged = r"C:\Reporting\tmp\user_stats_aged.txt"
file_count_aged = r"C:\Reporting\tmp\file_count_aged.txt"
user_cap_aged = r"C:\Reporting\tmp\user_capacity_aged.txt"


#Print Script Startup Message To Screen
print("Hammerspace Custom Reporting User Aged Stats Script")

def add_line_totals(filename):
    total_sum = 0
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        words = line.split()
        integers = [int(word) for word in words if word.isdigit()]
        if integers:
            total_sum += sum(integers)

    return total_sum

#Main While Statement
while True:
    now = datetime.datetime.now()
    if now.hour == 4:

#Flush Out Prometheous .prom Files For New Pass   
        file_names = {user_files_aged, file_count_aged, user_capacity_aged, user_cap_aged, user_files_all_aged, user_capacity_all_aged, cap_aged_total,count_aged_total}
        for empty_file in file_names:
            with open(empty_file, "w") as f:
                f.write("")

#Define variables with null values
        data = {}
        data2 = {}
        
#Subprocess Definition 
        def run_subprocess(command):
            output = ''
            try:
                output = subprocess.check_output(command, shell=True, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running command '{command}': {e}")
            return output
    
    
#Read The Fileshare Config File That Defines Which Shares Are Monitored And Run The Required HS Command For Each Share. Write The Output To User Stats File
        with open(hs_config,'r') as hs:
            for dir in hs:
                share = dir.strip().replace('\n', '')
                with open(user_stats_aged, 'w') as f_obj:
                    hscmd2 = str('IS_FILE?SUMS_TABLE{|KEY={OWNER,OWNER_GROUP,ACCESS_AGE>6weeks},|VALUE={1FILE,SPACE_USED}}')
                    output = subprocess.check_output(["hs","sum","-e", hscmd2, share])
                    output1 = output.decode('utf-8').replace("USER", "\nUSER")
                    keyword = "USER"
                    keyword1 = "TRUE"
                    for i, line in enumerate(output1.split('\n')):
                            if keyword in line and keyword1 in line:
                                print(line, file=f_obj)
                                print(line, output1.split('\n')[i+1].lstrip(), file=f_obj)

                with open(user_stats_aged, 'r') as stats:
                    for line in stats:
                        if 'USER' in line:
                            line1 = line.split()
                            if len(line1) >= 1:
                                user = line1[0].replace("USER(", "").replace("),", "")
                        if 'VALUE' in line:
                            line1 = line.split()
                            if len(line1) >= 3:
                                files = line1[2].replace("{", "")
                                if kilofiles in line:
                                    result1 = float(files)
                                    kfiles = result1 * 1000
                                    kfiles1 = int(kfiles)
                                    with open(file_count_aged, 'a') as filecount:
                                        print(user, kfiles1, share, sep=" ", file=filecount, end="\n")
                                if megafiles in line:
                                    result1 = float(files)
                                    mfiles = result1 * 1000000
                                    mfiles1 = int(mfiles)
                                    with open(file_count_aged, 'a') as filecount:
                                        print(user, mfiles1, share, sep=" ", file=filecount, end="\n")
                                if kilofiles not in line and megafiles not in line:
                                    result1 = float(files)
                                    hfiles = result1
                                    hfiles1 = int(hfiles)
                                    with open(file_count_aged, 'a') as filecount:
                                        print(user, hfiles1, share, sep=" ", file=filecount, end="\n")

                        if 'VALUE' in line:
                            line1 = line.split()
                            if len(line1) >= 5:
                                capacity = line1[4].replace("{", "")
                                if kilostring in line:
                                    result1 = float(capacity)
                                    mcap = result1 / 1024
                                    with open(user_cap_aged, 'a') as usercap:
                                        print(user, mcap, share, sep=" ", file=usercap, end="\n")

                                if megstring in line:
                                    result1 = float(capacity)
                                    mcap = result1
                                    with open(user_cap_aged, 'a') as usercap:
                                        print(user, mcap, share, sep=" ", file=usercap, end="\n")

                                if gigstring in line:
                                    result1 = float(capacity)
                                    gcap = result1 * 1024
                                    with open(user_cap_aged, 'a') as usercap:
                                        print(user, gcap, share, sep=" ", file=usercap, end="\n")
        with open(file_count_aged, "r") as file1:
            for line in file1:
                words = line.strip().split()
                key4 = words[0]
                key = key4.split("@")[0].replace("'", "").replace("\"", "")
                value1 = float(words[1])
                value = int(value1)
                if key in data:
                    data[key] += value
                else:
                    data[key] = value
            for key, value in data.items():
                with open(user_files_aged, 'a') as file_total:
                    print("fileshare_user_count_aged{User=",'"',key,'"'," }"," ",value,sep="", file=file_total, end="\n")

        with open(user_cap_aged, "r") as file2:
            for line in file2:
                words = line.strip().split()
                key3 = words[0]
                key2 = key3.split("@")[0].replace("'", "").replace("\"", "")
                value2 = float(words[1])
                value3 = int(value2)
                if key2 in data2:
                    data2[key2] += value3
                else:
                    data2[key2] = value3

        for key2, value3 in data2.items():
            with open(user_capacity_aged, 'a') as capacity_total:
                print("fileshare_user_capacity_aged{User=",'"',key2,'"'," }"," ",value3,sep="", file=capacity_total, end="\n")

        with open(file_count_aged, "r") as file2:
            for line in file2:
                words = line.strip().split()
                key5 = words[0]
                key = key5.split("@")[0].replace("'", "").replace("\"", "")
                value1 = float(words[1])
                value = int(value1)
                mount = words[2].replace(":", "")
                with open(user_files_all_aged, 'a') as files_all:
                    print("fileshare_user_count_all_aged{User=",'"',key,'"',",","Share =",'"',mount,'"',"}"," ",value,sep="",file=files_all, end="\n")

        with open(user_cap_aged, "r") as file3:
            for line in file3:
                words = line.strip().split()
                key6 = words[0]
                key = key6.split("@")[0].replace("'", "").replace("\"", "")
                value1 = float(words[1])
                value = int(value1)
                mount = words[2].replace(":", "")
                with open(user_capacity_all_aged, 'a') as capacity_all:      
                    print("fileshare_user_capacity_all_aged{User=",'"',key,'"',",","Share =",'"',mount,'"',"}"," ",value,sep="",file=capacity_all, end="\n")

#Reset Variables                
        resetvars = ['data', 'data2', 'key', 'key2', 'value', 'value2', 'value3', 'mcap', 'gcap']
        for var in resetvars:
            exec(f"{var} = 0")

        filename = user_capacity_all_aged  # Replace with the name or path of your file
        total_aged = add_line_totals(filename)
        with open(cap_aged_total, 'a') as aged_all:
            print("fileshare_capacity_aged_total{Size =",'"',megstring,'"'," }"," ",total_aged,sep="",file=aged_all, end="\n")

        filename = user_files_all_aged  # Replace with the name or path of your file
        total_aged = add_line_totals(filename)
        with open(count_aged_total, 'a') as aged_count_all:
            print("fileshare_count_aged_total{Size =",'"',hunfiles,'"'," }"," ",total_aged,sep="",file=aged_count_all, end="\n")

    time.sleep(3600)
