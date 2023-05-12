
![image](https://github.com/kircktd/HSCR/assets/105011940/3a2c8513-68ae-42b8-a2ec-6f7e67fc576c)
![image](https://github.com/kircktd/HSCR/assets/105011940/d5384010-1323-4d09-9b5d-608f182087dd)


<!-- ABOUT THE PROJECT -->
## About The Project
HSCR is a set of python scripts that queries the underlying Hammerspace filesystems for user specific and system specific metrics. Initially the tool provides reporting on fileshare replication stats, and user capacity and file aging stats. The scripts are designed to run in the backround. The replication monitoring script runs every 5 minutes, and the two file capacity and file aging scripts run in the backround, but wake up only once per day at 3AM and 4AM. Each of these two capacity reporting scripts walk the filesystems and can be Hammerspace Anvil CPU intensive. In light of that it is recommended to only run these once per day during low periods of system utilization. The output files generated by these scripts are feed to Grafana via Prometheous and Windows Exporter.
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

### Installation
1. Download and install the following packages in their default locations (Windows Exporter, Prometheus, Grafana)
2. Create the following directories
  - C:\Reporting
  - C:\Reporting\Scripts
  - C:\Reporting\tmp
3. Download the three reporting python scripts and install them in the C:\Reporting\Scripts directory
4. In the C:\Reporting\Scripts directory create an empty text file for each fileshare that you intend to monitor. (i.e Z.txt, Y.txt, W.txt). These files are used to calculate the latest metadata replication bandwidth for each monitored share. When additional shares are added to the montoring scheme a txt file will need to be created for each using the drive letter only.
5. Copy and modify the hsconfig.txt file to the C:\Reporting\Scripts directory. An example file is available on this git repo.


