
![image](https://github.com/kircktd/HSCR/assets/105011940/2d4209e5-0394-439d-a655-11dda59a3892)

![image](https://github.com/kircktd/HSCR/assets/105011940/e53ca2f7-52c1-40a5-b3a0-48817d09ac44)




<!-- ABOUT THE PROJECT -->
## About The Project
HSCR is a custom set of python scripts that utilize the Hammerspace Toolkit (hstk). Hammerspace hscli expressions are used to query the underlying Hammerspace filesystems for user specific and system specific metrics. Initially the tool provides reporting on fileshare replication stats, and user capacity and file aging stats. The scripts are designed to run in the backround. The replication monitoring script runs every 5 minutes, and the two file capacity and file aging scripts run in the backround, but wake up only once per day at 3AM and 4AM. Each of these two capacity reporting scripts walk the filesystems and can be Hammerspace Anvil CPU intensive. In light of that it is recommended to only run these once per day during low periods of system utilization. The output files generated by these scripts are feed to Grafana via Prometheous and Windows Exporter.
<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [MS Windows](https://msofficestore.us/?s=windows+11&post_type=product&gad=1&gclid=Cj0KCQjwpPKiBhDvARIsACn-gzD9jcRUlo_C6EHYsHoxFfCgr7VP9E9CKwX3YOFk28z-R3exmq3yXQUaAmgVEALw_wcB)
* [Python](https://python.org/)
* [Hammerspace Toolkit](https://github.com/hammer-space/hstk)
* [Windows Exporter](https://github.com/prometheus-community/windows_exporter)
* [Prometheous](https://prometheus.io/download/)
* [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/)
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Here are some basics on getting up and running. 
### Prerequisites
1. [MS Windows](https://msofficestore.us/?s=windows+11&post_type=product&gad=1&gclid=Cj0KCQjwpPKiBhDvARIsACn-gzD9jcRUlo_C6EHYsHoxFfCgr7VP9E9CKwX3YOFk28z-R3exmq3yXQUaAmgVEALw_wcB)
2. [Python](https://python.org/)
3. [Hammerspace Toolkit](https://github.com/hammer-space/hstk) (hstk) installed: `$ pip install hstk`
4. [Prometheous](https://prometheus.io/download/)
5. [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/)
6. Hammerspace File Systems Mounted As SMB Shares
<p align="right">(<a href="#top">back to top</a>)</p>

### Installation
1. Download and install the following packages in their default locations (Windows Exporter, Prometheus, Grafana)
2. Create the following directories:
  - C:\Reporting
  - C:\Reporting\Scripts
  - C:\Reporting\tmp
3. Download the three reporting python scripts and install them in the C:\Reporting\Scripts directory
4. In the C:\Reporting\tmp directory create an empty text file for each fileshare that you intend to monitor. (i.e Z.txt, Y.txt, W.txt). These files are used to calculate the latest metadata replication bandwidth for each monitored share. When additional shares are added to the montoring scheme a txt file will need to be created for each new share using the drive letter only.
5. Copy and modify the hsconfig.txt file to the C:\Reporting\Scripts directory. An example file is available on this git repo.
<p align="right">(<a href="#top">back to top</a>)</p>

### Starting
1. Right click C:\Reporting\Scripts\startup.ps1 and "Run with PowerShell"
![image](https://github.com/kircktd/HSCR/assets/105011940/69381c84-af1f-4f1b-be0b-16d833c97d47)
<p align="right">(<a href="#top">back to top</a>)</p>

### Verify Installation
1. Look in the C:\Program Files\Windows Exporter\textfile_inputs directory and verify that the following .prom files have been written. The userstats.py script runs at the top of the hour and the userstats_aged.py script runs at the bottom of the hour. It will take at least one hour for all prom files to be present. 

![image](https://github.com/kircktd/HSCR/assets/105011940/cb39e065-4069-45c0-90c0-99f09ad92c41)
3. In your web browser go to 127.0.0.1:9182 (Windows Exporter GUI). Here you will see the list of custom metrics that are being generated by the python scripts.
![image](https://github.com/kircktd/HSCR/assets/105011940/905ed900-63bf-40fc-a5a5-7675c58ad9b6)

<p align="right">(<a href="#top">back to top</a>)</p>
