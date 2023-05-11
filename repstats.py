#Imported Modules
import subprocess
import logging
import sys
import shlex
import json
import time
import re
import time
import io
import math
import reprlib

#Defined Variables
secstring = "SECONDS"
minstring = "MINUTES"
kilostring = "KBYTES"
megstring = "MBYTES"
gigstring = "GBYTES"
terastring = "TBYTES"

#Defined Windows_Exporter Output Files
rep_lat = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_replication_latency.prom"
rep_bw = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_replication_bandwidth.prom"
rep_pending = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_replication_pending.prom"
rep_errors = r"C:\Program Files\Windows Exporter\textfile_inputs\fileshare_replication_errors.prom"

#Defined Program Workfile Location
rep_stats = r"C:\Reporting\tmp\repstats.txt"
hs_config = r"C:\Reporting\tmp\hs_config.txt"
pend_out = r"C:\Reporting\tmp\pend.txt"
bw_raw = r"C:\Reporting\tmp\bwraw.txt"
errors = r"C:\Reporting\tmp\error.txt"

print("Hammerspace Custom Reporting Replication Stats Script")
while (True):
    
    file_names = {rep_lat, rep_bw, rep_pending, rep_errors}
    for empty_file in file_names:
        with open(empty_file, "w") as f:
            f.write("")

    def run_subprocess(command):
        output = ''
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command '{command}': {e}")
        return output

    with open(hs_config,'r') as hs:
        for dir in hs:
            with open(rep_stats, 'w') as f_obj:
                hscmd = "hs status replication"
                share = dir.strip().replace(":", "").replace('\n', '')
                cmd = (hscmd + " " + dir)
                output = run_subprocess(cmd)
                print(output, file=f_obj)

##This section of code reports on the latency of the file shares.
            with open(rep_stats, 'r') as repraw:        
                for line in (repraw.readlines()):
                    output = (line)
                    recv_filter = ' '.join(line for line in output.splitlines()if 'RECV_AGE' in line)
                    send_filter = ' '.join(line for line in output.splitlines()if 'SEND_AGE' in line)
                    recv = recv_filter.replace("|RECV_AGE = ", '')
                    send = send_filter.replace("|SEND_AGE = ", '')
                    with open(rep_lat, "a") as statsout:
                        if secstring in recv:
                            recvs_out = recv.replace("SECONDS}", "").replace('\t', '').replace(" ", "")
                            print("fileshare_replication_latency{Fileshare=",'"','\\','"',share," Receive",'\\','"','"'," }"," ",recvs_out,sep="", file=statsout, end="\n")
                        if minstring in recv:
                            recvm = recv.replace("MINUTES}", "").replace('\t', '').replace(" ", "")
                            recvs_out = recvm * 60
                            print("fileshare_replication_latency{Fileshare=",'"','\\','"',share," Receive",'\\','"','"'," }"," ",recvs_out,sep="", file=statsout, end="\n")
                        if secstring in send:
                            send_out = send.replace("SECONDS,", "").replace('\t', '').replace(" ", "")
                            print("fileshare_replication_latency{Fileshare=",'"','\\','"',share," Send",'\\','"','"'," }"," ",send_out,sep="", file=statsout, end="\n")
                        if minstring in send:
                            sendm = send.replace("MINUTES,", "").replace('\t', '')
                            send_out = sendm * 60
                            print("fileshare_replication_latency{Fileshare=",'"','\\','"',share," Send",'\\','"','"'," }"," ",send_out,sep="", file=statsout, end="\n")

#This section of the code reports on the bandwidth of the filesystem that has occurred since the last reporting interval (5 min.)
            with open(rep_stats, 'r') as repraw:
                found = "TOTAL"
                lines = repraw.readlines()
                for index, line in enumerate(lines):
                    if found in line:
                        with open(bw_raw, 'r+') as bwraw:
                            print(lines[index+2], file = bwraw)
                        with open(bw_raw, 'r+') as bwout:
                            for line in (bwout.readlines()):
                                bwout1 = line.replace("|SENT_BYTES =", " ")
                                if megstring in line:
                                    with open(f'{share}.txt', 'r') as o:
                                        bwold1 = o.read().rstrip()
                                        bwold = int(bwold1)
                                        bwout2 = bwout1.replace("MBYTES,", " ").replace(" ", "")
                                        bwout3 = float(bwout2) * 1000
                                        bwfinal1 = int(bwout3)
                                        bwfinal = str(bwfinal1 - bwold)
                                        bwsave = str(bwfinal1)
                                        with open(rep_bw, "a") as band_width:
                                            print("fileshare_replication_bandwidth{Fileshare=",'"','\\','"',share," Bandwidth",'\\','"','"',"}"," ",bwfinal,sep="", file=band_width)
                                        with open(f'{share}.txt', 'r+') as f:
                                            f.write(bwsave)
                                if kilostring in line:
                                    with open(f'{share}.txt', 'r') as o:
                                        bwold1 = o.read().rstrip()
                                        bwold = int(bwold1)
                                        bwout2 = bwout1.replace("KBYTES,", " ").replace(" ", "")
                                        bwout3 = float(bwout2)
                                        bwfinal1 = int(bwout3)
                                        bwfinal = int(bwout3)
                                        bwfinal = str(bwfinal1 - bwold)
                                        bwsave = str(bwfinal1)
                                        with open(rep_bw, "a") as band_width:
                                            print("fileshare_replication_bandwidth{Fileshare=",'"','\\','"',share," Bandwidth",'\\','"','"',"}"," ",bwfinal, sep="", file=band_width)
                                        with open(f'{share}.txt', 'r+') as f:
                                            f.write(bwsave)

#This section of the code reports on the pending requests of the filesystem. This is a point in time measurement and is not based on the last cycle period.
            with open(rep_stats, 'r') as repraw:
                found = "TOTAL"
                lines = repraw.readlines()
                for index, line in enumerate(lines):
                    if found in line:
                        with open(pend_out, 'r+') as pend:
                            print(lines[index+9].strip(), file=pend)
                        with open(pend_out, 'r') as pend1:
                            pend2 = pend1.readline().strip('\n').replace("|PENDING_REQUESTS =", " ").replace(",","").replace(" ","")
                            with open(rep_pending, "a") as pending_out:
                                print("fileshare_replication_pending{Fileshare=",'"','\\','"',share," Pending Requests",'\\','"','"',"}"," ",pend2, sep="", file=pending_out)

 #This section of the code reports on the error counts of the filesystem. This is a point in time measurement and is not based on the last cycle period.            
            with open(rep_stats, 'r') as repraw:
                found = "TOTAL"
                lines = repraw.readlines()
                for index, line in enumerate(lines):
                    if found in line:
                        with open(errors, 'r+') as error:
                            print(lines[index+5].strip(), file=error)
                        with open(errors, 'r') as error:
                            error_out = error.readline().strip('\n').replace("|ERRORED_REQUESTS =", " ").replace(",","").replace(" ","")
                            with open(rep_errors, "a") as errors_out:
                                print("fileshare_replication_error_count{Fileshare=",'"','\\','"',share," Error Count",'\\','"','"',"}"," ",error_out, sep="", file=errors_out)
                     
        time.sleep(300)
